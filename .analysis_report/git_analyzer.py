"""
Git History Analyzer Module

This module analyzes Git repository history to extract commit patterns,
developer contributions, and feature development timelines.
"""

import subprocess
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
from collections import defaultdict, Counter
import json

from .config import AnalysisConfig, GitAnalysisConfig


@dataclass
class CommitInfo:
    """Information about a single commit."""
    
    hash: str
    author: str
    author_email: str
    date: datetime
    message: str
    files_changed: int
    lines_added: int
    lines_deleted: int
    is_merge: bool
    branch: str


@dataclass
class AuthorStats:
    """Statistics for a single author."""
    
    name: str
    email: str
    commit_count: int
    total_lines_added: int
    total_lines_deleted: int
    first_commit: datetime
    last_commit: datetime
    commit_frequency: float
    average_commit_size: float
    contribution_percentage: float


@dataclass
class CommitPattern:
    """Analysis of commit patterns."""
    
    total_commits: int
    feature_commits: int
    bug_fix_commits: int
    refactor_commits: int
    documentation_commits: int
    merge_commits: int
    average_commits_per_day: float
    commit_frequency_trend: str
    most_active_days: List[str]
    commit_message_quality: float


@dataclass
class FeatureTimeline:
    """Timeline analysis of feature development."""
    
    feature_name: str
    start_date: datetime
    end_date: Optional[datetime]
    commit_count: int
    total_lines_changed: int
    development_duration: Optional[timedelta]
    development_intensity: float


