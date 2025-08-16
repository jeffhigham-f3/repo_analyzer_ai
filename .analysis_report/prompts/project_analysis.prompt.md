# Project Analysis Report Generator

## Initial Setup Instructions

**IMPORTANT**: This prompt is designed to be executed by an AI agent that can fetch content from URLs.

### **For AI Agents:**
1. **Fetch the Analysis System**: The agent should first fetch the complete project analysis system from the repository
2. **Download Required Files**: Get all necessary Python modules and templates
3. **Execute Analysis**: Run the analysis on the current project using the downloaded system

### **Required Repository Files:**
The agent needs to download these files from the repository:
- `.analysis_report/` directory (all Python modules)
- `templates/project_analysis.template.md`
- This prompt file for reference

## AI Agent Implementation Guide

### **Downloading the Analysis System:**
The agent should download these files from the repository:

```bash
# Example: If the prompt is at:
# https://github.com/jeffhigham-f3/repo_analyzer_ai/blob/main/prompts/project_analysis.prompt.md
# 
# The agent should download:
# https://raw.githubusercontent.com/jeffhigham/repo_analyzer_ai/main/.analysis_report/
# https://raw.githubusercontent.com/jeffhigham/repo_analyzer_ai/main/templates/project_analysis.template.md
```

### **File Structure Required:**
```
.analysis_report/
├── __init__.py
├── config.py
├── repo_analyzer.py
├── git_analyzer.py
├── feature_mapper.py
├── developer_analyzer.py
├── risk_assessor.py
├── report_generator.py
├── analyze_project.py
└── requirements.txt

templates/
└── project_analysis.template.md
```

### **Agent Actions Required:**
1. **Download Files**: Fetch all required files from the repository
2. **Install Dependencies**: Ensure PyYAML and other requirements are available
3. **Execute Analysis**: Run the analysis system on the current project
4. **Generate Report**: Create the comprehensive analysis report

## Repository Access Instructions

### **For AI Agents:**
- **Base Repository**: Extract the base repository URL from this prompt's location
- **File Paths**: Use relative paths from the repository root
- **Raw Content**: Use raw GitHub URLs for file downloads
- **Directory Structure**: Maintain the exact directory structure when downloading

### **Example:**
If this prompt is located at:
`https://github.com/jeffhigham-f3/repo_analyzer_ai/blob/main/prompts/project_analysis.prompt.md`

The agent should download from:
- `https://raw.githubusercontent.com/jeffhigham-f3/repo_analyzer_ai/main/.analysis_report/`
- `https://raw.githubusercontent.com/jeffhigham-f3/repo_analyzer_ai/main/templates/`

## Objective
Generate a comprehensive, consistent project analysis report based on repository structure, git history, and project documentation. This report should provide actionable insights for project planning, team assessment, and technical debt evaluation, organized by stakeholder hierarchy.

## Report Structure & Stakeholder Focus

### Executive Level (C-Suite, Stakeholders)
- **Executive Summary**: Project health, investment summary, strategic insights
- **Project Overview**: Business value, goals, strategic positioning  
- **Key Metrics & ROI**: Investment summary, performance indicators, business impact

### Management Level (Product/Project Managers)
- **Feature Analysis**: Business-focused feature breakdown with priorities and risk levels
- **Development Timeline**: Project phases with business milestones and deliverables
- **Resource Allocation**: Team composition and resource utilization
- **Risk Assessment**: Business, technical, and team risks with mitigation strategies

### Technical Leadership Level (Tech Leads, Architects)
- **Technical Architecture**: Technology stack with business justification
- **Development Patterns & Insights**: Commit analysis with business impact
- **Code Quality & Health**: Quality metrics with business implications

### Developer Level (Engineers, Dev Teams)
- **Developer Analysis**: Detailed developer insights with business value
- **Feature Complexity Analysis**: Technical complexity with business priority
- **Technical Implementation Details**: Deep technical implementation specifics

## Report Requirements

### 1. Feature Inventory & Analysis
- **Feature Definition**: A feature is a discrete unit of functionality that delivers user value or technical capability
- **Identification Method**: 
  - Analyze README.md, CHANGELOG.md, and documentation files
  - Examine directory structure for logical groupings
  - Review commit messages for feature-related keywords
  - Cross-reference with issue/PR labels if available
- **Required Output**: Complete feature list with business value, priorities, complexity ratings, and estimated development time

### 2. Time Estimation Framework
- **Complexity Categories**:
  - **Low**: Simple UI changes, bug fixes, documentation updates (0.5-2 hours per commit)
  - **Medium**: New components, API endpoints, moderate refactoring (2-6 hours per commit)
  - **High**: Complex algorithms, architectural changes, major integrations (6-12+ hours per commit)
