#!/usr/bin/env python3
"""
Example Usage Script

This script demonstrates how to use the Project Analysis Report Generator
programmatically in your own Python code.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import AnalysisConfig
from analyze_project import ProjectAnalyzer


def analyze_single_repository(repo_path: str, output_path: str = None):
    """
    Analyze a single repository and generate a report.
    
    Args:
        repo_path: Path to the Git repository
        output_path: Optional output path for the report
    """
    print(f"Analyzing repository: {repo_path}")
    
    # Initialize configuration
    config = AnalysisConfig()
    
    # Initialize analyzer
    analyzer = ProjectAnalyzer(config)
    
    try:
        # Perform analysis
        report_path = analyzer.analyze_project(repo_path, output_path)
        
        # Save analysis data for inspection
        analyzer.save_analysis_data(report_path)
        
        print(f"Analysis completed! Report: {report_path}")
        return report_path
        
    except Exception as e:
        print(f"Error analyzing repository: {e}")
        return None


def analyze_multiple_repositories(repo_paths: list, output_dir: str = "reports"):
    """
    Analyze multiple repositories and generate reports.
    
    Args:
        repo_paths: List of repository paths
        output_dir: Directory to save reports
    """
    print(f"Analyzing {len(repo_paths)} repositories...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    
    for repo_path in repo_paths:
        repo_name = os.path.basename(repo_path.rstrip('/'))
        output_path = os.path.join(output_dir, f"{repo_name}_analysis.md")
        
        print(f"\n{'='*50}")
        result = analyze_single_repository(repo_path, output_path)
        results.append((repo_path, result))
    
    # Print summary
    print(f"\n{'='*50}")
    print("ANALYSIS SUMMARY")
    print(f"{'='*50}")
    
    successful = 0
    for repo_path, result in results:
        status = "✓ SUCCESS" if result else "✗ FAILED"
        print(f"{status}: {repo_path}")
        if result:
            successful += 1
    
    print(f"\nTotal: {len(results)} repositories")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")


def custom_analysis_example(repo_path: str):
    """
    Example of custom analysis with modified configuration.
    
    Args:
        repo_path: Path to the Git repository
    """
    print("Running custom analysis with modified configuration...")
    
    # Create custom configuration
    config = AnalysisConfig()
    
    # Modify complexity thresholds for your specific project type
    config.complexity.LOW_COMPLEXITY_LOC = 200  # More lenient for large projects
    config.complexity.MEDIUM_COMPLEXITY_LOC = 800
    config.complexity.HIGH_COMPLEXITY_MULTIPLIER = 8.0  # More time for complex features
    
    # Modify Git analysis settings
    config.git.MAX_COMMIT_HISTORY = 15000  # Analyze more commits
    config.git.IGNORE_MERGE_COMMITS = False  # Include merge commits
    
    # Initialize analyzer with custom config
    analyzer = ProjectAnalyzer(config)
    
    try:
        # Perform analysis
        report_path = analyzer.analyze_project(repo_path)
        
        # Save analysis data
        analyzer.save_analysis_data(report_path)
        
        print(f"Custom analysis completed! Report: {report_path}")
        return report_path
        
    except Exception as e:
        print(f"Error in custom analysis: {e}")
        return None


def main():
    """Main example function."""
    print("Project Analysis Report Generator - Example Usage")
    print("=" * 60)
    
    # Example 1: Analyze a single repository
    print("\n1. Single Repository Analysis")
    print("-" * 30)
    
    # Replace with your repository path
    repo_path = "/path/to/your/repository"
    
    if os.path.exists(repo_path):
        analyze_single_repository(repo_path)
    else:
        print(f"Repository not found: {repo_path}")
        print("Please update the repo_path variable with a valid repository path")
    
    # Example 2: Analyze multiple repositories
    print("\n2. Multiple Repository Analysis")
    print("-" * 30)
    
    # Replace with your repository paths
    repo_paths = [
        "/path/to/repo1",
        "/path/to/repo2",
        "/path/to/repo3"
    ]
    
    # Filter to existing repositories
    existing_repos = [p for p in repo_paths if os.path.exists(p)]
    
    if existing_repos:
        analyze_multiple_repositories(existing_repos)
    else:
        print("No existing repositories found in repo_paths list")
        print("Please update the repo_paths variable with valid repository paths")
    
    # Example 3: Custom analysis
    print("\n3. Custom Analysis Example")
    print("-" * 30)
    
    if os.path.exists(repo_path):
        custom_analysis_example(repo_path)
    else:
        print("Skipping custom analysis - repository not found")
    
    print("\n" + "=" * 60)
    print("Example usage completed!")
    print("\nTo use this system:")
    print("1. Update the repository paths in this script")
    print("2. Run: python example_usage.py")
    print("3. Or use the command line: python analyze_project.py /path/to/repo")


if __name__ == "__main__":
    main() 