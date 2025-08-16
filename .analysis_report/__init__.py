"""
Project Analysis Report Generator

A comprehensive Python package for analyzing Git repositories and generating
stakeholder-focused project analysis reports.

This package provides modules for:
- Repository structure analysis
- Git history analysis
- Feature mapping and complexity assessment
- Developer analysis and skill assessment
- Risk assessment and mitigation strategies
- Automated report generation

Author: Project Analysis System
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Project Analysis System"

from .config import AnalysisConfig
from .analyze_project import ProjectAnalyzer

__all__ = [
    "AnalysisConfig",
    "ProjectAnalyzer",
] 