# Project Analysis Report Generator

A comprehensive, AI-powered system for generating detailed project analysis reports from any Git repository. This tool provides stakeholder-focused insights into project health, development patterns, team dynamics, and technical architecture.

## 🎯 What It Does

Generate professional project analysis reports that include:

- **Executive Summary** with key business metrics and strategic insights
- **Feature Analysis** with complexity assessment and time estimates
- **Development Timeline** with project phases and milestones
- **Team Analysis** with developer skill assessment and contribution patterns
- **Risk Assessment** covering technical, team, and business risks
- **Technical Architecture** with technology stack and business justification
- **Code Quality Metrics** with health indicators and technical debt analysis

## 🚀 Quick Start

### For Cursor AI Agents

Simply paste the URL to `AGENT.md` in your Cursor chat window. The agent will:

1. Download the complete analysis system
2. Analyze your current project
3. Generate a comprehensive report

### For Manual Use

```bash
# Clone the repository
git clone https://github.com/jeffhigham-f3/repo_analyzer_ai.git
cd repo_analyzer_ai

# Install dependencies
pip install -r .analysis_report/requirements.txt

# Run analysis on a project
python .analysis_report/analyze_project.py /path/to/your/project --save-data
```

## 📁 Repository Structure

```
├── AGENT.md                           # AI Agent launcher instructions
├── prompts/
│   └── project_analysis.prompt.md     # Detailed analysis instructions
├── templates/
│   └── project_analysis.template.md   # Report template
├── .analysis_report/                  # Python analysis system
│   ├── __init__.py
│   ├── config.py                      # Configuration and thresholds
│   ├── repo_analyzer.py               # Repository structure analysis
│   ├── git_analyzer.py                # Git history analysis
│   ├── feature_mapper.py              # Feature identification & mapping
│   ├── developer_analyzer.py          # Developer contribution analysis
│   ├── risk_assessor.py               # Risk identification & assessment
│   ├── report_generator.py            # Report generation & formatting
│   ├── analyze_project.py             # Main orchestration script
│   ├── requirements.txt               # Python dependencies
│   ├── README.md                      # System documentation
│   └── example_usage.py               # Usage examples
└── README.md                          # This file
```

## 🔧 How It Works

### 1. Repository Analysis
- Scans project structure and identifies technology stack
- Analyzes configuration files and architecture patterns
- Maps project organization and dependencies

### 2. Git History Analysis
- Extracts commit statistics and patterns
- Analyzes developer contributions and collaboration
- Identifies feature development timelines
- Calculates project velocity and consistency metrics

### 3. Feature Mapping
- Identifies discrete features from commits and structure
- Assesses complexity using multi-factor analysis
- Estimates development time with industry benchmarks
- Maps business value and priority levels

### 4. Risk Assessment
- Identifies technical debt and architectural concerns
- Assesses team knowledge concentration and bus factor
- Evaluates business and scalability risks
- Provides mitigation strategies

### 5. Report Generation
- Populates stakeholder-focused template
- Organizes content by audience hierarchy
- Includes confidence levels and methodology
- Generates actionable recommendations

## 🎭 Stakeholder-Focused Reporting

### Executive Level (C-Suite, Stakeholders)
- Project health assessment and investment summary
- Key business metrics and ROI analysis
- Strategic insights and recommendations

### Management Level (Product/Project Managers)
- Feature analysis with business priorities
- Development timeline and resource allocation
- Risk assessment and mitigation strategies

### Technical Leadership Level (Tech Leads, Architects)
- Technical architecture with business justification
- Development patterns and code quality metrics
- Performance indicators and scalability analysis

### Developer Level (Engineers, Dev Teams)
- Detailed developer insights and skill assessment
- Feature complexity analysis and technical details
- Code quality indicators and improvement areas

## 🛠️ Configuration

The system uses configurable thresholds and parameters:

```python
# Example configuration
ComplexityThresholds(
    low_max_hours=2,
    medium_max_hours=6,
    high_min_hours=6
)

GitAnalysisConfig(
    commit_patterns=['feat:', 'fix:', 'refactor:'],
    author_patterns=['name <email>'],
    time_estimation_method='commit_count'
)
```

## 📊 Output Example

The system generates a comprehensive markdown report with:

- **Executive Summary** with key metrics and insights
- **Feature Analysis** tables with complexity and time estimates
- **Development Timeline** with phase breakdowns
- **Risk Assessment** with probability and impact ratings
- **Technical Architecture** with technology stack details
- **Developer Analysis** with skill assessments and contributions
- **Recommendations** organized by stakeholder level

## 🔒 Safety Features

- **Read-Only Operations**: Never modifies the analyzed repository
- **Isolated Execution**: All analysis runs in separate `.analysis_report/` directory
- **Dependency Verification**: Checks requirements without installing in target project
- **Confirmation Prompts**: Asks before overwriting existing analysis directories

## 🚨 Requirements

### Python Dependencies
- Python 3.7+
- PyYAML
- pathlib2 (for older Python versions)

### System Requirements
- Git repository access
- Read permissions on target project
- Sufficient disk space for analysis data

## 📈 Use Cases

### Project Management
- **Due Diligence**: Assess codebase health before acquisition
- **Team Planning**: Understand skill distribution and resource needs
- **Timeline Estimation**: Plan feature development and releases
- **Risk Mitigation**: Identify and address technical debt

### Business Intelligence
- **Investment Analysis**: Evaluate development ROI and efficiency
- **Strategic Planning**: Understand technical capabilities and limitations
- **Compliance**: Assess code quality and security posture
- **Vendor Evaluation**: Analyze third-party project health

### Technical Leadership
- **Architecture Review**: Assess system design and scalability
- **Code Quality**: Identify improvement areas and technical debt
- **Team Assessment**: Understand knowledge distribution and bus factor
- **Performance Analysis**: Evaluate development velocity and consistency

## 🔄 Code Evolution Approach

The system is designed to evolve and improve:

1. **Start with Existing Code**: Use proven analysis modules
2. **Discover Limitations**: Identify what existing code can't handle
3. **Plan Improvements**: Determine needed modifications
4. **Implement Changes**: Enhance modules for project-specific needs
5. **Test and Validate**: Verify improvements work correctly
6. **Document Evolution**: Explain what changed and why

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include unit tests for new functionality
- Update documentation for API changes

## 📝 License

Copyright © 2025 F3 Software

This project is licensed under the Polyform Noncommercial License 1.0.0 - see the [LICENSE](LICENSE.md) file for details.

**Note**: This license allows free use for noncommercial purposes only. Commercial use requires separate licensing.

## 🆘 Support

### Common Issues
- **Dependencies Missing**: Install required Python packages
- **Permission Errors**: Ensure read access to target repository
- **Large Repositories**: Analysis may take longer for big projects
- **Template Issues**: Verify template file is properly formatted

### Getting Help
- Check the example usage files
- Review the configuration options
- Examine the generated reports for insights
- Open an issue for bugs or feature requests
- **Repository**: [https://github.com/jeffhigham-f3/repo_analyzer_ai](https://github.com/jeffhigham-f3/repo_analyzer_ai)

## 🗺️ Roadmap

### Planned Features
- **Multi-Repository Analysis**: Compare multiple projects
- **Historical Trend Analysis**: Track project evolution over time
- **Custom Report Templates**: User-defined report formats
- **Integration APIs**: Connect with project management tools
- **Performance Optimization**: Faster analysis for large repositories

### Version History
- **v1.0**: Core analysis capabilities and stakeholder reporting
- **v1.1**: Enhanced risk assessment and developer analysis
- **v1.2**: Code evolution and repository-specific optimization
- **v2.0**: Multi-repository analysis and trend tracking
