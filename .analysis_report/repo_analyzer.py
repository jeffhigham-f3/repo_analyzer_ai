"""
Repository Analyzer Module

This module analyzes the repository structure, identifies technology stacks,
and maps project architecture patterns.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
import json
import yaml

from .config import AnalysisConfig, TechnologyStackConfig


@dataclass
class FileInfo:
    """Information about a file in the repository."""
    
    path: str
    size: int
    lines: int
    extension: str
    is_config: bool
    is_documentation: bool
    is_source: bool


@dataclass
class TechnologyInfo:
    """Information about a technology used in the project."""
    
    name: str
    category: str
    confidence: float
    evidence: List[str]
    version: Optional[str] = None


@dataclass
class ProjectStructure:
    """Analysis of the project structure."""
    
    total_files: int
    total_lines: int
    directories: List[str]
    file_types: Dict[str, int]
    technology_stack: List[TechnologyInfo]
    architecture_patterns: List[str]
    configuration_files: List[str]
    documentation_files: List[str]


class RepositoryAnalyzer:
    """Analyzes repository structure and technology stack."""
    
    def __init__(self, config: AnalysisConfig):
        """
        Initialize the repository analyzer.
        
        Args:
            config: Analysis configuration
        """
        self.config = config
        self.tech_config = config.tech_stack
        
    def analyze_repository(self, repo_path: str) -> ProjectStructure:
        """
        Analyze the complete repository structure.
        
        Args:
            repo_path: Path to the repository root
            
        Returns:
            ProjectStructure object with analysis results
        """
        repo_path = Path(repo_path)
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        # Analyze file structure
        file_info_list = self._scan_directory(repo_path)
        
        # Identify technology stack
        tech_stack = self._identify_technology_stack(file_info_list, repo_path)
        
        # Detect architecture patterns
        architecture_patterns = self._detect_architecture_patterns(file_info_list, tech_stack)
        
        # Categorize files
        config_files = [f.path for f in file_info_list if f.is_config]
        doc_files = [f.path for f in file_info_list if f.is_documentation]
        
        # Calculate totals
        total_files = len(file_info_list)
        total_lines = sum(f.lines for f in file_info_list)
        
        # Group by file type
        file_types = {}
        for file_info in file_info_list:
            ext = file_info.extension
            file_types[ext] = file_types.get(ext, 0) + 1
        
        # Get directory list
        directories = self._get_directories(repo_path)
        
        return ProjectStructure(
            total_files=total_files,
            total_lines=total_lines,
            directories=directories,
            file_types=file_types,
            technology_stack=tech_stack,
            architecture_patterns=architecture_patterns,
            configuration_files=config_files,
            documentation_files=doc_files
        )
    
    def _scan_directory(self, repo_path: Path) -> List[FileInfo]:
        """Scan directory recursively and collect file information."""
        file_info_list = []
        
        for file_path in repo_path.rglob('*'):
            if file_path.is_file():
                # Skip hidden files and common ignore patterns
                if self._should_skip_file(file_path):
                    continue
                
                try:
                    file_info = self._analyze_file(file_path, repo_path)
                    file_info_list.append(file_info)
                except Exception as e:
                    # Log error but continue with other files
                    print(f"Error analyzing file {file_path}: {e}")
        
        return file_info_list
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if a file should be skipped during analysis."""
        # Skip hidden files
        if file_path.name.startswith('.'):
            return True
        
        # Skip common directories to ignore
        skip_dirs = {
            '.git', 'node_modules', '__pycache__', '.pytest_cache',
            'build', 'dist', 'target', 'bin', 'obj'
        }
        
        for part in file_path.parts:
            if part in skip_dirs:
                return True
        
        return False
    
    def _analyze_file(self, file_path: Path, repo_path: Path) -> FileInfo:
        """Analyze a single file and extract information."""
        # Get relative path
        rel_path = str(file_path.relative_to(repo_path))
        
        # Get file size
        size = file_path.stat().st_size
        
        # Count lines
        lines = self._count_lines(file_path)
        
        # Get extension
        extension = file_path.suffix.lower()
        
        # Determine file categories
        is_config = self._is_config_file(file_path)
        is_documentation = self._is_documentation_file(file_path)
        is_source = self._is_source_file(file_path)
        
        return FileInfo(
            path=rel_path,
            size=size,
            lines=lines,
            extension=extension,
            is_config=is_config,
            is_documentation=is_documentation,
            is_source=is_source
        )
    
    def _count_lines(self, file_path: Path) -> int:
        """Count lines in a file, handling different encodings."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return sum(1 for _ in f)
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return sum(1 for _ in f)
            except:
                return 0
        except:
            return 0
    
    def _is_config_file(self, file_path: Path) -> bool:
        """Determine if a file is a configuration file."""
        config_patterns = [
            'package.json', 'requirements.txt', 'pom.xml', 'build.gradle',
            'go.mod', 'Cargo.toml', 'docker-compose.yml', 'Dockerfile',
            '.gitignore', '.env', 'config.yml', 'config.yaml', 'tsconfig.json',
            'webpack.config.js', 'vite.config.js', 'jest.config.js'
        ]
        
        return file_path.name in config_patterns
    
    def _is_documentation_file(self, file_path: Path) -> bool:
        """Determine if a file is a documentation file."""
        doc_extensions = {'.md', '.txt', '.rst', '.adoc'}
        doc_names = {'README', 'CHANGELOG', 'LICENSE', 'CONTRIBUTING'}
        
        return (file_path.suffix.lower() in doc_extensions or
                file_path.stem.upper() in doc_names)
    
    def _is_source_file(self, file_path: Path) -> bool:
        """Determine if a file is a source code file."""
        source_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rs',
            '.cpp', '.c', '.h', '.hpp', '.cs', '.php', '.rb', '.swift'
        }
        
        return file_path.suffix.lower() in source_extensions
    
    def _get_directories(self, repo_path: Path) -> List[str]:
        """Get list of directories in the repository."""
        directories = []
        
        for item in repo_path.rglob('*'):
            if item.is_dir() and not self._should_skip_file(item):
                rel_path = str(item.relative_to(repo_path))
                if rel_path:  # Skip root directory
                    directories.append(rel_path)
        
        return sorted(directories)
    
    def _identify_technology_stack(self, file_info_list: List[FileInfo], 
                                 repo_path: Path) -> List[TechnologyInfo]:
        """Identify the technology stack used in the project."""
        tech_stack = []
        
        # Analyze configuration files
        config_tech = self._analyze_config_files(file_info_list, repo_path)
        tech_stack.extend(config_tech)
        
        # Analyze source files
        source_tech = self._analyze_source_files(file_info_list)
        tech_stack.extend(source_tech)
        
        # Analyze build and dependency files
        build_tech = self._analyze_build_files(file_info_list, repo_path)
        tech_stack.extend(build_tech)
        
        # Remove duplicates and sort by confidence
        unique_tech = self._deduplicate_technologies(tech_stack)
        return sorted(unique_tech, key=lambda x: x.confidence, reverse=True)
    
    def _analyze_config_files(self, file_info_list: List[FileInfo], 
                             repo_path: Path) -> List[TechnologyInfo]:
        """Analyze configuration files to identify technologies."""
        config_tech = []
        
        for file_info in file_info_list:
            if not file_info.is_config:
                continue
            
            file_path = repo_path / file_info.path
            
            try:
                if file_info.path.endswith('package.json'):
                    tech_info = self._analyze_package_json(file_path)
                    if tech_info:
                        config_tech.append(tech_info)
                
                elif file_info.path.endswith('requirements.txt'):
                    tech_info = self._analyze_requirements_txt(file_path)
                    if tech_info:
                        config_tech.append(tech_info)
                
                elif file_info.path.endswith('pom.xml'):
                    tech_info = self._analyze_pom_xml(file_path)
                    if tech_info:
                        config_tech.append(tech_info)
                
                elif file_info.path.endswith('go.mod'):
                    tech_info = self._analyze_go_mod(file_path)
                    if tech_info:
                        config_tech.append(tech_info)
                
                elif file_info.path.endswith('Cargo.toml'):
                    tech_info = self._analyze_cargo_toml(file_path)
                    if tech_info:
                        config_tech.append(tech_info)
                
                elif file_info.path.endswith(('.yml', '.yaml')):
                    tech_info = self._analyze_yaml_file(file_path)
                    if tech_info:
                        config_tech.append(tech_info)
                
            except Exception as e:
                print(f"Error analyzing config file {file_path}: {e}")
        
        return config_tech
    
    def _analyze_package_json(self, file_path: Path) -> Optional[TechnologyInfo]:
        """Analyze package.json file for Node.js technologies."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Check for framework indicators
            dependencies = data.get('dependencies', {})
            dev_dependencies = data.get('devDependencies', {})
            all_deps = {**dependencies, **dev_dependencies}
            
            # Identify frontend frameworks
            if 'react' in all_deps:
                return TechnologyInfo(
                    name="React",
                    category="Frontend",
                    confidence=0.9,
                    evidence=[f"Found in {file_path.name}"],
                    version=all_deps.get('react')
                )
            
            if 'vue' in all_deps:
                return TechnologyInfo(
                    name="Vue.js",
                    category="Frontend",
                    confidence=0.9,
                    evidence=[f"Found in {file_path.name}"],
                    version=all_deps.get('vue')
                )
            
            if 'angular' in all_deps:
                return TechnologyInfo(
                    name="Angular",
                    category="Frontend",
                    confidence=0.9,
                    evidence=[f"Found in {file_path.name}"],
                    version=all_deps.get('angular')
                )
            
            # Identify backend frameworks
            if 'express' in all_deps:
                return TechnologyInfo(
                    name="Express.js",
                    category="Backend",
                    confidence=0.8,
                    evidence=[f"Found in {file_path.name}"],
                    version=all_deps.get('express')
                )
            
            # Generic Node.js
            return TechnologyInfo(
                name="Node.js",
                category="Backend",
                confidence=0.7,
                evidence=[f"Found {file_path.name}"],
                version=data.get('engines', {}).get('node')
            )
            
        except Exception as e:
            print(f"Error parsing package.json: {e}")
            return None
    
    def _analyze_requirements_txt(self, file_path: Path) -> Optional[TechnologyInfo]:
        """Analyze requirements.txt file for Python technologies."""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Check for common Python frameworks
            for line in lines:
                line = line.strip().lower()
                if 'django' in line:
                    return TechnologyInfo(
                        name="Django",
                        category="Backend",
                        confidence=0.9,
                        evidence=[f"Found in {file_path.name}"],
                        version=line.split('==')[-1] if '==' in line else None
                    )
                
                if 'flask' in line:
                    return TechnologyInfo(
                        name="Flask",
                        category="Backend",
                        confidence=0.9,
                        evidence=[f"Found in {file_path.name}"],
                        version=line.split('==')[-1] if '==' in line else None
                    )
            
            # Generic Python
            return TechnologyInfo(
                name="Python",
                category="Backend",
                confidence=0.8,
                evidence=[f"Found {file_path.name}"],
                version=None
            )
            
        except Exception as e:
            print(f"Error parsing requirements.txt: {e}")
            return None
    
    def _analyze_pom_xml(self, file_path: Path) -> Optional[TechnologyInfo]:
        """Analyze pom.xml file for Java technologies."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for Spring Boot
            if 'spring-boot' in content:
                return TechnologyInfo(
                    name="Spring Boot",
                    category="Backend",
                    confidence=0.9,
                    evidence=[f"Found in {file_path.name}"],
                    version=None
                )
            
            # Generic Java
            return TechnologyInfo(
                name="Java",
                category="Backend",
                confidence=0.8,
                evidence=[f"Found {file_path.name}"],
                version=None
            )
            
        except Exception as e:
            print(f"Error parsing pom.xml: {e}")
            return None
    
    def _analyze_go_mod(self, file_path: Path) -> Optional[TechnologyInfo]:
        """Analyze go.mod file for Go technologies."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for common Go frameworks
            if 'gin' in content:
                return TechnologyInfo(
                    name="Gin",
                    category="Backend",
                    confidence=0.9,
                    evidence=[f"Found in {file_path.name}"],
                    version=None
                )
            
            # Generic Go
            return TechnologyInfo(
                name="Go",
                category="Backend",
                confidence=0.8,
                evidence=[f"Found {file_path.name}"],
                version=None
            )
            
        except Exception as e:
            print(f"Error parsing go.mod: {e}")
            return None
    
    def _analyze_cargo_toml(self, file_path: Path) -> Optional[TechnologyInfo]:
        """Analyze Cargo.toml file for Rust technologies."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Generic Rust
            return TechnologyInfo(
                name="Rust",
                category="Backend",
                confidence=0.8,
                evidence=[f"Found {file_path.name}"],
                version=None
            )
            
        except Exception as e:
            print(f"Error parsing Cargo.toml: {e}")
            return None
    
    def _analyze_yaml_file(self, file_path: Path) -> Optional[TechnologyInfo]:
        """Analyze YAML files for technology indicators."""
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
            
            if not data:
                return None
            
            # Check for Docker Compose
            if isinstance(data, dict) and 'services' in data:
                return TechnologyInfo(
                    name="Docker Compose",
                    category="Infrastructure",
                    confidence=0.9,
                    evidence=[f"Found in {file_path.name}"],
                    version=None
                )
            
            # Check for GitHub Actions
            if file_path.name.startswith('.github/workflows/'):
                return TechnologyInfo(
                    name="GitHub Actions",
                    category="CI/CD",
                    confidence=0.9,
                    evidence=[f"Found in {file_path.name}"],
                    version=None
                )
            
            return None
            
        except Exception as e:
            print(f"Error parsing YAML file {file_path}: {e}")
            return None
    
    def _analyze_source_files(self, file_info_list: List[FileInfo]) -> List[TechnologyInfo]:
        """Analyze source files to identify technologies."""
        source_tech = []
        
        # Count file types
        ext_counts = {}
        for file_info in file_info_list:
            if file_info.is_source:
                ext = file_info.extension
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
        
        # Identify technologies based on file extensions
        for ext, count in ext_counts.items():
            if ext == '.py' and count > 0:
                source_tech.append(TechnologyInfo(
                    name="Python",
                    category="Backend",
                    confidence=0.7,
                    evidence=[f"Found {count} Python files"],
                    version=None
                ))
            
            elif ext in ['.js', '.jsx'] and count > 0:
                source_tech.append(TechnologyInfo(
                    name="JavaScript/JSX",
                    category="Frontend",
                    confidence=0.7,
                    evidence=[f"Found {count} JavaScript/JSX files"],
                    version=None
                ))
            
            elif ext in ['.ts', '.tsx'] and count > 0:
                source_tech.append(TechnologyInfo(
                    name="TypeScript",
                    category="Frontend",
                    confidence=0.7,
                    evidence=[f"Found {count} TypeScript files"],
                    version=None
                ))
            
            elif ext == '.java' and count > 0:
                source_tech.append(TechnologyInfo(
                    name="Java",
                    category="Backend",
                    confidence=0.7,
                    evidence=[f"Found {count} Java files"],
                    version=None
                ))
            
            elif ext == '.go' and count > 0:
                source_tech.append(TechnologyInfo(
                    name="Go",
                    category="Backend",
                    confidence=0.7,
                    evidence=[f"Found {count} Go files"],
                    version=None
                ))
        
        return source_tech
    
    def _analyze_build_files(self, file_info_list: List[FileInfo], 
                            repo_path: Path) -> List[TechnologyInfo]:
        """Analyze build and dependency files."""
        build_tech = []
        
        for file_info in file_info_list:
            if not file_info.is_config:
                continue
            
            file_path = repo_path / file_info.path
            
            # Check for build tools
            if file_info.path.endswith('Makefile'):
                build_tech.append(TechnologyInfo(
                    name="Make",
                    category="Build Tools",
                    confidence=0.9,
                    evidence=[f"Found {file_info.path}"],
                    version=None
                ))
            
            elif file_info.path.endswith('webpack.config.js'):
                build_tech.append(TechnologyInfo(
                    name="Webpack",
                    category="Build Tools",
                    confidence=0.9,
                    evidence=[f"Found {file_info.path}"],
                    version=None
                ))
            
            elif file_info.path.endswith('vite.config.js'):
                build_tech.append(TechnologyInfo(
                    name="Vite",
                    category="Build Tools",
                    confidence=0.9,
                    evidence=[f"Found {file_info.path}"],
                    version=None
                ))
        
        return build_tech
    
    def _deduplicate_technologies(self, tech_list: List[TechnologyInfo]) -> List[TechnologyInfo]:
        """Remove duplicate technologies and merge evidence."""
        tech_dict = {}
        
        for tech in tech_list:
            key = (tech.name, tech.category)
            
            if key in tech_dict:
                # Merge evidence and take higher confidence
                existing = tech_dict[key]
                existing.evidence.extend(tech.evidence)
                existing.confidence = max(existing.confidence, tech.confidence)
            else:
                tech_dict[key] = tech
        
        return list(tech_dict.values())
    
    def _detect_architecture_patterns(self, file_info_list: List[FileInfo], 
                                    tech_stack: List[TechnologyInfo]) -> List[str]:
        """Detect common architecture patterns in the project."""
        patterns = []
        
        # Check for microservices pattern
        if self._detect_microservices_pattern(file_info_list):
            patterns.append("Microservices")
        
        # Check for monorepo pattern
        if self._detect_monorepo_pattern(file_info_list):
            patterns.append("Monorepo")
        
        # Check for layered architecture
        if self._detect_layered_architecture(file_info_list):
            patterns.append("Layered Architecture")
        
        # Check for MVC pattern
        if self._detect_mvc_pattern(file_info_list):
            patterns.append("Model-View-Controller (MVC)")
        
        # Check for event-driven architecture
        if self._detect_event_driven_pattern(file_info_list):
            patterns.append("Event-Driven Architecture")
        
        return patterns
    
    def _detect_microservices_pattern(self, file_info_list: List[FileInfo]) -> bool:
        """Detect if the project follows a microservices pattern."""
        # Look for multiple service directories
        service_dirs = [f.path for f in file_info_list 
                       if 'service' in f.path.lower() or 'api' in f.path.lower()]
        
        # Look for Docker files
        docker_files = [f.path for f in file_info_list 
                       if f.path.endswith('Dockerfile') or 'docker-compose' in f.path]
        
        return len(service_dirs) > 1 or len(docker_files) > 1
    
    def _detect_monorepo_pattern(self, file_info_list: List[FileInfo]) -> bool:
        """Detect if the project is a monorepo."""
        # Look for multiple package.json files or multiple language indicators
        package_files = [f.path for f in file_info_list if f.path.endswith('package.json')]
        py_files = [f.path for f in file_info_list if f.path.endswith('.py')]
        java_files = [f.path for f in file_info_list if f.path.endswith('.java')]
        
        return len(package_files) > 1 or (len(py_files) > 0 and len(java_files) > 0)
    
    def _detect_layered_architecture(self, file_info_list: List[FileInfo]) -> bool:
        """Detect layered architecture patterns."""
        # Look for common layer directories
        layer_dirs = ['controllers', 'services', 'repositories', 'models', 'views']
        found_layers = sum(1 for layer in layer_dirs 
                          for f in file_info_list if layer in f.path.lower())
        
        return found_layers >= 3
    
    def _detect_mvc_pattern(self, file_info_list: List[FileInfo]) -> bool:
        """Detect MVC architecture pattern."""
        # Look for MVC-related directories
        mvc_dirs = ['models', 'views', 'controllers']
        found_mvc = sum(1 for mvc_dir in mvc_dirs 
                       for f in file_info_list if mvc_dir in f.path.lower())
        
        return found_mvc >= 2
    
    def _detect_event_driven_pattern(self, file_info_list: List[FileInfo]) -> bool:
        """Detect event-driven architecture patterns."""
        # Look for event-related files
        event_files = [f.path for f in file_info_list 
                      if 'event' in f.path.lower() or 'listener' in f.path.lower()]
        
        return len(event_files) > 0 