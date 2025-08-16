"""
Configuration module for project analysis parameters and settings.

This module centralizes all configuration options for the analysis system,
including complexity thresholds, time estimates, and analysis parameters.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path


@dataclass
class ComplexityThresholds:
    """Thresholds for feature complexity categorization."""
    
    # Lines of code thresholds
    LOW_COMPLEXITY_LOC: int = 100
    MEDIUM_COMPLEXITY_LOC: int = 500
    
    # Commit count thresholds
    LOW_COMPLEXITY_COMMITS: int = 3
    MEDIUM_COMPLEXITY_COMMITS: int = 8
    
    # Time estimate multipliers (hours per commit)
    LOW_COMPLEXITY_MULTIPLIER: float = 1.5
    MEDIUM_COMPLEXITY_MULTIPLIER: float = 3.0
    HIGH_COMPLEXITY_MULTIPLIER: float = 6.0
    
    # Buffer percentages for estimates
    TESTING_BUFFER: float = 0.15
    DOCUMENTATION_BUFFER: float = 0.05
    TOTAL_BUFFER: float = 0.20


@dataclass
class GitAnalysisConfig:
    """Configuration for Git history analysis."""
    
    # Commit message patterns
    FEATURE_PATTERNS: List[str] = None
    BUG_FIX_PATTERNS: List[str] = None
    REFACTOR_PATTERNS: List[str] = None
    DOCUMENTATION_PATTERNS: List[str] = None
    
    # Analysis parameters
    MAX_COMMIT_HISTORY: int = 10000
    MIN_COMMIT_LENGTH: int = 10
    IGNORE_MERGE_COMMITS: bool = True
    
    def __post_init__(self):
        if self.FEATURE_PATTERNS is None:
            self.FEATURE_PATTERNS = [
                "feat:", "feature:", "add:", "implement:",
                "new:", "create:", "build:"
            ]
        if self.BUG_FIX_PATTERNS is None:
            self.BUG_FIX_PATTERNS = [
                "fix:", "bugfix:", "bug:", "resolve:",
                "patch:", "correct:"
            ]
        if self.REFACTOR_PATTERNS is None:
            self.REFACTOR_PATTERNS = [
                "refactor:", "refactor:", "cleanup:",
                "restructure:", "optimize:"
            ]
        if self.DOCUMENTATION_PATTERNS is None:
            self.DOCUMENTATION_PATTERNS = [
                "docs:", "documentation:", "readme:",
                "comment:", "update docs:"
            ]


@dataclass
class TechnologyStackConfig:
    """Configuration for technology stack identification."""
    
    # File extensions and patterns for different technologies
    FRONTEND_TECH: Dict[str, List[str]] = None
    BACKEND_TECH: Dict[str, List[str]] = None
    BUILD_TOOLS: Dict[str, List[str]] = None
    TESTING_TOOLS: Dict[str, List[str]] = None
    
    # Configuration files to analyze
    CONFIG_FILES: List[str] = None
    
    def __post_init__(self):
        if self.FRONTEND_TECH is None:
            self.FRONTEND_TECH = {
                "React": ["*.jsx", "*.tsx", "react", "next.js"],
                "Vue": ["*.vue", "vue", "nuxt"],
                "Angular": ["*.ts", "angular", "ng-"],
                "HTML/CSS": ["*.html", "*.css", "*.scss", "*.sass"]
            }
        if self.BACKEND_TECH is None:
            self.BACKEND_TECH = {
                "Node.js": ["package.json", "*.js", "express", "koa"],
                "Python": ["*.py", "requirements.txt", "pyproject.toml"],
                "Java": ["*.java", "pom.xml", "build.gradle"],
                "Go": ["*.go", "go.mod", "go.sum"]
            }
        if self.BUILD_TOOLS is None:
            self.BUILD_TOOLS = {
                "Webpack": ["webpack.config.js", "webpack"],
                "Vite": ["vite.config.js", "vite"],
                "Rollup": ["rollup.config.js", "rollup"],
                "Make": ["Makefile", "makefile"]
            }
        if self.TESTING_TOOLS is None:
            self.TESTING_TOOLS = {
                "Jest": ["jest.config.js", "jest"],
                "Mocha": ["mocha", "*.test.js"],
                "Pytest": ["pytest.ini", "conftest.py"],
                "JUnit": ["junit", "test"]
            }
        if self.CONFIG_FILES is None:
            self.CONFIG_FILES = [
                "package.json", "requirements.txt", "pom.xml",
                "build.gradle", "go.mod", "Cargo.toml",
                "docker-compose.yml", "Dockerfile",
                ".gitignore", "README.md", "CHANGELOG.md"
            ]


@dataclass
class ReportConfig:
    """Configuration for report generation."""
    
    # Output settings
    OUTPUT_FILE: str = "PROJECT_ANALYSIS_REPORT.md"
    TEMPLATE_FILE: str = "templates/project_analysis.template.md"
    
    # Report sections to include
    INCLUDE_EXECUTIVE_SUMMARY: bool = True
    INCLUDE_FEATURE_ANALYSIS: bool = True
    INCLUDE_DEVELOPER_ANALYSIS: bool = True
    INCLUDE_TECHNICAL_ARCHITECTURE: bool = True
    INCLUDE_RISK_ASSESSMENT: bool = True
    
    # Confidence thresholds
    HIGH_CONFIDENCE_THRESHOLD: float = 0.8
    MEDIUM_CONFIDENCE_THRESHOLD: float = 0.5
    
    # Business impact categories
    BUSINESS_IMPACT_LEVELS: List[str] = None
    
    def __post_init__(self):
        if self.BUSINESS_IMPACT_LEVELS is None:
            self.BUSINESS_IMPACT_LEVELS = [
                "Critical", "High", "Medium", "Low", "Minimal"
            ]


class AnalysisConfig:
    """Main configuration class for the analysis system."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the analysis configuration.
        
        Args:
            config_path: Optional path to a configuration file
        """
        self.complexity = ComplexityThresholds()
        self.git = GitAnalysisConfig()
        self.tech_stack = TechnologyStackConfig()
        self.report = ReportConfig()
        
        # Load custom configuration if provided
        if config_path and os.path.exists(config_path):
            self._load_config(config_path)
    
    def _load_config(self, config_path: str):
        """Load configuration from a file (placeholder for future implementation)."""
        # TODO: Implement configuration file loading
        pass
    
    def get_complexity_level(self, loc: int, commit_count: int) -> str:
        """
        Determine complexity level based on lines of code and commit count.
        
        Args:
            loc: Lines of code
            commit_count: Number of commits
            
        Returns:
            Complexity level: 'low', 'medium', or 'high'
        """
        if (loc <= self.complexity.LOW_COMPLEXITY_LOC and 
            commit_count <= self.complexity.LOW_COMPLEXITY_COMMITS):
            return "low"
        elif (loc <= self.complexity.MEDIUM_COMPLEXITY_LOC and 
              commit_count <= self.complexity.MEDIUM_COMPLEXITY_COMMITS):
            return "medium"
        else:
            return "high"
    
    def get_time_estimate(self, complexity: str, commit_count: int) -> float:
        """
        Calculate time estimate based on complexity and commit count.
        
        Args:
            complexity: Complexity level
            commit_count: Number of commits
            
        Returns:
            Estimated hours
        """
        multipliers = {
            "low": self.complexity.LOW_COMPLEXITY_MULTIPLIER,
            "medium": self.complexity.MEDIUM_COMPLEXITY_MULTIPLIER,
            "high": self.complexity.HIGH_COMPLEXITY_MULTIPLIER
        }
        
        base_hours = multipliers.get(complexity, 3.0) * commit_count
        total_hours = base_hours * (1 + self.complexity.TOTAL_BUFFER)
        
        return round(total_hours, 1)
    
    def get_confidence_score(self, data_quality: float, sample_size: int) -> float:
        """
        Calculate confidence score based on data quality and sample size.
        
        Args:
            data_quality: Data quality score (0-1)
            sample_size: Number of data points
            
        Returns:
            Confidence score (0-1)
        """
        # Base confidence on data quality
        confidence = data_quality
        
        # Adjust based on sample size
        if sample_size >= 100:
            confidence *= 1.0
        elif sample_size >= 50:
            confidence *= 0.9
        elif sample_size >= 20:
            confidence *= 0.8
        elif sample_size >= 10:
            confidence *= 0.7
        else:
            confidence *= 0.5
        
        return min(confidence, 1.0) 