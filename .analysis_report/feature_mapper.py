"""
Feature Mapper Module

This module identifies features in the project, assesses their complexity,
and maps them to development time estimates.
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
from pathlib import Path

from config import AnalysisConfig
from git_analyzer import CommitInfo


@dataclass
class Feature:
    """Represents a feature in the project."""
    
    name: str
    description: str
    complexity: str  # 'low', 'medium', 'high'
    status: str  # 'completed', 'in_progress', 'planned'
    estimated_hours: float
    actual_hours: Optional[float]
    commit_count: int
    lines_of_code: int
    business_value: str
    priority: str
    risk_level: str
    confidence: float
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    dependencies: List[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []


@dataclass
class FeatureGroup:
    """A group of related features."""
    
    name: str
    features: List[Feature]
    total_hours: float
    average_complexity: str
    business_impact: str


class FeatureMapper:
    """Maps and analyzes features in the project."""
    
    def __init__(self, config: AnalysisConfig):
        """
        Initialize the feature mapper.
        
        Args:
            config: Analysis configuration
        """
        self.config = config
        
    def identify_features(self, commits: List[CommitInfo], 
                         repo_structure: Dict) -> List[Feature]:
        """
        Identify features from commit history and repository structure.
        
        Args:
            commits: List of commit information
            repo_structure: Repository structure information
            
        Returns:
            List of identified features
        """
        features = []
        
        # Extract features from commit messages
        commit_features = self._extract_features_from_commits(commits)
        
        # Extract features from directory structure
        dir_features = self._extract_features_from_structure(repo_structure)
        
        # Merge and deduplicate features
        all_features = self._merge_features(commit_features, dir_features)
        
        # Analyze each feature
        for feature_name, feature_data in all_features.items():
            feature = self._create_feature_object(feature_name, feature_data, commits)
            if feature:
                features.append(feature)
        
        return sorted(features, key=lambda x: x.estimated_hours, reverse=True)
    
    def assess_complexity(self, feature: Feature) -> str:
        """
        Assess the complexity of a feature.
        
        Args:
            feature: Feature to assess
            
        Returns:
            Complexity level: 'low', 'medium', or 'high'
        """
        # Use configuration thresholds
        complexity = self.config.get_complexity_level(
            feature.lines_of_code, 
            feature.commit_count
        )
        
        # Adjust based on additional factors
        if feature.dependencies and len(feature.dependencies) > 3:
            if complexity == 'low':
                complexity = 'medium'
            elif complexity == 'medium':
                complexity = 'high'
        
        if feature.risk_level == 'high':
            if complexity == 'low':
                complexity = 'medium'
            elif complexity == 'medium':
                complexity = 'high'
        
        return complexity
    
    def estimate_development_time(self, feature: Feature) -> float:
        """
        Estimate development time for a feature.
        
        Args:
            feature: Feature to estimate
            
        Returns:
            Estimated hours
        """
        # Use configuration-based estimation
        base_hours = self.config.get_time_estimate(
            feature.complexity, 
            feature.commit_count
        )
        
        # Adjust based on feature characteristics
        adjustments = 1.0
        
        # Business value adjustment
        if feature.business_value == 'Critical':
            adjustments *= 1.2  # More time for critical features
        elif feature.business_value == 'Minimal':
            adjustments *= 0.8  # Less time for minimal features
        
        # Risk adjustment
        if feature.risk_level == 'High':
            adjustments *= 1.3  # More time for high-risk features
        elif feature.risk_level == 'Low':
            adjustments *= 0.9  # Less time for low-risk features
        
        # Dependency adjustment
        if feature.dependencies:
            adjustments *= (1 + len(feature.dependencies) * 0.1)
        
        return round(base_hours * adjustments, 1)
    
    def group_features(self, features: List[Feature]) -> List[FeatureGroup]:
        """
        Group features by logical categories.
        
        Args:
            features: List of features to group
            
        Returns:
            List of feature groups
        """
        groups = defaultdict(list)
        
        for feature in features:
            # Determine group based on feature name and tags
            group_name = self._determine_feature_group(feature)
            groups[group_name].append(feature)
        
        feature_groups = []
        
        for group_name, group_features in groups.items():
            total_hours = sum(f.estimated_hours for f in group_features)
            
            # Calculate average complexity
            complexity_scores = {'low': 1, 'medium': 2, 'high': 3}
            avg_complexity_score = sum(complexity_scores[f.complexity] for f in group_features) / len(group_features)
            
            if avg_complexity_score <= 1.5:
                avg_complexity = 'low'
            elif avg_complexity_score <= 2.5:
                avg_complexity = 'medium'
            else:
                avg_complexity = 'high'
            
            # Determine business impact
            business_impact = self._determine_group_business_impact(group_features)
            
            feature_groups.append(FeatureGroup(
                name=group_name,
                features=group_features,
                total_hours=total_hours,
                average_complexity=avg_complexity,
                business_impact=business_impact
            ))
        
        return sorted(feature_groups, key=lambda x: x.total_hours, reverse=True)
    
    def _extract_features_from_commits(self, commits: List[CommitInfo]) -> Dict[str, Dict]:
        """Extract features from commit messages."""
        features = defaultdict(lambda: {
            'commits': [],
            'lines_changed': 0,
            'start_date': None,
            'end_date': None,
            'tags': set()
        })
        
        for commit in commits:
            feature_name = self._extract_feature_name_from_commit(commit)
            if feature_name:
                features[feature_name]['commits'].append(commit)
                features[feature_name]['lines_changed'] += (
                    commit.lines_added + commit.lines_deleted
                )
                
                # Track dates
                if (features[feature_name]['start_date'] is None or 
                    commit.date < features[feature_name]['start_date']):
                    features[feature_name]['start_date'] = commit.date
                
                if (features[feature_name]['end_date'] is None or 
                    commit.date > features[feature_name]['end_date']):
                    features[feature_name]['end_date'] = commit.date
                
                # Extract tags from commit message
                tags = self._extract_tags_from_commit(commit)
                features[feature_name]['tags'].update(tags)
        
        # Convert to regular dict
        return {name: {
            'commits': data['commits'],
            'lines_changed': data['lines_changed'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'tags': list(data['tags'])
        } for name, data in features.items()}
    
    def _extract_features_from_structure(self, repo_structure: Dict) -> Dict[str, Dict]:
        """Extract features from repository structure."""
        features = {}
        
        # Look for feature-related directories
        for directory in repo_structure.get('directories', []):
            if self._is_feature_directory(directory):
                feature_name = self._extract_feature_name_from_directory(directory)
                if feature_name:
                    features[feature_name] = {
                        'commits': [],
                        'lines_changed': 0,
                        'start_date': None,
                        'end_date': None,
                        'tags': ['structure-based']
                    }
        
        return features
    
    def _merge_features(self, commit_features: Dict, 
                       dir_features: Dict) -> Dict[str, Dict]:
        """Merge features from different sources."""
        merged = {}
        
        # Add commit-based features
        for name, data in commit_features.items():
            merged[name] = data
        
        # Add or merge directory-based features
        for name, data in dir_features.items():
            if name in merged:
                # Merge with existing feature
                merged[name]['tags'].extend(data['tags'])
            else:
                merged[name] = data
        
        return merged
    
    def _create_feature_object(self, feature_name: str, feature_data: Dict, 
                              commits: List[CommitInfo]) -> Optional[Feature]:
        """Create a Feature object from feature data."""
        try:
            # Calculate commit count
            commit_count = len(feature_data['commits'])
            
            # Estimate lines of code
            lines_of_code = feature_data.get('lines_changed', 0)
            
            # Determine status
            status = self._determine_feature_status(feature_data)
            
            # Determine business value
            business_value = self._determine_business_value(feature_name, feature_data)
            
            # Determine priority
            priority = self._determine_priority(feature_name, feature_data)
            
            # Determine risk level
            risk_level = self._determine_risk_level(feature_data)
            
            # Calculate confidence
            confidence = self._calculate_feature_confidence(feature_data)
            
            # Create feature object
            feature = Feature(
                name=feature_name,
                description=self._generate_feature_description(feature_name, feature_data),
                complexity='medium',  # Will be updated after creation
                status=status,
                estimated_hours=0.0,  # Will be calculated after creation
                actual_hours=None,
                commit_count=commit_count,
                lines_of_code=lines_of_code,
                business_value=business_value,
                priority=priority,
                risk_level=risk_level,
                confidence=confidence,
                start_date=feature_data.get('start_date'),
                end_date=feature_data.get('end_date'),
                dependencies=self._extract_dependencies(feature_data),
                tags=feature_data.get('tags', [])
            )
            
            # Update complexity and time estimate
            feature.complexity = self.assess_complexity(feature)
            feature.estimated_hours = self.estimate_development_time(feature)
            
            return feature
            
        except Exception as e:
            print(f"Error creating feature object for {feature_name}: {e}")
            return None
    
    def _extract_feature_name_from_commit(self, commit: CommitInfo) -> Optional[str]:
        """Extract feature name from commit message."""
        message = commit.message.lower()
        
        # Look for conventional commit format
        conventional_patterns = [
            r'feat\(([^)]+)\):',
            r'feature\(([^)]+)\):',
            r'add\(([^)]+)\):',
            r'new\(([^)]+)\):'
        ]
        
        for pattern in conventional_patterns:
            match = re.search(pattern, message)
            if match:
                return match.group(1).strip()
        
        # Look for other patterns
        if 'feat:' in message:
            # Extract text after feat:
            start_idx = message.find('feat:') + 5
            end_idx = message.find('\n') if '\n' in message else len(message)
            feature_name = message[start_idx:end_idx].strip()
            if feature_name:
                return feature_name
        
        # Look for feature-related keywords
        feature_keywords = ['add', 'implement', 'new', 'create', 'build']
        for keyword in feature_keywords:
            if keyword in message:
                # Extract the next word as feature name
                words = message.split()
                try:
                    keyword_idx = words.index(keyword)
                    if keyword_idx + 1 < len(words):
                        return words[keyword_idx + 1].strip('.,:')
                except ValueError:
                    continue
        
        return None
    
    def _extract_tags_from_commit(self, commit: CommitInfo) -> List[str]:
        """Extract tags from commit message."""
        tags = []
        message = commit.message.lower()
        
        # Look for common tags
        tag_patterns = {
            'bugfix': ['bug', 'fix', 'patch'],
            'feature': ['feat', 'feature', 'add', 'new'],
            'refactor': ['refactor', 'refactor', 'cleanup'],
            'documentation': ['docs', 'documentation', 'readme'],
            'testing': ['test', 'testing', 'spec'],
            'performance': ['perf', 'performance', 'optimize'],
            'security': ['security', 'secure', 'vulnerability']
        }
        
        for tag, keywords in tag_patterns.items():
            if any(keyword in message for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    def _is_feature_directory(self, directory: str) -> bool:
        """Determine if a directory represents a feature."""
        feature_indicators = [
            'feature', 'component', 'module', 'service', 'api',
            'controller', 'model', 'view', 'page', 'screen'
        ]
        
        directory_lower = directory.lower()
        return any(indicator in directory_lower for indicator in feature_indicators)
    
    def _extract_feature_name_from_directory(self, directory: str) -> str:
        """Extract feature name from directory path."""
        # Remove common prefixes and suffixes
        name = directory
        
        # Remove common prefixes
        prefixes = ['src/', 'app/', 'components/', 'features/', 'modules/']
        for prefix in prefixes:
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        
        # Remove common suffixes
        suffixes = ['/', '-component', '-module', '-feature']
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
                break
        
        # Convert to title case
        return name.replace('-', ' ').replace('_', ' ').title()
    
    def _determine_feature_status(self, feature_data: Dict) -> str:
        """Determine the status of a feature."""
        if feature_data.get('end_date'):
            return 'completed'
        elif feature_data.get('start_date'):
            return 'in_progress'
        else:
            return 'planned'
    
    def _determine_business_value(self, feature_name: str, feature_data: Dict) -> str:
        """Determine the business value of a feature."""
        name_lower = feature_name.lower()
        
        # High-value indicators
        high_value_keywords = ['auth', 'payment', 'user', 'core', 'main', 'critical']
        if any(keyword in name_lower for keyword in high_value_keywords):
            return 'High'
        
        # Medium-value indicators
        medium_value_keywords = ['api', 'service', 'component', 'feature']
        if any(keyword in name_lower for keyword in medium_value_keywords):
            return 'Medium'
        
        # Default to medium
        return 'Medium'
    
    def _determine_priority(self, feature_name: str, feature_data: Dict) -> str:
        """Determine the priority of a feature."""
        business_value = self._determine_business_value(feature_name, feature_data)
        
        if business_value == 'High':
            return 'High'
        elif business_value == 'Medium':
            return 'Medium'
        else:
            return 'Low'
    
    def _determine_risk_level(self, feature_data: Dict) -> str:
        """Determine the risk level of a feature."""
        # High risk indicators
        if feature_data.get('lines_changed', 0) > 1000:
            return 'High'
        
        if len(feature_data.get('dependencies', [])) > 5:
            return 'High'
        
        # Medium risk indicators
        if feature_data.get('lines_changed', 0) > 500:
            return 'Medium'
        
        if len(feature_data.get('dependencies', [])) > 2:
            return 'Medium'
        
        return 'Low'
    
    def _calculate_feature_confidence(self, feature_data: Dict) -> float:
        """Calculate confidence level for feature analysis."""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on data quality
        if feature_data.get('commits'):
            confidence += 0.2
        
        if feature_data.get('start_date') and feature_data.get('end_date'):
            confidence += 0.1
        
        if feature_data.get('lines_changed', 0) > 0:
            confidence += 0.1
        
        if feature_data.get('tags'):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _generate_feature_description(self, feature_name: str, feature_data: Dict) -> str:
        """Generate a description for the feature."""
        description_parts = []
        
        # Add feature type
        if feature_data.get('tags'):
            if 'feature' in feature_data['tags']:
                description_parts.append("Feature implementation")
            elif 'bugfix' in feature_data['tags']:
                description_parts.append("Bug fix")
            elif 'refactor' in feature_data['tags']:
                description_parts.append("Code refactoring")
            else:
                description_parts.append("Development work")
        else:
            description_parts.append("Development work")
        
        # Add scope information
        if feature_data.get('lines_changed', 0) > 0:
            description_parts.append(f"affecting {feature_data['lines_changed']} lines of code")
        
        # Add commit information
        if feature_data.get('commits'):
            description_parts.append(f"with {len(feature_data['commits'])} commits")
        
        return " ".join(description_parts)
    
    def _extract_dependencies(self, feature_data: Dict) -> List[str]:
        """Extract dependencies for a feature."""
        dependencies = []
        
        # Look for dependency indicators in tags
        if 'api' in feature_data.get('tags', []):
            dependencies.append('Backend API')
        
        if 'database' in feature_data.get('tags', []):
            dependencies.append('Database')
        
        if 'ui' in feature_data.get('tags', []):
            dependencies.append('UI Components')
        
        return dependencies
    
    def _determine_feature_group(self, feature: Feature) -> str:
        """Determine which group a feature belongs to."""
        name_lower = feature.name.lower()
        
        # Frontend features
        if any(keyword in name_lower for keyword in ['ui', 'component', 'page', 'screen', 'view']):
            return 'User Interface'
        
        # Backend features
        if any(keyword in name_lower for keyword in ['api', 'service', 'controller', 'model']):
            return 'Backend Services'
        
        # Infrastructure features
        if any(keyword in name_lower for keyword in ['config', 'setup', 'deploy', 'docker']):
            return 'Infrastructure'
        
        # Data features
        if any(keyword in name_lower for keyword in ['database', 'data', 'storage', 'cache']):
            return 'Data Management'
        
        # Default group
        return 'Core Features'
    
    def _determine_group_business_impact(self, features: List[Feature]) -> str:
        """Determine the business impact of a feature group."""
        if not features:
            return 'Low'
        
        # Calculate weighted business impact
        impact_scores = {'Critical': 5, 'High': 4, 'Medium': 3, 'Low': 2, 'Minimal': 1}
        
        total_score = sum(impact_scores.get(f.business_value, 3) for f in features)
        average_score = total_score / len(features)
        
        if average_score >= 4.5:
            return 'Critical'
        elif average_score >= 3.5:
            return 'High'
        elif average_score >= 2.5:
            return 'Medium'
        elif average_score >= 1.5:
            return 'Low'
        else:
            return 'Minimal' 