

<p align="center">
  <img src="https://img.shields.io/badge/Firewall--Optimizer-AI--Powered-ff0050?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/github/license/your-username/firewall-optimizer?style=for-the-badge&color=blue" />
  <img src="https://img.shields.io/badge/Built_with-Streamlit-orange?style=for-the-badge&logo=streamlit" />
</p>
<p align="center">
  <img src="https://github.com/Dev-axay18/firewall-rule-optimizer/blob/main/assets/AI-Powered%20Firewall%20Rule%20Optimizer.png?raw=true" alt="AI-Powered Firewall Rule Optimizer Banner" width="100%" />
</p>


# 🔥 AI-Powered Firewall Rule Optimizer and Visualizer

A comprehensive Python-based tool that analyzes Linux `iptables` firewall rules, detects redundant or conflicting rules, suggests optimization strategies, and provides interactive visualizations with beautiful CLI graphics for better security management.

## 🎯 Features

### 🔍 **Analysis Capabilities**
- **Redundant Rule Detection**: Identifies duplicate rules that can be removed
- **Conflict Resolution**: Finds rules that contradict each other
- **Performance Optimization**: Suggests rule reordering for better efficiency
- **Security Analysis**: Detects potential security vulnerabilities
- **Unreachable Rule Detection**: Finds rules that will never be executed

### 💡 **Intelligent Recommendations**
- **Priority-based Suggestions**: Categorizes recommendations by importance (🔥Critical, 🚨High, ⚠️Medium, 💡Low)
- **Risk Assessment**: Evaluates the risk level of each recommendation
- **Impact Analysis**: Estimates performance and security improvements
- **Implementation Guidance**: Provides step-by-step instructions

### 🎨 **Beautiful CLI Graphics**
- **Colorful Progress Bars**: Visual score representation for security and efficiency
- **ASCII Bar Charts**: Issue distribution visualization
- **Severity Pie Charts**: Visual breakdown of issue severity levels
- **Priority Charts**: Recommendation priorities with icons and colors
- **Impact Gauges**: Visual optimization benefits display
- **Professional Styling**: VS Code-like syntax highlighting with emojis

### 📊 **Advanced Visualizations**
- **Interactive Rule Flow Diagrams**: Visualize packet flow through rules
- **Dependency Graphs**: Show relationships between chains and rules
- **Security Dashboards**: Real-time security and efficiency scores
- **Rule Coverage Heatmaps**: Analyze protocol and port coverage
- **Optimization Impact Charts**: Visualize potential improvements

### 🖥️ **Multiple Interfaces**
- **Enhanced CLI**: Beautiful terminal interface with charts and colors
- **Web Interface**: User-friendly Streamlit-based GUI with interactive features
- **Python API**: Integrate into your own applications

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Linux system with `iptables` (for live analysis)
- Administrator privileges (for applying changes)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/firewall-optimizer.git
cd firewall-optimizer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### 🎯 Instant Usage (No Configuration Required!)

### 🔍 Analyze sample firewall rules with beautiful CLI graphics
```bash
python main.py analyze
```
### ⚡ Generate optimization recommendations with visual charts  
```bash
python main.py optimize
```
### 📊 Create interactive visualizations
```bash
python main.py visualize
```
### 🌐 Launch web interface
```bash
python main.py webapp
```

**That's it!** The tool includes sample data, so you can start exploring immediately!

## 🎨 CLI Interface Features

### Visual Elements
Our enhanced CLI provides a beautiful terminal experience with:

- 🔥 **Colorful Startup Banner** with ASCII art
- 📊 **Progress Bars** for security and efficiency scores  
- 📈 **Bar Charts** showing issue distribution
- 🥧 **Pie Charts** for severity level breakdown
- 🎯 **Priority Visualization** for recommendations
- ⚡ **Impact Gauges** showing optimization benefits
- 🌈 **Color-coded Output** for easy reading

