"""
Developer Analyzer Module

This module analyzes developer contributions, assesses skill levels,
and evaluates team dynamics and knowledge distribution.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import math

from .config import AnalysisConfig
from .git_analyzer import CommitInfo, AuthorStats


@dataclass
class DeveloperProfile:
    """Comprehensive profile of a developer."""
    
    name: str
    email: str
    role: str
    company: str
    expertise_areas: List[str]
    skill_level: str  # 'Junior', 'Mid-level', 'Senior', 'Expert'
    skill_description: str
    contribution_pattern: str
    commit_frequency: float
    last_contribution: datetime
    business_value: str
    knowledge_areas: List[str]
    collaboration_score: float
    code_quality_score: float


@dataclass
class TeamDynamics:
    """Analysis of team dynamics and collaboration."""
    
    team_size: int
    collaboration_model: str
    knowledge_distribution: str
    bus_factor: int
    primary_contributors: List[str]
    secondary_contributors: List[str]
    knowledge_concentration: float
    team_stability: str
    communication_patterns: List[str]


class DeveloperAnalyzer:
    """Analyzes developer contributions and team dynamics."""
    
    def __init__(self, config: AnalysisConfig):
        """
        Initialize the developer analyzer.
        
        Args:
            config: Analysis configuration
        """
        self.config = config
        
    def analyze_developers(self, commits: List[CommitInfo], 
                          author_stats: List[AuthorStats]) -> List[DeveloperProfile]:
        """
        Analyze individual developers and create comprehensive profiles.
        
        Args:
            commits: List of commit information
            author_stats: Basic author statistics
            
        Returns:
            List of developer profiles
        """
        developer_profiles = []
        
        for author_stat in author_stats:
            profile = self._create_developer_profile(author_stat, commits)
            if profile:
                developer_profiles.append(profile)
        
        return sorted(developer_profiles, key=lambda x: x.contribution_pattern, reverse=True)
    
    def analyze_team_dynamics(self, developer_profiles: List[DeveloperProfile],
                             commits: List[CommitInfo]) -> TeamDynamics:
        """
        Analyze overall team dynamics and collaboration patterns.
        
        Args:
            developer_profiles: List of developer profiles
            commits: List of commit information
            
        Returns:
            Team dynamics analysis
        """
        team_size = len(developer_profiles)
        
        # Analyze collaboration model
        collaboration_model = self._determine_collaboration_model(developer_profiles, commits)
        
        # Analyze knowledge distribution
        knowledge_distribution = self._analyze_knowledge_distribution(developer_profiles)
        
        # Calculate bus factor
        bus_factor = self._calculate_bus_factor(developer_profiles)
        
        # Identify primary and secondary contributors
        primary_contributors, secondary_contributors = self._categorize_contributors(developer_profiles)
        
        # Calculate knowledge concentration
        knowledge_concentration = self._calculate_knowledge_concentration(developer_profiles)
        
        # Assess team stability
        team_stability = self._assess_team_stability(developer_profiles, commits)
        
        # Analyze communication patterns
        communication_patterns = self._analyze_communication_patterns(commits)
        
        return TeamDynamics(
            team_size=team_size,
            collaboration_model=collaboration_model,
            knowledge_distribution=knowledge_distribution,
            bus_factor=bus_factor,
            primary_contributors=primary_contributors,
            secondary_contributors=secondary_contributors,
            knowledge_concentration=knowledge_concentration,
            team_stability=team_stability,
            communication_patterns=communication_patterns
        )
    
    def _create_developer_profile(self, author_stat: AuthorStats, 
                                 commits: List[CommitInfo]) -> Optional[DeveloperProfile]:
        """Create a comprehensive developer profile."""
        try:
            # Get developer's commits
            developer_commits = [c for c in commits if c.author == author_stat.name]
            
            # Determine role and company
            role, company = self._extract_role_and_company(author_stat.email)
            
            # Identify expertise areas
            expertise_areas = self._identify_expertise_areas(developer_commits)
            
            # Assess skill level
            skill_level, skill_description = self._assess_skill_level(author_stat, developer_commits)
            
            # Determine contribution pattern
            contribution_pattern = self._determine_contribution_pattern(author_stat, developer_commits)
            
            # Assess business value
            business_value = self._assess_business_value(author_stat, developer_commits)
            
            # Identify knowledge areas
            knowledge_areas = self._identify_knowledge_areas(developer_commits)
            
            # Calculate collaboration score
            collaboration_score = self._calculate_collaboration_score(developer_commits, commits)
            
            # Calculate code quality score
            code_quality_score = self._calculate_code_quality_score(developer_commits)
            
            return DeveloperProfile(
                name=author_stat.name,
                email=author_stat.email,
                role=role,
                company=company,
                expertise_areas=expertise_areas,
                skill_level=skill_level,
                skill_description=skill_description,
                contribution_pattern=contribution_pattern,
                commit_frequency=author_stat.commit_frequency,
                last_contribution=author_stat.last_commit,
                business_value=business_value,
                knowledge_areas=knowledge_areas,
                collaboration_score=collaboration_score,
                code_quality_score=code_quality_score
            )
            
        except Exception as e:
            print(f"Error creating profile for {author_stat.name}: {e}")
            return None
    
    def _extract_role_and_company(self, email: str) -> Tuple[str, str]:
        """Extract role and company information from email."""
        # Default values
        role = "Developer"
        company = "Unknown"
        
        try:
            # Extract domain from email
            if '@' in email:
                domain = email.split('@')[1]
                
                # Common company patterns
                company_patterns = {
                    'gmail.com': 'Individual',
                    'yahoo.com': 'Individual',
                    'outlook.com': 'Individual',
                    'hotmail.com': 'Individual'
                }
                
                if domain in company_patterns:
                    company = company_patterns[domain]
                else:
                    # Try to extract company name from domain
                    company = domain.split('.')[0].title()
                
                # Try to extract role from email prefix
                prefix = email.split('@')[0]
                if '.' in prefix:
                    name_parts = prefix.split('.')
                    if len(name_parts) > 1:
                        # Look for role indicators
                        role_indicators = {
                            'dev': 'Developer',
                            'eng': 'Engineer',
                            'swe': 'Software Engineer',
                            'lead': 'Tech Lead',
                            'arch': 'Architect',
                            'mgr': 'Manager',
                            'pm': 'Product Manager'
                        }
                        
                        for indicator, role_name in role_indicators.items():
                            if indicator in prefix.lower():
                                role = role_name
                                break
        
        except Exception:
            pass
        
        return role, company
    
    def _identify_expertise_areas(self, commits: List[CommitInfo]) -> List[str]:
        """Identify areas of expertise based on commit patterns."""
        expertise_areas = []
        
        # Analyze file types and commit patterns
        file_extensions = Counter()
        commit_types = Counter()
        
        for commit in commits:
            # Count file extensions (simplified)
            if commit.files_changed > 0:
                # This is a simplified approach - in practice, you'd analyze actual files
                file_extensions['code_files'] += 1
            
            # Analyze commit message patterns
            message_lower = commit.message.lower()
            if any(pattern in message_lower for pattern in ['feat:', 'feature:', 'add:']):
                commit_types['feature_development'] += 1
            elif any(pattern in message_lower for pattern in ['fix:', 'bug:', 'patch:']):
                commit_types['bug_fixing'] += 1
            elif any(pattern in message_lower for pattern in ['refactor:', 'cleanup:']):
                commit_types['refactoring'] += 1
            elif any(pattern in message_lower for pattern in ['docs:', 'readme:']):
                commit_types['documentation'] += 1
            elif any(pattern in message_lower for pattern in ['test:', 'spec:']):
                commit_types['testing'] += 1
        
        # Determine expertise based on patterns
        if commit_types['feature_development'] > len(commits) * 0.3:
            expertise_areas.append('Feature Development')
        
        if commit_types['bug_fixing'] > len(commits) * 0.2:
            expertise_areas.append('Bug Fixing')
        
        if commit_types['refactoring'] > len(commits) * 0.2:
            expertise_areas.append('Code Refactoring')
        
        if commit_types['documentation'] > len(commits) * 0.1:
            expertise_areas.append('Documentation')
        
        if commit_types['testing'] > len(commits) * 0.1:
            expertise_areas.append('Testing')
        
        # Add general expertise if no specific areas identified
        if not expertise_areas:
            expertise_areas.append('General Development')
        
        return expertise_areas
    
    def _assess_skill_level(self, author_stat: AuthorStats, 
                           commits: List[CommitInfo]) -> Tuple[str, str]:
        """Assess the skill level of a developer."""
        # Base assessment on commit patterns and contribution
        total_commits = author_stat.commit_count
        avg_commit_size = author_stat.average_commit_size
        contribution_percentage = author_stat.contribution_percentage
        
        # Calculate skill score
        skill_score = 0
        
        # Commit count factor
        if total_commits >= 100:
            skill_score += 3
        elif total_commits >= 50:
            skill_score += 2
        elif total_commits >= 20:
            skill_score += 1
        
        # Contribution percentage factor
        if contribution_percentage >= 50:
            skill_score += 2
        elif contribution_percentage >= 20:
            skill_score += 1
        
        # Commit size factor (smaller, focused commits often indicate better practices)
        if avg_commit_size <= 50:
            skill_score += 2
        elif avg_commit_size <= 100:
            skill_score += 1
        
        # Determine skill level
        if skill_score >= 6:
            skill_level = "Expert"
            skill_description = "Highly experienced developer with deep technical knowledge and excellent practices"
        elif skill_score >= 4:
            skill_level = "Senior"
            skill_description = "Experienced developer with strong technical skills and good development practices"
        elif skill_score >= 2:
            skill_level = "Mid-level"
            skill_description = "Developer with solid technical foundation and growing expertise"
        else:
            skill_level = "Junior"
            skill_description = "Early-career developer learning and building technical skills"
        
        return skill_level, skill_description
    
    def _determine_contribution_pattern(self, author_stat: AuthorStats, 
                                      commits: List[CommitInfo]) -> str:
        """Determine the contribution pattern of a developer."""
        if not commits:
            return "No contributions"
        
        # Analyze contribution consistency
        dates = [commit.date for commit in commits]
        dates.sort()
        
        if len(dates) < 2:
            return "Single contribution"
        
        # Calculate gaps between contributions
        gaps = []
        for i in range(1, len(dates)):
            gap = (dates[i] - dates[i-1]).days
            gaps.append(gap)
        
        avg_gap = sum(gaps) / len(gaps)
        
        # Analyze commit frequency
        if author_stat.commit_frequency >= 1.0:
            pattern = "High frequency"
        elif author_stat.commit_frequency >= 0.5:
            pattern = "Regular"
        elif author_stat.commit_frequency >= 0.2:
            pattern = "Occasional"
        else:
            pattern = "Infrequent"
        
        # Add consistency information
        if avg_gap <= 3:
            consistency = "consistent"
        elif avg_gap <= 7:
            consistency = "moderately consistent"
        else:
            consistency = "sporadic"
        
        return f"{pattern}, {consistency} contributor"
    
    def _assess_business_value(self, author_stat: AuthorStats, 
                              commits: List[CommitInfo]) -> str:
        """Assess the business value of a developer's contributions."""
        # Base assessment on contribution percentage
        contribution_percentage = author_stat.contribution_percentage
        
        if contribution_percentage >= 40:
            return "Critical"
        elif contribution_percentage >= 20:
            return "High"
        elif contribution_percentage >= 10:
            return "Medium"
        elif contribution_percentage >= 5:
            return "Low"
        else:
            return "Minimal"
    
    def _identify_knowledge_areas(self, commits: List[CommitInfo]) -> List[str]:
        """Identify specific knowledge areas based on commit patterns."""
        knowledge_areas = []
        
        # Analyze commit messages for technology indicators
        tech_keywords = {
            'frontend': ['react', 'vue', 'angular', 'javascript', 'typescript', 'css', 'html'],
            'backend': ['api', 'server', 'database', 'sql', 'nosql', 'rest', 'graphql'],
            'devops': ['docker', 'kubernetes', 'ci/cd', 'deployment', 'infrastructure'],
            'testing': ['test', 'testing', 'spec', 'unit', 'integration', 'e2e'],
            'security': ['security', 'auth', 'authentication', 'encryption', 'vulnerability'],
            'performance': ['performance', 'optimization', 'caching', 'scalability']
        }
        
        for area, keywords in tech_keywords.items():
            for commit in commits:
                message_lower = commit.message.lower()
                if any(keyword in message_lower for keyword in keywords):
                    if area not in knowledge_areas:
                        knowledge_areas.append(area)
                    break
        
        # Add general areas if no specific ones identified
        if not knowledge_areas:
            knowledge_areas.append('General Software Development')
        
        return knowledge_areas
    
    def _calculate_collaboration_score(self, developer_commits: List[CommitInfo], 
                                     all_commits: List[CommitInfo]) -> float:
        """Calculate collaboration score based on commit patterns."""
        if not developer_commits:
            return 0.0
        
        # Calculate various collaboration factors
        factors = []
        
        # Factor 1: Commit frequency consistency
        if len(developer_commits) > 1:
            dates = [c.date for c in developer_commits]
            dates.sort()
            gaps = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
            avg_gap = sum(gaps) / len(gaps)
            
            if avg_gap <= 3:
                factors.append(1.0)
            elif avg_gap <= 7:
                factors.append(0.8)
            elif avg_gap <= 14:
                factors.append(0.6)
            else:
                factors.append(0.4)
        else:
            factors.append(0.5)
        
        # Factor 2: Contribution to team knowledge
        total_commits = len(all_commits)
        developer_commits_count = len(developer_commits)
        contribution_ratio = developer_commits_count / total_commits if total_commits > 0 else 0
        
        if contribution_ratio >= 0.3:
            factors.append(1.0)
        elif contribution_ratio >= 0.2:
            factors.append(0.8)
        elif contribution_ratio >= 0.1:
            factors.append(0.6)
        else:
            factors.append(0.4)
        
        # Factor 3: Code quality (simplified)
        quality_scores = []
        for commit in developer_commits:
            score = 0.5  # Base score
            
            # Message quality
            if len(commit.message) >= 20:
                score += 0.2
            
            # Commit size (smaller commits often indicate better practices)
            if commit.lines_added + commit.lines_deleted <= 100:
                score += 0.3
            elif commit.lines_added + commit.lines_deleted <= 500:
                score += 0.1
            
            quality_scores.append(score)
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
        factors.append(avg_quality)
        
        # Calculate overall collaboration score
        return sum(factors) / len(factors)
    
    def _calculate_code_quality_score(self, commits: List[CommitInfo]) -> float:
        """Calculate code quality score based on commit patterns."""
        if not commits:
            return 0.0
        
        quality_scores = []
        
        for commit in commits:
            score = 0.5  # Base score
            
            # Message quality
            message = commit.message.strip()
            if len(message) >= 15:
                score += 0.2
            
            # Conventional commit format
            if any(pattern in message.lower() for pattern in ['feat:', 'fix:', 'docs:', 'refactor:']):
                score += 0.2
            
            # Commit size (smaller commits often indicate better practices)
            total_changes = commit.lines_added + commit.lines_deleted
            if total_changes <= 50:
                score += 0.3
            elif total_changes <= 200:
                score += 0.2
            elif total_changes <= 500:
                score += 0.1
            
            # File count (focused commits)
            if commit.files_changed <= 3:
                score += 0.2
            elif commit.files_changed <= 10:
                score += 0.1
            
            quality_scores.append(min(score, 1.0))
        
        return sum(quality_scores) / len(quality_scores)
    
    def _determine_collaboration_model(self, developer_profiles: List[DeveloperProfile],
                                     commits: List[CommitInfo]) -> str:
        """Determine the collaboration model used by the team."""
        if not developer_profiles:
            return "Unknown"
        
        # Analyze team composition
        primary_contributors = [p for p in developer_profiles if p.business_value in ['Critical', 'High']]
        secondary_contributors = [p for p in developer_profiles if p.business_value in ['Medium', 'Low']]
        
        if len(primary_contributors) == 1 and len(secondary_contributors) <= 2:
            return "Single Lead with Support"
        elif len(primary_contributors) <= 2 and len(secondary_contributors) >= 3:
            return "Small Core Team with Extended Support"
        elif len(primary_contributors) >= 3:
            return "Collaborative Team"
        else:
            return "Distributed Team"
    
    def _analyze_knowledge_distribution(self, developer_profiles: List[DeveloperProfile]) -> str:
        """Analyze how knowledge is distributed across the team."""
        if not developer_profiles:
            return "Unknown"
        
        # Calculate knowledge concentration
        total_contributors = len(developer_profiles)
        primary_contributors = [p for p in developer_profiles if p.business_value in ['Critical', 'High']]
        
        concentration_ratio = len(primary_contributors) / total_contributors
        
        if concentration_ratio <= 0.3:
            return "Well Distributed"
        elif concentration_ratio <= 0.5:
            return "Moderately Distributed"
        else:
            return "Highly Concentrated"
    
    def _calculate_bus_factor(self, developer_profiles: List[DeveloperProfile]) -> int:
        """Calculate the bus factor (how many developers can leave before project becomes unmaintainable)."""
        if not developer_profiles:
            return 0
        
        # Sort by business value contribution
        sorted_profiles = sorted(developer_profiles, 
                               key=lambda x: {'Critical': 5, 'High': 4, 'Medium': 3, 'Low': 2, 'Minimal': 1}[x.business_value],
                               reverse=True)
        
        # Calculate cumulative contribution
        total_contributors = len(developer_profiles)
        bus_factor = 0
        
        for profile in sorted_profiles:
            bus_factor += 1
            # If removing this developer would leave insufficient knowledge, stop
            if bus_factor >= total_contributors * 0.7:  # 70% threshold
                break
        
        return bus_factor
    
    def _categorize_contributors(self, developer_profiles: List[DeveloperProfile]) -> Tuple[List[str], List[str]]:
        """Categorize developers as primary or secondary contributors."""
        primary = [p.name for p in developer_profiles if p.business_value in ['Critical', 'High']]
        secondary = [p.name for p in developer_profiles if p.business_value in ['Medium', 'Low', 'Minimal']]
        
        return primary, secondary
    
    def _calculate_knowledge_concentration(self, developer_profiles: List[DeveloperProfile]) -> float:
        """Calculate the concentration of knowledge in the team."""
        if not developer_profiles:
            return 0.0
        
        # Calculate weighted knowledge concentration
        total_weight = 0
        weighted_sum = 0
        
        for profile in developer_profiles:
            weight = {'Critical': 5, 'High': 4, 'Medium': 3, 'Low': 2, 'Minimal': 1}[profile.business_value]
            total_weight += weight
            weighted_sum += weight * profile.contribution_pattern
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _assess_team_stability(self, developer_profiles: List[DeveloperProfile],
                              commits: List[CommitInfo]) -> str:
        """Assess the stability of the development team."""
        if not developer_profiles or not commits:
            return "Unknown"
        
        # Analyze recent activity
        recent_cutoff = datetime.now() - timedelta(days=30)
        recent_commits = [c for c in commits if c.date > recent_cutoff]
        
        if not recent_commits:
            return "Inactive"
        
        # Count active developers in recent period
        recent_authors = set(c.author for c in recent_commits)
        total_developers = len(developer_profiles)
        active_ratio = len(recent_authors) / total_developers
        
        if active_ratio >= 0.8:
            return "Very Stable"
        elif active_ratio >= 0.6:
            return "Stable"
        elif active_ratio >= 0.4:
            return "Moderately Stable"
        else:
            return "Unstable"
    
    def _analyze_communication_patterns(self, commits: List[CommitInfo]) -> List[str]:
        """Analyze communication patterns in commit messages."""
        patterns = []
        
        if not commits:
            return patterns
        
        # Analyze commit message patterns
        message_lengths = [len(c.message) for c in commits]
        avg_message_length = sum(message_lengths) / len(message_lengths)
        
        if avg_message_length >= 50:
            patterns.append("Detailed Communication")
        elif avg_message_length >= 20:
            patterns.append("Standard Communication")
        else:
            patterns.append("Minimal Communication")
        
        # Check for conventional commit format usage
        conventional_commits = sum(1 for c in commits 
                                 if any(pattern in c.message.lower() 
                                       for pattern in ['feat:', 'fix:', 'docs:', 'refactor:']))
        
        conventional_ratio = conventional_commits / len(commits)
        
        if conventional_ratio >= 0.7:
            patterns.append("Structured Commit Messages")
        elif conventional_ratio >= 0.4:
            patterns.append("Mixed Commit Styles")
        else:
            patterns.append("Informal Commit Messages")
        
        return patterns 