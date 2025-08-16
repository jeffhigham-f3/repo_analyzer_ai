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

1. Analyze your current project
2. Generate a comprehensive report

### For Manual Use

```bash
# Clone the repository
git clone https://github.com/jeffhigham-f3/repo_analyzer_ai.git
cd repo_analyzer_ai


## 📁 Repository Structure

```
├── AGENT.md
├── .analysis_report/
│   └── prompts/
│       └── project_analysis.prompt.md
│   └── templates/
│       └── project_analysis.template.md
└── README.md
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


## 📝 License

Copyright © 2025 F3 Software

This project is licensed under the Polyform Noncommercial License 1.0.0 - see the [LICENSE](LICENSE.md) file for details.

**Note**: This license allows free use for noncommercial purposes only. Commercial use requires separate licensing.