### Sample CLI Output
```
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║        🔥 AI-Powered Firewall Rule Optimizer 🔥         ║
    ║                                                          ║
    ║     Analyze • Optimize • Visualize • Secure            ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝

────────────────────────────────────────
📊 Score Overview  
────────────────────────────────────────
  Security Score.......... ████████████████████░░░░░░░░░░ 54.0%
  Efficiency Score........ ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 5.0%

────────────────────────────────────────
📊 Issues Distribution
────────────────────────────────────────
  Conflicting............. ████████████████████████████████ 15
  Unreachable............. ██████████████████████████████   13  
  Inefficient Order....... ████████████████████████         11
  Security Risk........... ████                              2
```
## Console Output
<p align="center">
  <img src="https://github.com/Dev-axay18/firewall-rule-optimizer/blob/main/assets/removed-background%20(1).png?raw=true" width="600">
  <br><em>🧠 Console Output </em>
</p>

## 🌐 Web Dashboard Preview

> 📊 Run in your browser: `python main.py webapp`

### 📷 Screenshot Samples

<p align="center">
  <img src="[https://github.com/your-username/firewall-optimizer/assets/web-overview.png](https://github.com/Dev-axay18/firewall-rule-optimizer/blob/main/assets/photo_5_2025-07-27_19-39-52.jpg?raw=true)" width="600">
  <br><em>🧠 AI-Powered Analysis Dashboard</em>
</p>

<p align="center">
  <img src="https://github.com/Dev-axay18/firewall-rule-optimizer/blob/main/assets/photo_6_2025-07-27_19-39-52.jpg?raw=true" width="600">
  <br><em>📈 Real-time Visualizations of Issues and Priorities</em>
</p>

<p align="center">
  <img src="[https://github.com/your-username/firewall-optimizer/assets/flow-diagram.png](https://github.com/Dev-axay18/firewall-rule-optimizer/blob/main/assets/photo_7_2025-07-27_19-39-52.jpg?raw=true)" width="600">
  <br><em>🌐 Rule Flow Diagrams & Dependency Mapping</em>
</p>
<p align="center">
  <img src="https://github.com/Dev-axay18/firewall-rule-optimizer/blob/main/assets/photo_8_2025-07-27_19-39-52.jpg?raw=true" width="600">
  <br><em>🌐 Visualization </em>
</p>

--- 

## 📋 Complete Command Reference

### 🔍 Analysis Commands
### Basic analysis with beautiful graphics
```bash
python main.py analyze
```
### Analyze specific file
```bash
python main.py analyze --input /path/to/iptables-rules.txt
```
### Analyze current system rules (Linux)
```bash
python main.py analyze --input system
```
### Save results to file
```bash
python main.py analyze --output report.json --format json
```

### ⚡ Optimization Commands  
```bash
# Generate recommendations with visual priority charts
python main.py optimize

# Optimize specific configuration
python main.py optimize --input /path/to/rules.txt

# Save optimized rules
python main.py optimize --input rules.txt --output optimized.txt

# Apply to system with backup (requires root)
sudo python main.py optimize --input system --apply --backup
```

### 📊 Visualization Commands
```bash
# Create all interactive visualizations
python main.py visualize

# Specific visualization types
python main.py visualize --type flow      # Rule flow diagram
python main.py visualize --type issues   # Issues dashboard  
python main.py visualize --type graph    # Network topology
```

### 🌐 Web Interface
```bash
# Launch web app (default: localhost:8501)
python main.py webapp

# Custom port and host
python main.py webapp --port 8080 --host 0.0.0.0
```

### 💾 Backup & Restore
#### Create backup
```bash
python main.py backup --input system --description "Before optimization"
```
### Restore from backup
```bash
python main.py restore --backup /path/to/backup.json
```

## 📖 Usage Guide

### 🌐 Web Interface

Launch the interactive web interface:

```bash
python main.py webapp
```

Then open your browser to `http://localhost:8501`

**Features:**
- 📁 Upload firewall configuration files or use sample data
- 🔍 Real-time analysis with colorful charts and metrics
- 📊 Interactive visualizations and dashboards
- 💾 Backup and restore functionality
- ⚙️ Configurable analysis settings
- 📤 Export reports in multiple formats

### 💻 Enhanced Command Line Interface

Our CLI features beautiful terminal graphics with:
- 🎨 **VS Code-like syntax highlighting** with colors
- 📊 **ASCII progress bars and charts** 
- 🔥 **Emoji-rich output** for better readability
- 📈 **Visual data representation** right in your terminal

For complete command documentation, see **[COMMANDS.md](COMMANDS.md)** - a comprehensive guide with:
- 📋 All available commands and options
- 💡 Usage examples and best practices  
- 🎨 CLI features and visual elements
- 🔧 Advanced configuration options
- 🚨 Safety features and troubleshooting

