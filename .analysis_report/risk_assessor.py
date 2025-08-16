"""
Risk Assessor Module

This module identifies and analyzes various types of risks in the project,
including technical, team, and business risks.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import math

from .config import AnalysisConfig
from .git_analyzer import CommitInfo, AuthorStats
from .feature_mapper import Feature


@dataclass
class Risk:
    """Represents a project risk."""
    
    id: str
    name: str
    category: str  # 'technical', 'team', 'business'
    probability: str  # 'low', 'medium', 'high'
    impact: str  # 'low', 'medium', 'high'
    business_impact: str
    description: str
    mitigation_strategy: str
    risk_score: float
    detection_date: datetime
    status: str  # 'identified', 'mitigated', 'monitoring', 'resolved'


@dataclass
class RiskAssessment:
    """Overall risk assessment for the project."""
    
    total_risks: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    overall_risk_level: str
    technical_risks: List[Risk]
    team_risks: List[Risk]
    business_risks: List[Risk]
    risk_trend: str
    mitigation_coverage: float


class RiskAssessor:
    """Assesses various types of risks in the project."""
    
    def __init__(self, config: AnalysisConfig):
        """
        Initialize the risk assessor.
        
        Args:
            config: Analysis configuration
        """
        self.config = config
        
    def assess_project_risks(self, commits: List[CommitInfo], 
                            features: List[Feature],
                            developer_profiles: List,
                            repo_structure: Dict) -> RiskAssessment:
        """
        Perform comprehensive risk assessment of the project.
        
        Args:
            commits: List of commit information
            features: List of project features
            developer_profiles: List of developer profiles
            repo_structure: Repository structure information
            
        Returns:
            Comprehensive risk assessment
        """
        # Identify different types of risks
        technical_risks = self._identify_technical_risks(commits, features, repo_structure)
        team_risks = self._identify_team_risks(developer_profiles, commits)
        business_risks = self._identify_business_risks(features, commits)
        
        # Combine all risks
        all_risks = technical_risks + team_risks + business_risks
        
        # Calculate overall risk metrics
        total_risks = len(all_risks)
        high_risk_count = len([r for r in all_risks if r.risk_score >= 0.7])
        medium_risk_count = len([r for r in all_risks if 0.4 <= r.risk_score < 0.7])
        low_risk_count = len([r for r in all_risks if r.risk_score < 0.4])
        
        # Determine overall risk level
        overall_risk_level = self._determine_overall_risk_level(all_risks)
        
        # Analyze risk trend
        risk_trend = self._analyze_risk_trend(commits, all_risks)
        
        # Calculate mitigation coverage
        mitigation_coverage = self._calculate_mitigation_coverage(all_risks)
        
        return RiskAssessment(
            total_risks=total_risks,
            high_risk_count=high_risk_count,
            medium_risk_count=medium_risk_count,
            low_risk_count=low_risk_count,
            overall_risk_level=overall_risk_level,
            technical_risks=technical_risks,
            team_risks=team_risks,
            business_risks=business_risks,
            risk_trend=risk_trend,
            mitigation_coverage=mitigation_coverage
        )
    
    def _identify_technical_risks(self, commits: List[CommitInfo], 
                                 features: List[Feature],
                                 repo_structure: Dict) -> List[Risk]:
        """Identify technical risks in the project."""
        risks = []
        
        # Risk 1: High complexity features
        high_complexity_features = [f for f in features if f.complexity == 'high']
        if high_complexity_features:
            risk_score = min(0.8, len(high_complexity_features) * 0.2)
            risks.append(Risk(
                id="TECH_001",
                name="High Complexity Features",
                category="technical",
                probability="medium",
                impact="high",
                business_impact="Delayed delivery and increased maintenance costs",
                description=f"Project contains {len(high_complexity_features)} high-complexity features that may cause delays and quality issues",
                mitigation_strategy="Break down complex features, increase testing coverage, allocate senior developers",
                risk_score=risk_score,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        # Risk 2: Technical debt
        technical_debt_score = self._assess_technical_debt(commits)
        if technical_debt_score > 0.6:
            risks.append(Risk(
                id="TECH_002",
                name="High Technical Debt",
                category="technical",
                probability="high",
                impact="medium",
                business_impact="Reduced development velocity and increased bug frequency",
                description=f"Technical debt score of {technical_debt_score:.2f} indicates accumulated technical issues",
                mitigation_strategy="Implement refactoring sprints, improve code review process, establish coding standards",
                risk_score=technical_debt_score,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        # Risk 3: Architecture complexity
        arch_complexity = self._assess_architecture_complexity(repo_structure)
        if arch_complexity > 0.7:
            risks.append(Risk(
                id="TECH_003",
                name="Complex Architecture",
                category="technical",
                probability="medium",
                impact="high",
                business_impact="Difficult maintenance and onboarding challenges",
                description="Project architecture shows high complexity that may impact maintainability",
                mitigation_strategy="Document architecture decisions, create onboarding guides, simplify complex components",
                risk_score=arch_complexity,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        # Risk 4: Testing coverage
        testing_coverage = self._assess_testing_coverage(commits, repo_structure)
        if testing_coverage < 0.5:
            risks.append(Risk(
                id="TECH_004",
                name="Low Testing Coverage",
                category="technical",
                probability="high",
                impact="medium",
                business_impact="Increased bug frequency and deployment risks",
                description=f"Testing coverage of {testing_coverage:.2f} indicates insufficient testing",
                mitigation_strategy="Implement automated testing, establish testing requirements, increase test coverage",
                risk_score=1.0 - testing_coverage,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        # Risk 5: Dependency risks
        dependency_risks = self._assess_dependency_risks(repo_structure)
        if dependency_risks:
            risks.append(Risk(
                id="TECH_005",
                name="Dependency Vulnerabilities",
                category="technical",
                probability="medium",
                impact="medium",
                business_impact="Security vulnerabilities and maintenance overhead",
                description="Project has potential dependency and security risks",
                mitigation_strategy="Regular dependency updates, security scanning, vulnerability monitoring",
                risk_score=0.6,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        return risks
    
    def _identify_team_risks(self, developer_profiles: List, 
                             commits: List[CommitInfo]) -> List[Risk]:
        """Identify team-related risks."""
        risks = []
        
        if not developer_profiles:
            return risks
        
        # Risk 1: Knowledge concentration
        knowledge_concentration = self._assess_knowledge_concentration(developer_profiles)
        if knowledge_concentration > 0.7:
            risks.append(Risk(
                id="TEAM_001",
                name="High Knowledge Concentration",
                category="team",
                probability="medium",
                impact="high",
                business_impact="Project becomes unmaintainable if key developers leave",
                description=f"Knowledge concentration score of {knowledge_concentration:.2f} indicates over-reliance on few developers",
                mitigation_strategy="Cross-training, documentation, knowledge sharing sessions, pair programming",
                risk_score=knowledge_concentration,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        # Risk 2: Team stability
        team_stability = self._assess_team_stability(developer_profiles, commits)
        if team_stability < 0.5:
            risks.append(Risk(
                id="TEAM_002",
                name="Team Instability",
                category="team",
                probability="high",
                impact="medium",
                business_impact="Reduced productivity and knowledge loss",
                description="Team shows signs of instability with frequent changes",
                mitigation_strategy="Improve retention, establish clear roles, provide growth opportunities",
                risk_score=1.0 - team_stability,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        # Risk 3: Skill gaps
        skill_gaps = self._assess_skill_gaps(developer_profiles)
        if skill_gaps:
            risks.append(Risk(
                id="TEAM_003",
                name="Skill Gaps",
                category="team",
                probability="medium",
                impact="medium",
                business_impact="Reduced development velocity and quality issues",
                description=f"Team has skill gaps in areas: {', '.join(skill_gaps)}",
                mitigation_strategy="Training programs, hiring, knowledge transfer, external consultants",
                risk_score=0.6,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        # Risk 4: Communication issues
        communication_score = self._assess_communication_quality(commits)
        if communication_score < 0.6:
            risks.append(Risk(
                id="TEAM_004",
                name="Communication Issues",
                category="team",
                probability="medium",
                impact="medium",
                business_impact="Misunderstandings and coordination problems",
                description="Commit messages and communication patterns indicate potential communication issues",
                mitigation_strategy="Improve documentation, establish communication protocols, regular team meetings",
                risk_score=1.0 - communication_score,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        return risks
    
    def _identify_business_risks(self, features: List[Feature], 
                                commits: List[CommitInfo]) -> List[Risk]:
        """Identify business-related risks."""
        risks = []
        
        # Risk 1: Feature scope creep
        scope_creep_score = self._assess_scope_creep(features, commits)
        if scope_creep_score > 0.6:
            risks.append(Risk(
                id="BUS_001",
                name="Scope Creep",
                category="business",
                probability="medium",
                impact="high",
                business_impact="Delayed delivery and increased costs",
                description="Project shows signs of scope creep with expanding feature set",
                mitigation_strategy="Strict change control, regular scope reviews, stakeholder alignment",
                risk_score=scope_creep_score,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        # Risk 2: Timeline risks
        timeline_risk = self._assess_timeline_risks(features, commits)
        if timeline_risk > 0.7:
            risks.append(Risk(
                id="BUS_002",
                name="Timeline Risks",
                category="business",
                probability="high",
                impact="high",
                business_impact="Missed deadlines and stakeholder dissatisfaction",
                description="Project timeline shows significant risks of delays",
                mitigation_strategy="Resource reallocation, scope reduction, stakeholder communication",
                risk_score=timeline_risk,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        # Risk 3: Resource constraints
        resource_risk = self._assess_resource_constraints(commits, features)
        if resource_risk > 0.6:
            risks.append(Risk(
                id="BUS_003",
                name="Resource Constraints",
                category="business",
                probability="medium",
                impact="medium",
                business_impact="Reduced development velocity and quality",
                description="Project may face resource constraints affecting delivery",
                mitigation_strategy="Resource planning, prioritization, external support",
                risk_score=resource_risk,
                detection_date=datetime.now(),
                status="identified"
            ))
        
        return risks
    
    def _assess_technical_debt(self, commits: List[CommitInfo]) -> float:
        """Assess technical debt based on commit patterns."""
        if not commits:
            return 0.0
        
        debt_indicators = 0
        total_commits = len(commits)
        
        # Look for technical debt indicators
        for commit in commits:
            message_lower = commit.message.lower()
            
            # Refactoring commits indicate technical debt
            if any(word in message_lower for word in ['refactor', 'cleanup', 'technical debt', 'legacy']):
                debt_indicators += 1
            
            # Large commits often indicate accumulated issues
            if commit.lines_added + commit.lines_deleted > 500:
                debt_indicators += 0.5
            
            # Bug fixes indicate existing issues
            if any(word in message_lower for word in ['fix', 'bug', 'patch', 'hotfix']):
                debt_indicators += 0.3
        
        # Calculate technical debt score
        debt_score = min(1.0, debt_indicators / max(total_commits * 0.3, 1))
        return debt_score
    
    def _assess_architecture_complexity(self, repo_structure: Dict) -> float:
        """Assess architecture complexity based on repository structure."""
        complexity_score = 0.0
        
        # Directory depth complexity
        directories = repo_structure.get('directories', [])
        max_depth = max(len(d.split('/')) for d in directories) if directories else 1
        
        if max_depth > 5:
            complexity_score += 0.4
        elif max_depth > 3:
            complexity_score += 0.2
        
        # Technology stack complexity
        tech_stack = repo_structure.get('technology_stack', [])
        if len(tech_stack) > 5:
            complexity_score += 0.3
        elif len(tech_stack) > 3:
            complexity_score += 0.2
        
        # File type diversity
        file_types = repo_structure.get('file_types', {})
        if len(file_types) > 10:
            complexity_score += 0.3
        elif len(file_types) > 5:
            complexity_score += 0.2
        
        return min(complexity_score, 1.0)
    
    def _assess_testing_coverage(self, commits: List[CommitInfo], 
                                repo_structure: Dict) -> float:
        """Assess testing coverage based on available data."""
        if not commits:
            return 0.0
        
        # Count test-related commits
        test_commits = 0
        for commit in commits:
            message_lower = commit.message.lower()
            if any(word in message_lower for word in ['test', 'testing', 'spec', 'unit', 'integration']):
                test_commits += 1
        
        # Calculate testing coverage ratio
        total_commits = len(commits)
        test_coverage = test_commits / total_commits if total_commits > 0 else 0
        
        # Normalize to 0-1 scale
        return min(test_coverage * 3, 1.0)  # Assume 33% test commits is good coverage
    
    def _assess_dependency_risks(self, repo_structure: Dict) -> bool:
        """Assess dependency-related risks."""
        # This is a simplified assessment
        # In practice, you'd analyze package.json, requirements.txt, etc.
        return False  # Placeholder
    
    def _assess_knowledge_concentration(self, developer_profiles: List) -> float:
        """Assess knowledge concentration in the team."""
        if not developer_profiles:
            return 0.0
        
        # Calculate based on contribution distribution
        total_contributors = len(developer_profiles)
        primary_contributors = [p for p in developer_profiles if p.business_value in ['Critical', 'High']]
        
        concentration_ratio = len(primary_contributors) / total_contributors
        return concentration_ratio
    
    def _assess_team_stability(self, developer_profiles: List, 
                              commits: List[CommitInfo]) -> float:
        """Assess team stability."""
        if not developer_profiles or not commits:
            return 0.0
        
        # Analyze recent activity
        recent_cutoff = datetime.now() - timedelta(days=30)
        recent_commits = [c for c in commits if c.date > recent_cutoff]
        
        if not recent_commits:
            return 0.0
        
        # Count active developers in recent period
        recent_authors = set(c.author for c in recent_commits)
        total_developers = len(developer_profiles)
        active_ratio = len(recent_authors) / total_developers
        
        return active_ratio
    
    def _assess_skill_gaps(self, developer_profiles: List) -> List[str]:
        """Assess skill gaps in the team."""
        # This is a simplified assessment
        # In practice, you'd analyze specific technology requirements vs. team skills
        return []  # Placeholder
    
    def _assess_communication_quality(self, commits: List[CommitInfo]) -> float:
        """Assess communication quality based on commit messages."""
        if not commits:
            return 0.0
        
        quality_scores = []
        
        for commit in commits:
            score = 0.5  # Base score
            message = commit.message.strip()
            
            # Length check
            if len(message) >= 15:
                score += 0.2
            
            # Format check
            if any(pattern in message.lower() for pattern in ['feat:', 'fix:', 'docs:', 'refactor:']):
                score += 0.3
            
            quality_scores.append(score)
        
        return sum(quality_scores) / len(quality_scores)
    
    def _assess_scope_creep(self, features: List[Feature], 
                           commits: List[CommitInfo]) -> float:
        """Assess scope creep based on feature evolution."""
        if not features or not commits:
            return 0.0
        
        # Analyze feature growth over time
        # This is a simplified assessment
        return 0.3  # Placeholder
    
    def _assess_timeline_risks(self, features: List[Feature], 
                              commits: List[CommitInfo]) -> float:
        """Assess timeline risks."""
        if not features:
            return 0.0
        
        # Analyze feature complexity and estimated time
        high_complexity_features = [f for f in features if f.complexity == 'high']
        total_features = len(features)
        
        if total_features == 0:
            return 0.0
        
        # Calculate risk based on high complexity features
        complexity_risk = len(high_complexity_features) / total_features
        
        # Additional risk factors
        additional_risk = 0.0
        
        # Features with high risk levels
        high_risk_features = [f for f in features if f.risk_level == 'High']
        if high_risk_features:
            additional_risk += 0.2
        
        # Features with dependencies
        features_with_deps = [f for f in features if f.dependencies]
        if features_with_deps:
            additional_risk += 0.1
        
        return min(complexity_risk + additional_risk, 1.0)
    
    def _assess_resource_constraints(self, commits: List[CommitInfo], 
                                   features: List[Feature]) -> float:
        """Assess resource constraints."""
        if not commits or not features:
            return 0.0
        
        # Analyze commit frequency and feature complexity
        # This is a simplified assessment
        return 0.4  # Placeholder
    
    def _determine_overall_risk_level(self, risks: List[Risk]) -> str:
        """Determine the overall risk level for the project."""
        if not risks:
            return "Low"
        
        # Calculate average risk score
        avg_risk_score = sum(r.risk_score for r in risks) / len(risks)
        
        if avg_risk_score >= 0.7:
            return "High"
        elif avg_risk_score >= 0.4:
            return "Medium"
        else:
            return "Low"
    
    def _analyze_risk_trend(self, commits: List[CommitInfo], 
                           risks: List[Risk]) -> str:
        """Analyze the trend of risks over time."""
        if not commits or not risks:
            return "Unknown"
        
        # This is a simplified analysis
        # In practice, you'd track risk evolution over time
        return "Stable"  # Placeholder
    
    def _calculate_mitigation_coverage(self, risks: List[Risk]) -> float:
        """Calculate the coverage of risk mitigation strategies."""
        if not risks:
            return 1.0
        
        # Count risks with mitigation strategies
        risks_with_mitigation = sum(1 for r in risks if r.mitigation_strategy)
        
        return risks_with_mitigation / len(risks) 