#!/usr/bin/env python3
"""
Main Project Analysis Script

This script orchestrates the complete project analysis process,
coordinating all analysis modules and generating the final report.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
import json

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import AnalysisConfig
from repo_analyzer import RepositoryAnalyzer
from git_analyzer import GitAnalyzer
from feature_mapper import FeatureMapper
from developer_analyzer import DeveloperAnalyzer
from risk_assessor import RiskAssessor
from report_generator import ReportGenerator


class ProjectAnalyzer:
    """Main orchestrator for project analysis."""
    
    def __init__(self, config: AnalysisConfig):
        """
        Initialize the project analyzer.
        
        Args:
            config: Analysis configuration
        """
        self.config = config
        self.repo_analyzer = RepositoryAnalyzer(config)
        self.git_analyzer = GitAnalyzer(config)
        self.feature_mapper = FeatureMapper(config)
        self.developer_analyzer = DeveloperAnalyzer(config)
        self.risk_assessor = RiskAssessor(config)
        self.report_generator = ReportGenerator(config)
        
        # Analysis results storage
        self.analysis_data = {}
        
    def analyze_project(self, repo_path: str, output_path: str = None) -> str:
        """
        Perform complete project analysis.
        
        Args:
            repo_path: Path to the repository to analyze
            output_path: Optional output path for the report
            
        Returns:
            Path to the generated report
        """
        print(f"Starting analysis of repository: {repo_path}")
        print("=" * 60)
        
        try:
            # Step 1: Repository Structure Analysis
            print("1. Analyzing repository structure...")
            repo_structure = self.repo_analyzer.analyze_repository(repo_path)
            self.analysis_data['repo_structure'] = self._convert_to_dict(repo_structure)
            print(f"   ✓ Found {repo_structure.total_files} files, {repo_structure.total_lines} lines of code")
            print(f"   ✓ Identified {len(repo_structure.technology_stack)} technologies")
            
            # Step 2: Git History Analysis
            print("2. Analyzing Git history...")
            commits, commit_patterns = self.git_analyzer.analyze_git_history(repo_path)
            self.analysis_data['commits'] = [self._convert_to_dict(c) for c in commits]
            self.analysis_data['commit_patterns'] = self._convert_to_dict(commit_patterns)
            print(f"   ✓ Analyzed {len(commits)} commits")
            print(f"   ✓ Identified {commit_patterns.feature_commits} feature commits")
            
            # Step 3: Developer Analysis
            print("3. Analyzing developer contributions...")
            author_stats = self.git_analyzer.analyze_developers(commits)
            developer_profiles = self.developer_analyzer.analyze_developers(commits, author_stats)
            self.analysis_data['author_stats'] = [self._convert_to_dict(a) for a in author_stats]
            self.analysis_data['developer_profiles'] = [self._convert_to_dict(d) for d in developer_profiles]
            print(f"   ✓ Analyzed {len(developer_profiles)} developers")
            
            # Step 4: Feature Analysis
            print("4. Mapping and analyzing features...")
            features = self.feature_mapper.identify_features(commits, self.analysis_data['repo_structure'])
            self.analysis_data['features'] = [self._convert_to_dict(f) for f in features]
            print(f"   ✓ Identified {len(features)} features")
            
            # Step 5: Risk Assessment
            print("5. Assessing project risks...")
            risk_assessment = self.risk_assessor.assess_project_risks(
                commits, features, developer_profiles, self.analysis_data['repo_structure']
            )
            self.analysis_data['risk_assessment'] = self._convert_to_dict(risk_assessment)
            print(f"   ✓ Identified {risk_assessment.total_risks} risks")
            
            # Step 6: Additional Analysis
            print("6. Performing additional analysis...")
            self._perform_additional_analysis()
            
            # Step 7: Generate Report
            print("7. Generating analysis report...")
            if output_path is None:
                output_path = self.config.report.OUTPUT_FILE
            
            report_path = self.report_generator.generate_report(self.analysis_data, output_path)
            
            print("=" * 60)
            print(f"Analysis completed successfully!")
            print(f"Report generated: {report_path}")
            
            return report_path
            
        except Exception as e:
            print(f"Error during analysis: {e}")
            raise
    
    def _perform_additional_analysis(self):
        """Perform additional analysis tasks."""
        # Calculate project metrics
        commits = self.analysis_data.get('commits', [])
        features = self.analysis_data.get('features', [])
        developer_profiles = self.analysis_data.get('developer_profiles', [])
        
        # Project timeline analysis
        if commits:
            dates = [c['date'] for c in commits if 'date' in c]
            if dates:
                # Convert string dates back to datetime for analysis
                from datetime import datetime
                parsed_dates = []
                for date_str in dates:
                    try:
                        if isinstance(date_str, str):
                            parsed_dates.append(datetime.fromisoformat(date_str.replace('Z', '+00:00')))
                        else:
                            parsed_dates.append(date_str)
                    except:
                        continue
                
                if parsed_dates:
                    start_date = min(parsed_dates)
                    end_date = max(parsed_dates)
                    duration = (end_date - start_date).days
                    
                    self.analysis_data['project_timeline'] = {
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat(),
                        'duration_days': duration,
                        'duration_weeks': duration // 7,
                        'duration_months': duration // 30
                    }
        
        # Feature complexity analysis
        if features:
            complexity_counts = {'low': 0, 'medium': 0, 'high': 0}
            total_hours = 0
            
            for feature in features:
                complexity = feature.get('complexity', 'medium')
                complexity_counts[complexity] += 1
                total_hours += feature.get('estimated_hours', 0)
            
            self.analysis_data['feature_complexity'] = {
                'counts': complexity_counts,
                'total_hours': total_hours,
                'average_hours_per_feature': total_hours / len(features) if features else 0
            }
        
        # Team analysis
        if developer_profiles:
            total_contributors = len(developer_profiles)
            primary_contributors = [d for d in developer_profiles if d.get('business_value') in ['Critical', 'High']]
            
            self.analysis_data['team_analysis'] = {
                'total_contributors': total_contributors,
                'primary_contributors': len(primary_contributors),
                'knowledge_concentration': len(primary_contributors) / total_contributors if total_contributors > 0 else 0
            }
        
        # Project health score
        health_score = self._calculate_project_health_score()
        self.analysis_data['project_health'] = {
            'overall_score': health_score,
            'rating': self._get_health_rating(health_score)
        }
    
    def _calculate_project_health_score(self) -> float:
        """Calculate overall project health score."""
        score = 0.0
        factors = 0
        
        # Factor 1: Code quality
        commit_patterns = self.analysis_data.get('commit_patterns', {})
        if commit_patterns and 'commit_message_quality' in commit_patterns:
            score += commit_patterns['commit_message_quality']
            factors += 1
        
        # Factor 2: Feature completion
        features = self.analysis_data.get('features', [])
        if features:
            completed = len([f for f in features if f.get('status') == 'completed'])
            completion_rate = completed / len(features)
            score += completion_rate
            factors += 1
        
        # Factor 3: Risk level
        risk_assessment = self.analysis_data.get('risk_assessment', {})
        if risk_assessment and 'overall_risk_level' in risk_assessment:
            risk_level = risk_assessment['overall_risk_level']
            risk_scores = {'Low': 1.0, 'Medium': 0.6, 'High': 0.2}
            score += risk_scores.get(risk_level, 0.6)
            factors += 1
        
        # Factor 4: Team stability
        team_analysis = self.analysis_data.get('team_analysis', {})
        if team_analysis and 'knowledge_concentration' in team_analysis:
            # Lower concentration is better (more distributed knowledge)
            concentration = team_analysis['knowledge_concentration']
            stability_score = 1.0 - concentration
            score += stability_score
            factors += 1
        
        return score / factors if factors > 0 else 0.5
    
    def _get_health_rating(self, score: float) -> str:
        """Convert health score to rating."""
        if score >= 0.8:
            return "Excellent"
        elif score >= 0.6:
            return "Good"
        elif score >= 0.4:
            return "Fair"
        else:
            return "Poor"
    
    def _convert_to_dict(self, obj):
        """Convert dataclass objects to dictionaries for JSON serialization."""
        if hasattr(obj, '__dict__'):
            result = {}
            for key, value in obj.__dict__.items():
                if hasattr(value, '__dict__'):
                    result[key] = self._convert_to_dict(value)
                elif isinstance(value, (list, tuple)):
                    result[key] = [self._convert_to_dict(item) if hasattr(item, '__dict__') else item for item in value]
                elif isinstance(value, datetime):
                    result[key] = value.isoformat()
                else:
                    result[key] = value
            return result
        else:
            return obj
    
    def save_analysis_data(self, output_path: str):
        """Save analysis data to JSON file for debugging/inspection."""
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        json_path = output_path.replace('.md', '_data.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_data, f, indent=2, ensure_ascii=False)
        
        print(f"Analysis data saved to: {json_path}")


def main():
    """Main entry point for the project analyzer."""
    parser = argparse.ArgumentParser(description='Analyze a Git repository and generate a comprehensive report')
    parser.add_argument('repo_path', help='Path to the Git repository to analyze')
    parser.add_argument('-o', '--output', help='Output path for the report (default: PROJECT_ANALYSIS_REPORT.md)')
    parser.add_argument('-c', '--config', help='Path to configuration file (optional)')
    parser.add_argument('--save-data', action='store_true', help='Save analysis data to JSON file')
    
    args = parser.parse_args()
    
    # Validate repository path
    if not os.path.exists(args.repo_path):
        print(f"Error: Repository path does not exist: {args.repo_path}")
        sys.exit(1)
    
    if not os.path.exists(os.path.join(args.repo_path, '.git')):
        print(f"Error: Path is not a Git repository: {args.repo_path}")
        sys.exit(1)
    
    try:
        # Initialize configuration
        config = AnalysisConfig(args.config)
        
        # Initialize analyzer
        analyzer = ProjectAnalyzer(config)
        
        # Perform analysis
        report_path = analyzer.analyze_project(args.repo_path, args.output)
        
        # Save analysis data if requested
        if args.save_data:
            analyzer.save_analysis_data(report_path)
        
        print(f"\nAnalysis completed successfully!")
        print(f"Report: {report_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 