### 💻 Command Line Interface

#### Analyze Firewall Rules

```bash
# Analyze a configuration file
python main.py analyze --input /etc/iptables/rules.v4

# Analyze current system rules
python main.py analyze --input system

# Save analysis to file
python main.py analyze --input rules.txt --output analysis.json --format json
```

#### Generate Optimization Recommendations

```bash
# Generate recommendations
python main.py optimize --input rules.txt

# Generate and save optimized rules
python main.py optimize --input rules.txt --output optimized_rules.txt

# Apply optimizations (with backup)
python main.py optimize --input system --apply --backup
```

#### Create Visualizations

### Create comprehensive visualization report
```bash
python main.py visualize --input rules.txt --output ./reports
```
### Create specific visualization types
```bash
python main.py visualize --input rules.txt --output ./reports --type flow
```

#### Backup and Restore
### Create backup
```bash
python main.py backup --input system --description "Before optimization"
```
### Restore from backup
```bash
python main.py restore --backup backup_20250126_143022.json --apply
```

### 🐍 Python API

```python
from optimizer import (
    IptablesParser, FirewallAnalyzer, 
    FirewallRecommender, FirewallVisualizer
)

# Initialize components
parser = IptablesParser()
analyzer = FirewallAnalyzer()
recommender = FirewallRecommender()
visualizer = FirewallVisualizer()

# Load and parse configuration
with open('rules.txt', 'r') as f:
    rules_content = f.read()

config = parser.parse_iptables_save(rules_content)

# Analyze configuration
analysis = analyzer.analyze_configuration(config)
print(f"Security Score: {analysis.security_score:.1f}/100")
print(f"Issues Found: {len(analysis.issues)}")

# Generate recommendations
plan = recommender.generate_recommendations(config, analysis)
print(f"Recommendations: {len(plan.recommendations)}")

# Create visualizations
flow_chart = visualizer.create_rule_flow_diagram(config)
dashboard = visualizer.create_issue_dashboard(analysis)

# Show interactive plots
flow_chart.show()
dashboard.show()
```

## � Documentation & Help

### 📖 Complete Command Reference
- **[COMMANDS.md](COMMANDS.md)** - Comprehensive command documentation with examples
- Use `python main.py --help` for general help
- Use `python main.py <command> --help` for command-specific help

### 🎨 What Makes Our CLI Special
1. **Beautiful Visual Output**: ASCII progress bars, charts, and colored text
2. **Instant Feedback**: No configuration needed - works with sample data
3. **Professional Styling**: VS Code-like syntax highlighting with emojis  
4. **Smart Graphics**: Charts adjust to terminal width automatically
5. **Cross-Platform**: Works on Windows, macOS, and Linux
6. **Comprehensive**: Analysis, optimization, visualization, and web interface

### 🔥 Key Features Highlights

#### 🎯 Smart Analysis
- Detects 47+ different types of firewall issues
- Provides actionable recommendations for each issue
- Calculates security and efficiency scores
- Identifies unreachable and redundant rules

#### ⚡ Visual Performance  
- Beautiful terminal graphics without external dependencies
- Real-time progress indicators during analysis
- Color-coded severity levels (🔴Critical, 🟡Medium, 🟢Low)
- Interactive web charts with Plotly integration

#### 🛡️ Enterprise-Ready
- Automatic backup creation before any changes
- Dry-run mode by default (no accidental modifications)
- Comprehensive logging and audit trails
- Linux system integration with iptables

## �📂 Project Structure

```
firewall-optimizer/
│
├── data/                          # Sample data and test files
│   └── sample_rules.txt          # Sample iptables rules
│
├── optimizer/                     # Core optimizer package
│   ├── __init__.py               # Package initialization
│   ├── parser.py                 # Iptables rule parser
│   ├── analyzer.py               # Rule analysis engine
│   ├── recommender.py            # Optimization recommender
│   ├── visualizer.py             # Visualization components
│   └── utils.py                  # Utility functions
│
├── web_ui/                        # Streamlit web interface
│   └── app.py                    # Main web application
│
├── main.py                        # Command line interface
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── .github/
    └── copilot-instructions.md    # Copilot customization
```