- **Estimation Method**: 
  - Count commits per feature
  - Apply complexity multiplier based on feature type
  - Add 20% buffer for testing and documentation
  - Use industry benchmarks for validation

### 3. Development Pattern Analysis
- **Commit Patterns**: Frequency, consistency, and timing analysis with business impact
- **Team Dynamics**: Developer contribution patterns and skill assessment
- **Code Quality Indicators**: Architecture consistency, testing patterns, documentation coverage
- **Project Health Metrics**: Technical debt indicators, maintenance patterns

### 4. Strategic Recommendations
- **Executive Level**: High-level strategic decisions, investment priorities, risk mitigation
- **Management Level**: Process improvements, resource allocation, timeline optimization
- **Technical Level**: Architecture improvements, testing strategies, performance optimizations

## Analysis Methodology

### Phase 1: Data Collection (Read-Only Operations)
1. **Repository Structure Analysis**
   - Scan all directories and files
   - Identify technology stack from configuration files
   - Map project architecture patterns

2. **Git History Analysis**
   - Extract commit statistics (total, frequency, authors)
   - Analyze commit message patterns and categorization
   - Identify feature development timelines
   - Calculate developer contribution metrics

3. **Documentation Review**
   - Parse README.md for feature descriptions
   - Extract version information and changelog data
   - Identify project goals and requirements

### Phase 2: Feature Mapping & Categorization
1. **Feature Identification**
   - Group related commits by topic/component
   - Map features to directory structures
   - Cross-reference with documentation

2. **Complexity Assessment**
   - Evaluate based on: lines of code, commit count, architectural impact
   - Apply industry-standard complexity metrics
   - Validate against similar projects

3. **Time Estimation**
   - Apply complexity-based time multipliers
   - Account for project-specific factors
   - Validate estimates against commit patterns

### Phase 3: Analysis & Insights
1. **Development Pattern Analysis**
   - Team collaboration patterns
   - Code quality indicators
   - Project velocity and consistency

2. **Risk Assessment**
   - Technical debt identification
   - Knowledge concentration risks
   - Scalability concerns

3. **Recommendation Generation**
   - Prioritized improvement suggestions by stakeholder level
   - Resource allocation recommendations
   - Timeline optimization strategies

## Python Analysis Code Requirements

### Code Organization
- **Directory**: Use existing code in `.analysis_report/` directory as a starting point
- **Modular Structure**: Maintain separate modules for different analysis types
- **Configuration**: Use centralized configuration for analysis parameters
- **Output Generation**: Automated report generation from analysis results

### Required Python Modules

#### 1. **Repository Analyzer** (`.analysis_report/repo_analyzer.py`)
- Project structure scanning
- Technology stack identification
- Configuration file parsing
- Architecture pattern detection

#### 2. **Git History Analyzer** (`.analysis_report/git_analyzer.py`)
- Commit statistics extraction
- Author contribution analysis
- Feature timeline mapping
- Commit pattern categorization

#### 3. **Feature Mapper** (`.analysis_report/feature_mapper.py`)
- Feature identification logic
- Complexity assessment algorithms
- Time estimation calculations
- Business value mapping

#### 4. **Developer Analyzer** (`.analysis_report/developer_analyzer.py`)
- Developer skill assessment
- Contribution pattern analysis
- Knowledge concentration calculation
- Team dynamics evaluation

#### 5. **Risk Assessor** (`.analysis_report/risk_assessor.py`)
- Technical debt identification
- Risk probability calculation
- Mitigation strategy generation
- Business impact assessment

#### 6. **Report Generator** (`.analysis_report/report_generator.py`)
- Template population
- Data formatting and validation
- Stakeholder-specific content generation
- Output file creation

#### 7. **Main Analysis Script** (`.analysis_report/analyze_project.py`)
- Orchestrates all analysis modules
- Manages data flow between components
- Handles error cases and validation
- Generates final report

### Code Quality Requirements
- **Error Handling**: Graceful handling of missing data and edge cases
- **Validation**: Data consistency checks and confidence scoring
- **Documentation**: Clear docstrings and inline comments
- **Testing**: Unit tests for critical analysis functions
- **Configuration**: Environment-specific settings and parameters

### Code Modification Guidelines
**When to Modify Existing Code:**
- Repository has unique characteristics not covered by existing analyzers
- Performance issues with large repositories
- Missing technology stack or architecture patterns
- Repository-specific commit patterns or workflows
- Specialized file types or project structures

**How to Modify Code:**
- Preserve the existing module structure and interfaces
- Add new methods rather than completely rewriting existing ones
- Document all changes and their rationale
- Test modifications with the specific repository
- Maintain backward compatibility where possible

