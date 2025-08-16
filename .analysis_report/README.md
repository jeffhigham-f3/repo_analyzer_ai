# Project Analysis Report Generator

A comprehensive Python package for analyzing Git repositories and generating stakeholder-focused project analysis reports.

## Overview

This tool provides automated analysis of software projects by examining:
- Repository structure and technology stack
- Git commit history and patterns
- Feature identification and complexity assessment
- Developer contributions and skill analysis
- Risk assessment and mitigation strategies
- Project health and quality metrics

The generated reports are organized by stakeholder hierarchy, providing appropriate detail levels for executives, managers, technical leads, and developers.

## Features

### 🔍 **Repository Analysis**
- Automatic technology stack identification
- Project structure mapping
- Architecture pattern detection
- Configuration file analysis

### 📊 **Git History Analysis**
- Commit pattern analysis
- Developer contribution tracking
- Feature timeline mapping
- Code quality assessment

### 🎯 **Feature Mapping**
- Automatic feature identification
- Complexity assessment
- Time estimation
- Business value mapping

### 👥 **Developer Analysis**
- Skill level assessment
- Contribution pattern analysis
- Knowledge concentration calculation
- Team dynamics evaluation

### ⚠️ **Risk Assessment**
- Technical debt identification
- Team risk analysis
- Business risk evaluation
- Mitigation strategy generation

### 📋 **Report Generation**
- Stakeholder-focused content
- Executive summary
- Technical details
- Actionable recommendations

## Installation

### Prerequisites
- Python 3.7+
- Git repository access
- Read permissions for the target repository

### Setup
1. Clone or download this package
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage
```bash
python analyze_project.py /path/to/your/repository
```

### Advanced Usage
```bash
python analyze_project.py /path/to/repository \
    --output custom_report.md \
    --config custom_config.yaml \
    --save-data
```

### Command Line Options
- `repo_path`: Path to the Git repository to analyze
- `-o, --output`: Custom output path for the report
- `-c, --config`: Path to custom configuration file
- `--save-data`: Save analysis data to JSON file for inspection

## Configuration

The system uses a comprehensive configuration system that can be customized for different project types and requirements.

### Default Configuration
The system comes with sensible defaults for:
- Complexity thresholds
- Time estimation multipliers
- Technology stack patterns
- Risk assessment criteria

### Custom Configuration
Create a custom configuration file to override defaults:
```yaml
complexity:
  LOW_COMPLEXITY_LOC: 150
  MEDIUM_COMPLEXITY_LOC: 600
  HIGH_COMPLEXITY_MULTIPLIER: 7.0

git:
  MAX_COMMIT_HISTORY: 5000
  IGNORE_MERGE_COMMITS: true

report:
  INCLUDE_EXECUTIVE_SUMMARY: true
  INCLUDE_FEATURE_ANALYSIS: true
  INCLUDE_DEVELOPER_ANALYSIS: true
```

## Output

### Report Structure
The generated report follows a stakeholder hierarchy:

1. **Executive Level** (C-Suite, Stakeholders)
   - Executive Summary
   - Project Overview
   - Key Metrics & ROI

2. **Management Level** (Product/Project Managers)
   - Feature Analysis
   - Development Timeline
   - Resource Allocation
   - Risk Assessment

3. **Technical Leadership Level** (Tech Leads, Architects)
   - Technical Architecture
   - Development Patterns & Insights
   - Code Quality & Health

4. **Developer Level** (Engineers, Dev Teams)
   - Developer Analysis
   - Feature Complexity Analysis
   - Technical Implementation Details

### Sample Output
```
PROJECT_ANALYSIS_REPORT.md
├── Executive Summary
├── Project Overview
├── Key Metrics & ROI
├── Feature Analysis
├── Development Timeline
├── Resource Allocation
├── Risk Assessment
├── Technical Architecture
├── Development Patterns & Insights
├── Code Quality & Health
├── Developer Analysis
├── Feature Complexity Analysis
├── Technical Implementation Details
├── Methodology & Validation
├── Recommendations
└── Appendix
```

## Architecture

### Core Modules
- **`config.py`**: Configuration management and settings
- **`repo_analyzer.py`**: Repository structure analysis
- **`git_analyzer.py`**: Git history and commit analysis
- **`feature_mapper.py`**: Feature identification and mapping
- **`developer_analyzer.py`**: Developer analysis and team dynamics
- **`risk_assessor.py`**: Risk identification and assessment
- **`report_generator.py`**: Report generation and template population
- **`analyze_project.py`**: Main orchestration script

### Data Flow
```
Repository → Structure Analysis → Git Analysis → Feature Mapping
     ↓              ↓              ↓              ↓
Developer Analysis → Risk Assessment → Report Generation → Final Report
```

## Customization

### Adding New Analysis Types
1. Create a new analysis module
2. Extend the configuration classes
3. Integrate with the main analyzer
4. Update the report generator

### Custom Report Templates
1. Create a new template file
2. Update the report generator
3. Add new placeholder replacement logic

### Custom Metrics
1. Extend the configuration classes
2. Add calculation logic to analysis modules
3. Update the report generation

## Examples

### Analyzing a React Project
```bash
python analyze_project.py /path/to/react-app --save-data
```

### Analyzing a Python Backend
```bash
python analyze_project.py /path/to/python-api \
    --output backend_analysis.md \
    --config python_backend_config.yaml
```

### Batch Analysis
```bash
for repo in /path/to/repos/*; do
    python analyze_project.py "$repo" \
        --output "$(basename "$repo")_analysis.md"
done
```

## Troubleshooting

### Common Issues

#### Git Repository Not Found
```
Error: Path is not a Git repository
```
**Solution**: Ensure the path contains a `.git` directory

#### Permission Denied
```
Error: Permission denied accessing repository
```
**Solution**: Check read permissions for the repository directory

#### Missing Dependencies
```
ModuleNotFoundError: No module named 'yaml'
```
**Solution**: Install required dependencies with `pip install -r requirements.txt`

#### Large Repository Timeout
```
Error: Git log command timed out
```
**Solution**: The system has a 5-minute timeout for large repositories. This is usually sufficient for most projects.

### Performance Tips
- For very large repositories (>10,000 commits), consider analyzing recent history only
- Use `--save-data` flag to inspect analysis results and debug issues
- Customize configuration for your specific project type

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make your changes
5. Add tests
6. Submit a pull request

### Testing
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add comprehensive docstrings
- Include error handling

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

### Documentation
- This README
- Inline code documentation
- Configuration examples

### Issues
- Check the troubleshooting section
- Review error messages carefully
- Use `--save-data` flag to inspect analysis data

### Community
- Submit issues for bugs
- Request features
- Contribute improvements

## Roadmap

### Planned Features
- [ ] Enhanced visualization capabilities
- [ ] Integration with project management tools
- [ ] Custom metric definitions
- [ ] Multi-repository analysis
- [ ] Historical trend analysis
- [ ] Export to multiple formats (PDF, HTML, etc.)

### Version History
- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Enhanced configuration system
- **v1.2.0**: Improved risk assessment
- **v1.3.0**: Stakeholder-focused reporting

## Acknowledgments

- Built with modern Python best practices
- Inspired by industry-standard project analysis methodologies
- Designed for real-world development team needs 