## 🔧 Configuration

The optimizer can be configured through YAML configuration files:

```yaml
# optimizer_config.yaml
backup:
  enabled: true
  directory: './backups'
  max_backups: 10
  auto_backup_before_changes: true

analysis:
  check_redundant_rules: true
  check_conflicting_rules: true
  check_rule_ordering: true
  check_unreachable_rules: true
  check_security_issues: true
  confidence_threshold: 0.8

security:
  allow_system_modifications: false
  require_sudo_confirmation: true
  validate_rules_before_apply: true

visualization:
  default_theme: 'plotly_white'
  save_format: 'html'
  include_interactive: true
```

## 📊 Example Analysis Output

```
FIREWALL ANALYSIS RESULTS
============================================================

Overall Scores:
  Security Score:    78.5/100
  Efficiency Score:  85.2/100

Statistics:
  Total Rules: 23
  Total Chains: 6
  Total Tables: 3
  Accept Rules: 8
  Drop Rules: 12
  Reject Rules: 1

Issues Found (4):

  Redundant (2 issues):
    • Redundant rule found: duplicate of rule at line 15
      → Remove the duplicate rule to improve performance
    • Redundant rule found: duplicate of rule at line 22
      → Remove the duplicate rule to improve performance

  Security Risk (1 issues):
    • Administrative port 22 open to all sources
      → Restrict access to administrative ports to specific source IPs

  Inefficient Order (1 issues):
    • Specific rule at line 18 comes after general rule at line 12
      → Move more specific rules before general ones for better performance
```

## 🛡️ Security Considerations

### ⚠️ **Important Safety Features**

- **Dry Run Mode**: All operations default to dry run mode
- **Automatic Backups**: Creates backups before any modifications
- **Rule Validation**: Validates rules before applying changes
- **Confirmation Prompts**: Requires explicit confirmation for system changes
- **Rollback Capability**: Can restore from backups if needed

### 🔒 **Best Practices**

1. **Always test in dry run mode first**
2. **Create backups before making changes**
3. **Validate optimized rules in a test environment**
4. **Review all recommendations before applying**
5. **Keep the original configuration as a backup**

## 🔬 Example Optimizations

| Issue Type | Before | After | Impact |
|------------|--------|-------|--------|
| **Redundancy** | ```-A INPUT -p tcp --dport 22 -j ACCEPT``` (duplicated) | Single occurrence | Reduced rule count |
| **Conflict** | Allow port 80, then deny port 80 | Resolved based on policy | Predictable behavior |
| **Inefficiency** | Broad ACCEPT before specific DROP | Reordered for security | Better performance |
| **Security** | SSH open to 0.0.0.0/0 | Restricted to specific IPs | Reduced attack surface |

## 🧪 Testing

Run the example analysis with sample data:

```bash
# Test with sample rules
python main.py analyze --input data/sample_rules.txt

# Test web interface
python main.py webapp

# Test visualization generation
python main.py visualize --input data/sample_rules.txt --output ./test_reports
```

## 📋 Dependencies

### Core Dependencies
- `streamlit` - Web interface framework
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `matplotlib` - Static plotting
- `plotly` - Interactive plotting
- `networkx` - Graph analysis
- `seaborn` - Statistical visualization
- `pyparsing` - Text parsing
- `pyyaml` - YAML configuration
- `click` - Command line interface

### Optional Dependencies
- `scikit-learn` - Machine learning (for advanced analysis)
- `xgboost` - Gradient boosting (for ML features)
- `dash` - Alternative web framework
- `flask` - Lightweight web framework

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/firewall-optimizer.git
cd firewall-optimizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
python -m pytest tests/

# Run linting
black optimizer/
flake8 optimizer/
mypy optimizer/
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **iptables** - The Linux firewall utility that makes this project possible
- **Streamlit** - For providing an excellent web framework for data applications
- **Plotly** - For interactive visualization capabilities
- **NetworkX** - For graph analysis and visualization
- **The Python Community** - For the amazing ecosystem of tools and libraries

## 📞 Support

- 📧 **Email**: kaleakshay8856@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/Dev-axay18/firewall-rule-optimizer/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Dev-axay18/firewall-rule-optimizer/discussions)

---

**⭐ Star this repository if you find it useful!**

Made with ❤️ by the Firewall Optimizer Team