class GitAnalyzer:
    """Analyzes Git repository history and patterns."""
    
    def __init__(self, config: AnalysisConfig):
        """
        Initialize the Git analyzer.
        
        Args:
            config: Analysis configuration
        """
        self.config = config
        self.git_config = config.git
        
    def analyze_git_history(self, repo_path: str) -> Tuple[List[CommitInfo], CommitPattern]:
        """
        Analyze the complete Git history of the repository.
        
        Args:
            repo_path: Path to the repository root
            
        Returns:
            Tuple of (commit_info_list, commit_pattern)
        """
        # Get commit history
        commits = self._get_commit_history(repo_path)
        
        # Analyze commit patterns
        patterns = self._analyze_commit_patterns(commits)
        
        return commits, patterns
    
    def analyze_developers(self, commits: List[CommitInfo]) -> List[AuthorStats]:
        """
        Analyze developer contributions and patterns.
        
        Args:
            commits: List of commit information
            
        Returns:
            List of author statistics
        """
        author_stats = defaultdict(lambda: {
            'commits': [],
            'lines_added': 0,
            'lines_deleted': 0,
            'first_commit': None,
            'last_commit': None
        })
        
        # Group commits by author
        for commit in commits:
            author = commit.author
            author_stats[author]['commits'].append(commit)
            author_stats[author]['lines_added'] += commit.lines_added
            author_stats[author]['lines_deleted'] += commit.lines_deleted
            
            if (author_stats[author]['first_commit'] is None or 
                commit.date < author_stats[author]['first_commit']):
                author_stats[author]['first_commit'] = commit.date
            
            if (author_stats[author]['last_commit'] is None or 
                commit.date > author_stats[author]['last_commit']):
                author_stats[author]['last_commit'] = commit.date
        
        # Calculate statistics for each author
        total_commits = len(commits)
        author_list = []
        
        for author, stats in author_stats.items():
            commit_count = len(stats['commits'])
            contribution_percentage = (commit_count / total_commits) * 100
            
            # Calculate commit frequency
            if stats['first_commit'] and stats['last_commit']:
                duration = (stats['last_commit'] - stats['first_commit']).days
                commit_frequency = commit_count / max(duration, 1)
            else:
                commit_frequency = 0.0
            
            # Calculate average commit size
            total_changes = stats['lines_added'] + stats['lines_deleted']
            average_commit_size = total_changes / commit_count if commit_count > 0 else 0
            
            author_list.append(AuthorStats(
                name=author,
                email=stats['commits'][0].author_email if stats['commits'] else '',
                commit_count=commit_count,
                total_lines_added=stats['lines_added'],
                total_lines_deleted=stats['lines_deleted'],
                first_commit=stats['first_commit'],
                last_commit=stats['last_commit'],
                commit_frequency=commit_frequency,
                average_commit_size=average_commit_size,
                contribution_percentage=contribution_percentage
            ))
        
        # Sort by contribution percentage
        return sorted(author_list, key=lambda x: x.contribution_percentage, reverse=True)
    
    def analyze_feature_timeline(self, commits: List[CommitInfo]) -> List[FeatureTimeline]:
        """
        Analyze the timeline of feature development.
        
        Args:
            commits: List of commit information
            
        Returns:
            List of feature timelines
        """
        # Group commits by feature (using commit message patterns)
        feature_commits = defaultdict(list)
        
        for commit in commits:
            feature = self._extract_feature_from_commit(commit)
            if feature:
                feature_commits[feature].append(commit)
        
        # Analyze each feature timeline
        feature_timelines = []
        
        for feature_name, feature_commit_list in feature_commits.items():
            if len(feature_commit_list) < 2:
                continue
            
            # Sort commits by date
            sorted_commits = sorted(feature_commit_list, key=lambda x: x.date)
            
            start_date = sorted_commits[0].date
            end_date = sorted_commits[-1].date
            development_duration = end_date - start_date
            
            # Calculate total lines changed
            total_lines_changed = sum(
                commit.lines_added + commit.lines_deleted 
                for commit in feature_commit_list
            )
            
            # Calculate development intensity (lines per day)
            development_intensity = total_lines_changed / max(development_duration.days, 1)
            
            feature_timelines.append(FeatureTimeline(
                feature_name=feature_name,
                start_date=start_date,
                end_date=end_date,
                commit_count=len(feature_commit_list),
                total_lines_changed=total_lines_changed,
                development_duration=development_duration,
                development_intensity=development_intensity
            ))
        
        return sorted(feature_timelines, key=lambda x: x.start_date)
    
    def _get_commit_history(self, repo_path: str) -> List[CommitInfo]:
        """Extract commit history from Git repository."""
        commits = []
        
        try:
            # Get commit log with detailed information
            cmd = [
                'git', 'log', '--pretty=format:%H|%an|%ae|%ad|%s',
                '--numstat', '--date=iso', '--all'
            ]
            
            result = subprocess.run(
                cmd, 
                cwd=repo_path, 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            
            if result.returncode != 0:
                print(f"Error running git log: {result.stderr}")
                return commits
            
            # Parse git log output
            lines = result.stdout.strip().split('\n')
            i = 0
            
            while i < len(lines):
                line = lines[i].strip()
                if not line:
                    i += 1
                    continue
                
                # Parse commit header
                parts = line.split('|')
                if len(parts) != 5:
                    i += 1
                    continue
                
                commit_hash, author, email, date_str, message = parts
                
                # Parse date
                try:
                    date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except ValueError:
                    date = datetime.now()
                
                # Parse file statistics
                files_changed = 0
                lines_added = 0
                lines_deleted = 0
                
                i += 1
                while i < len(lines) and lines[i].strip() and not lines[i].startswith('|'):
                    stat_line = lines[i].strip()
                    if stat_line and '\t' in stat_line:
                        parts = stat_line.split('\t')
                        if len(parts) >= 3:
                            try:
                                added = int(parts[0]) if parts[0].isdigit() else 0
                                deleted = int(parts[1]) if parts[1].isdigit() else 0
                                lines_added += added
                                lines_deleted += deleted
                                files_changed += 1
                            except ValueError:
                                pass
                    i += 1
                
                # Determine if it's a merge commit
                is_merge = 'merge' in message.lower() or 'Merge' in message
                
                # Get branch information
                branch = self._get_commit_branch(repo_path, commit_hash)
                
                commit_info = CommitInfo(
                    hash=commit_hash,
                    author=author,
                    author_email=email,
                    date=date,
                    message=message,
                    files_changed=files_changed,
                    lines_added=lines_added,
                    lines_deleted=lines_deleted,
                    is_merge=is_merge,
                    branch=branch
                )
                
                commits.append(commit_info)
        
        except subprocess.TimeoutExpired:
            print("Git log command timed out")
        except Exception as e:
            print(f"Error analyzing Git history: {e}")
        
        return commits
    
    def _get_commit_branch(self, repo_path: str, commit_hash: str) -> str:
        """Get the branch name for a specific commit."""
        try:
            cmd = ['git', 'name-rev', '--name-only', commit_hash]
            result = subprocess.run(
                cmd, 
                cwd=repo_path, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                branch = result.stdout.strip()
                # Clean up branch name
                if branch.startswith('remotes/'):
                    branch = branch.split('/')[2]  # Remove 'remotes/origin/'
                elif branch.startswith('heads/'):
                    branch = branch.split('/')[1]  # Remove 'heads/'
                return branch
            
        except Exception as e:
            print(f"Error getting branch for commit {commit_hash}: {e}")
        
        return "unknown"
    
    def _analyze_commit_patterns(self, commits: List[CommitInfo]) -> CommitPattern:
        """Analyze patterns in commit history."""
        if not commits:
            return CommitPattern(
                total_commits=0,
                feature_commits=0,
                bug_fix_commits=0,
                refactor_commits=0,
                documentation_commits=0,
                merge_commits=0,
                average_commits_per_day=0.0,
                commit_frequency_trend="unknown",
                most_active_days=[],
                commit_message_quality=0.0
            )
        
        # Count commit types
        feature_commits = 0
        bug_fix_commits = 0
        refactor_commits = 0
        documentation_commits = 0
        merge_commits = 0
        
        for commit in commits:
            message_lower = commit.message.lower()
            
            if any(pattern in message_lower for pattern in self.git_config.FEATURE_PATTERNS):
                feature_commits += 1
            elif any(pattern in message_lower for pattern in self.git_config.BUG_FIX_PATTERNS):
                bug_fix_commits += 1
            elif any(pattern in message_lower for pattern in self.git_config.REFACTOR_PATTERNS):
                refactor_commits += 1
            elif any(pattern in message_lower for pattern in self.git_config.DOCUMENTATION_PATTERNS):
                documentation_commits += 1
            
            if commit.is_merge:
                merge_commits += 1
        
        # Calculate average commits per day
        if commits:
            first_date = min(commit.date for commit in commits)
            last_date = max(commit.date for commit in commits)
            total_days = (last_date - first_date).days + 1
            average_commits_per_day = len(commits) / max(total_days, 1)
        else:
            average_commits_per_day = 0.0
        
        # Analyze commit frequency trend
        commit_frequency_trend = self._analyze_commit_frequency_trend(commits)
        
        # Find most active days
        most_active_days = self._find_most_active_days(commits)
        
        # Assess commit message quality
        commit_message_quality = self._assess_commit_message_quality(commits)
        
        return CommitPattern(
            total_commits=len(commits),
            feature_commits=feature_commits,
            bug_fix_commits=bug_fix_commits,
            refactor_commits=refactor_commits,
            documentation_commits=documentation_commits,
            merge_commits=merge_commits,
            average_commits_per_day=average_commits_per_day,
            commit_frequency_trend=commit_frequency_trend,
            most_active_days=most_active_days,
            commit_message_quality=commit_message_quality
        )
    
    def _analyze_commit_frequency_trend(self, commits: List[CommitInfo]) -> str:
        """Analyze the trend in commit frequency over time."""
        if len(commits) < 10:
            return "insufficient_data"
        
        # Group commits by week
        weekly_commits = defaultdict(int)
        for commit in commits:
            week_start = commit.date - timedelta(days=commit.date.weekday())
            week_key = week_start.strftime('%Y-%W')
            weekly_commits[week_key] += 1
        
        if len(weekly_commits) < 3:
            return "insufficient_data"
        
        # Calculate trend
        weeks = sorted(weekly_commits.keys())
        early_avg = sum(weekly_commits[week] for week in weeks[:len(weeks)//3])
        late_avg = sum(weekly_commits[week] for week in weeks[-len(weeks)//3:])
        
        if late_avg > early_avg * 1.2:
            return "increasing"
        elif late_avg < early_avg * 0.8:
            return "decreasing"
        else:
            return "stable"
    
    def _find_most_active_days(self, commits: List[CommitInfo]) -> List[str]:
        """Find the most active days of the week."""
        day_counts = Counter()
        
        for commit in commits:
            day_name = commit.date.strftime('%A')
            day_counts[day_name] += 1
        
        # Get top 3 most active days
        most_active = day_counts.most_common(3)
        return [day for day, count in most_active]
    
    def _assess_commit_message_quality(self, commits: List[CommitInfo]) -> float:
        """Assess the quality of commit messages."""
        if not commits:
            return 0.0
        
        quality_scores = []
        
        for commit in commits:
            score = 0.0
            message = commit.message.strip()
            
            # Length check
            if len(message) >= 10:
                score += 0.3
            
            # Format check (conventional commits)
            if re.match(r'^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?:', message):
                score += 0.4
            
            # Description check
            if len(message.split('\n')) > 1:
                score += 0.3
            
            quality_scores.append(score)
        
        return sum(quality_scores) / len(quality_scores)
    
    def _extract_feature_from_commit(self, commit: CommitInfo) -> Optional[str]:
        """Extract feature name from commit message."""
        message = commit.message.lower()
        
        # Look for feature-related keywords
        feature_keywords = ['feat:', 'feature:', 'add:', 'implement:', 'new:']
        
        for keyword in feature_keywords:
            if keyword in message:
                # Extract the feature name
                start_idx = message.find(keyword) + len(keyword)
                end_idx = message.find('\n') if '\n' in message else len(message)
                feature_name = message[start_idx:end_idx].strip()
                
                if feature_name:
                    return feature_name
        
        # Look for other patterns
        if 'add' in message or 'implement' in message or 'new' in message:
            # Try to extract a meaningful feature name
            words = message.split()
            for i, word in enumerate(words):
                if word in ['add', 'implement', 'new'] and i + 1 < len(words):
                    return words[i + 1].strip('.,:')
        
        return None 