**Modification Examples:**
- Add new technology stack detectors for specific frameworks
- Enhance feature mapping for repository-specific patterns
- Optimize Git analysis for large commit histories
- Add repository-specific risk assessment criteria
- Customize complexity thresholds for project type

### Data Processing Requirements
- **Git Data**: Efficient parsing of large git histories
- **File Analysis**: Fast directory traversal and file parsing
- **Data Aggregation**: Efficient grouping and calculation of metrics
- **Output Generation**: Fast report generation with proper formatting

## Output Requirements

### Report Structure
- Use the provided stakeholder-focused template with all placeholders populated
- Ensure consistent formatting and data presentation
- Include data validation and confidence indicators
- Provide clear methodology documentation
- Maintain stakeholder hierarchy throughout

### Data Quality Standards
- **Accuracy**: All metrics must be verifiable from source data
- **Consistency**: Similar projects should produce comparable results
- **Completeness**: All required sections must be populated
- **Actionability**: Recommendations must be specific and implementable
- **Business Context**: All technical metrics must include business impact

### Validation Steps
1. **Data Cross-Reference**: Ensure git data matches file structure analysis
2. **Estimate Validation**: Compare time estimates with industry benchmarks
3. **Consistency Check**: Verify feature categorization is logical and consistent
4. **Completeness Review**: Ensure all template sections are properly populated
5. **Business Impact Validation**: Verify all metrics include business context

## Safety & Constraints

### Read-Only Operations Only
- **Git Commands**: Only use `git log`, `git show`, `git diff` for analysis
- **File Operations**: Read and analyze files only, no modifications
- **Repository State**: Maintain current working directory and branch

### Error Handling
- **Missing Data**: Clearly indicate when information is unavailable
- **Uncertainty**: Provide confidence levels for estimates and analysis
- **Fallbacks**: Use reasonable defaults when specific data is missing

### File Management
- **Output Location**: Save as `PROJECT_ANALYSIS_REPORT.md` in project root
- **Code Location**: Place all analysis code in `.analysis_report/` directory
- **Existing Files**: Prompt for confirmation before overwriting
- **Backup**: Suggest backup creation for existing reports

## Execution Instructions for AI Agents

### **Phase 0: System Setup**
1. **Fetch Analysis System**: Download the complete `.analysis_report/` directory from the repository
2. **Verify Dependencies**: Ensure required Python packages are available
3. **Prepare Environment**: Set up the analysis system in the current project

### **Phase 1: Initial Analysis**
4. **Use Existing Code**: Run initial analysis with downloaded modules
5. **Identify Enhancement Needs**: Determine what code modifications are needed

### **Phase 2: Code Adaptation**
6. **Modify Code**: Enhance modules based on repository-specific requirements
7. **Execute Enhanced Analysis**: Run improved analysis for comprehensive results

### **Phase 3: Report Generation**
8. **Generate Report**: Create stakeholder-focused analysis report
9. **Validate Output**: Ensure quality standards are met
10. **Save Report**: Create final `PROJECT_ANALYSIS_REPORT.md`

### **Code Evolution Workflow**:
1. **Start with Existing Code**: Use downloaded modules for initial analysis
2. **Discover Limitations**: Identify what the existing code can't handle well
3. **Plan Improvements**: Determine what modifications are needed
4. **Implement Changes**: Modify code while maintaining structure
5. **Test Modifications**: Verify changes work with the specific repository
6. **Document Changes**: Explain what was modified and why

## Success Criteria

- **Consistency**: Similar repositories produce comparable analysis results
- **Accuracy**: Time estimates align with industry benchmarks
- **Completeness**: All template sections are properly populated
- **Actionability**: Recommendations are specific and implementable by stakeholder level
- **Reproducibility**: Analysis can be re-run with consistent results
- **Business Context**: All technical insights include business impact and value
- **Stakeholder Alignment**: Content is appropriately organized for different audience levels
- **Code Adaptability**: Analysis code evolves to better handle specific repository characteristics
- **Continuous Improvement**: Each analysis run improves the codebase for future use

## Benefits of Code Evolution Approach

### **Immediate Benefits**:
- **Faster Initial Analysis**: Start with working code instead of building from scratch
- **Proven Foundation**: Built on tested, well-structured modules
- **Consistent Interface**: Maintains familiar patterns across different analyses

### **Long-term Benefits**:
- **Repository-Specific Optimization**: Code becomes better suited for specific project types
- **Knowledge Accumulation**: Each analysis improves the system's capabilities
- **Maintainability**: Code evolves based on real-world usage patterns
- **Scalability**: System can handle increasingly complex repositories over time

### **Quality Assurance**:
- **Incremental Testing**: Each modification is tested with real repository data
- **Real-World Validation**: Code improvements are driven by actual analysis needs
- **Documented Evolution**: Clear record of what changed and why
