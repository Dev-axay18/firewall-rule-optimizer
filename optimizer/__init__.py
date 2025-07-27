"""
AI-Powered Firewall Rule Optimizer and Visualizer

This package provides comprehensive analysis and optimization capabilities
for Linux iptables firewall rules, including:

- Rule parsing and validation
- Redundancy and conflict detection
- Security vulnerability analysis
- Performance optimization recommendations
- Interactive visualization and reporting

Main Components:
- parser: Parse iptables rules and configurations
- analyzer: Analyze rules for issues and optimization opportunities
- recommender: Generate intelligent optimization recommendations
- visualizer: Create interactive visualizations and reports
- utils: Utility functions and system interfaces

Example Usage:
    from optimizer import IptablesParser, FirewallAnalyzer, FirewallRecommender
    
    parser = IptablesParser()
    analyzer = FirewallAnalyzer()
    recommender = FirewallRecommender()
    
    # Parse configuration
    config = parser.parse_iptables_save(rules_content)
    
    # Analyze for issues
    analysis = analyzer.analyze_configuration(config)
    
    # Generate recommendations
    plan = recommender.generate_recommendations(config, analysis)
"""

__version__ = "1.0.0"
__author__ = "Firewall Optimizer Team"
__email__ = "contact@firewalloptimizer.com"

# Import main classes for easy access
from .parser import (
    IptablesParser,
    FirewallRule,
    FirewallConfig,
    ChainInfo,
    RuleAction,
    RuleTable,
    ChainPolicy
)

from .analyzer import (
    FirewallAnalyzer,
    AnalysisResult,
    RuleIssue,
    IssueType,
    IssueSeverity
)

from .recommender import (
    FirewallRecommender,
    OptimizationPlan,
    Recommendation,
    RecommendationType,
    RecommendationPriority
)

from .visualizer import (
    FirewallVisualizer
)

from .cli_graphics import (
    CLIGraphics
)

from .utils import (
    ConfigManager,
    BackupManager,
    SystemInterface,
    setup_logging,
    safe_file_operation,
    validate_ip_address,
    validate_port,
    format_size
)

# Define what's available when importing with "from optimizer import *"
__all__ = [
    # Parser components
    'IptablesParser',
    'FirewallRule', 
    'FirewallConfig',
    'ChainInfo',
    'RuleAction',
    'RuleTable',
    'ChainPolicy',
    
    # Analyzer components
    'FirewallAnalyzer',
    'AnalysisResult',
    'RuleIssue',
    'IssueType',
    'IssueSeverity',
    
    # Recommender components
    'FirewallRecommender',
    'OptimizationPlan',
    'Recommendation',
    'RecommendationType',
    'RecommendationPriority',
    
    # Visualizer components
    'FirewallVisualizer',
    
    # Utility components
    'ConfigManager',
    'BackupManager',
    'SystemInterface',
    'setup_logging',
    'safe_file_operation',
    'validate_ip_address',
    'validate_port',
    'format_size'
]

# Package metadata
PACKAGE_INFO = {
    'name': 'firewall-optimizer',
    'version': __version__,
    'description': 'AI-Powered Firewall Rule Optimizer and Visualizer',
    'author': __author__,
    'author_email': __email__,
    'url': 'https://github.com/firewall-optimizer/firewall-optimizer',
    'license': 'MIT',
    'python_requires': '>=3.8',
    'keywords': ['firewall', 'iptables', 'security', 'optimization', 'visualization'],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Networking :: Firewalls',
        'Topic :: System :: Systems Administration',
        'Topic :: Security'
    ]
}
