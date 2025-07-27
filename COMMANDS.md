# 🔥 AI-Powered Firewall Rule Optimizer - Complete Commands Guide

<div align="center">

```
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║        🔥 AI-Powered Firewall Rule Optimizer 🔥         ║
    ║                                                          ║
    ║        📋 Complete Commands Reference Guide              ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
```

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![CLI](https://img.shields.io/badge/CLI-Enhanced-green.svg)](https://github.com)
[![Web](https://img.shields.io/badge/Web-Streamlit-red.svg)](https://streamlit.io)
[![Graphics](https://img.shields.io/badge/Graphics-ASCII%20Art-purple.svg)](https://github.com)

</div>

---

## 📖 Table of Contents

- [🚀 Quick Start Commands](#-quick-start-commands)
- [🔍 Analyze Command](#-analyze-command)
- [⚡ Optimize Command](#-optimize-command)
- [📊 Visualize Command](#-visualize-command)
- [🌐 WebApp Command](#-webapp-command)
- [💾 Backup Command](#-backup-command)
- [🔄 Restore Command](#-restore-command)
- [🎨 CLI Visual Features](#-cli-visual-features)
- [📁 File Formats](#-file-formats)
- [🛠️ Advanced Usage](#️-advanced-usage)
- [🚨 Safety Features](#-safety-features)
- [🐛 Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start Commands

### ⚡ Instant Usage (Zero Configuration!)
```bash
# 🔍 Analyze sample firewall rules with stunning CLI graphics
python main.py analyze

# ⚡ Generate optimization recommendations with visual priority charts
python main.py optimize

# 📊 Create interactive HTML visualizations and reports
python main.py visualize

# 🌐 Launch beautiful web interface with dashboard
python main.py webapp
```

> 💡 **Pro Tip**: All commands work immediately with included sample data - no setup required!

---

## 🔍 Analyze Command

### 🎯 Purpose
Analyze firewall rules for security issues, conflicts, redundancies, and performance problems with beautiful visual output.

### 📋 Basic Syntax
```bash
python main.py analyze [OPTIONS]
```

### 🚀 Usage Examples

#### 📊 Basic Analysis (Sample Data)
```bash
python main.py analyze
```
**Output Features:**
- 🔥 Colorful startup banner with ASCII art
- 📊 Progress bars for security (54.0%) and efficiency (5.0%) scores  
- 📈 Bar charts showing issue distribution (47 issues found)
- 🥧 Pie charts for severity levels (Critical/High/Medium/Low)
- 🎨 Color-coded issue details with emojis and icons

#### 📁 Analyze Specific File
```bash
python main.py analyze --input /path/to/iptables-rules.txt
python main.py analyze --input data/production-rules.txt
python main.py analyze -i firewall-config.txt
```

#### 🖥️ Analyze Live System Rules (Linux)
```bash
sudo python main.py analyze --input system
```
> ⚠️ **Note**: Requires root privileges to read system iptables

#### 💾 Save Analysis Results
```bash
# Save as JSON for machine processing
python main.py analyze --output analysis-report.json --format json

# Save as formatted text
python main.py analyze --output analysis-report.txt --format text

# Save as HTML report
python main.py analyze --output analysis-report.html --format html
```

#### 🔍 Verbose Analysis
```bash
python main.py analyze --verbose
python main.py analyze -v --input system
```

### 📊 Visual Output Example
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
  Redundant............... ██                                2
  Missing Log............. ██                                2
  Overly Permissive....... ██                                2

🥧 Severity Distribution
────────────────────────────────────────
    🔥 CRITICAL...... ███                    6.4% (3)
    🚨 HIGH.......... ████████████████████   42.6% (20)  
    ⚠️  MEDIUM........ ███████████████████████ 48.9% (23)
    💡 LOW........... ██                     2.1% (1)
```

### 🎛️ Command Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--input` | `-i` | Input file path or "system" | `--input rules.txt` |
| `--output` | `-o` | Output file for results | `--output report.json` |
| `--format` | | Output format (json/text/html) | `--format json` |
| `--verbose` | `-v` | Enable detailed logging | `--verbose` |

---

## ⚡ Optimize Command

### 🎯 Purpose
Generate intelligent optimization recommendations with visual priority charts and impact analysis.

### 📋 Basic Syntax
```bash
python main.py optimize [OPTIONS]
```

### 🚀 Usage Examples

#### 🎯 Basic Optimization (Sample Data)
```bash
python main.py optimize
```
**Visual Features:**
- ⚡ Performance impact gauges with colored bars
- 🎯 Priority charts (🔥Critical, 🚨High, ⚠️Medium, 💡Low)
- 📈 Estimated improvements (78.9% performance gain)
- 🔄 Rules reduction analysis (can remove 15 redundant rules)

#### 📁 Optimize Specific Configuration
```bash
python main.py optimize --input /path/to/rules.txt
python main.py optimize -i production-firewall.txt
```

#### 💾 Save Optimized Rules
```bash
python main.py optimize --input rules.txt --output optimized-rules.txt
python main.py optimize -i firewall.txt -o optimized.txt
```

#### 🛡️ Safe System Optimization (with Backup)
```bash
sudo python main.py optimize --input system --backup --output /tmp/optimized.txt
```

#### ⚡ Apply Optimizations to System
```bash
# Create backup first (HIGHLY RECOMMENDED)
sudo python main.py backup --input system --description "Before optimization"

# Apply with automatic backup
sudo python main.py optimize --input system --apply --backup
```
> 🚨 **CRITICAL**: Always backup before applying to production systems!

### 📊 Visual Output Example
```
============================================================
                OPTIMIZATION RECOMMENDATIONS
============================================================

⚡ Optimization Impact
────────────────────────────────────────
  🚀 Performance Gain: 78.9% ███████████████████████████████████████
  🛡️  Security Gain:    45.2% ██████████████████████
  🔄 Rules Reduced:    15 rules

🎯 Recommendation Priorities
────────────────────────────────────────
  🔥 CRITICAL...... ████████████████████ 41.7% (20)
  🚨 HIGH.......... ████████████████     33.3% (16)  
  ⚠️  MEDIUM........ ██████████           20.8% (10)
  💡 LOW........... ██                    4.2% (2)

────────────────────────────────────────
📋 Detailed Recommendations
────────────────────────────────────────

🔥 CRITICAL Priority (20 recommendations)
────────────────────────────────────────

  #1 Remove Redundant Rules
     Eliminate 8 duplicate rules that waste processing cycles
     Impact: Improves performance by 15-20%
     
  #2 Fix Rule Conflicts  
     Resolve 15 conflicting rules causing unpredictable behavior
     Impact: Eliminates security gaps and improves reliability
```

### 🎛️ Command Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--input` | `-i` | Input file path or "system" | `--input rules.txt` |
| `--output` | `-o` | Output file for optimized rules | `--output optimized.txt` |
| `--apply` | | Apply optimizations to system | `--apply` |
| `--backup` | | Create backup before changes | `--backup` |

---

## 📊 Visualize Command

### 🎯 Purpose
Create interactive HTML visualizations, dashboards, and comprehensive reports.

### 📋 Basic Syntax
```bash
python main.py visualize [OPTIONS]
```

### 🚀 Usage Examples

#### 🌐 Create All Visualizations (Sample Data)
```bash
python main.py visualize
```
**Generated Files:**
- `report/rule_flow.html` - Interactive rule flow diagram
- `report/issues_dashboard.html` - Comprehensive issues analysis  
- `report/optimization_impact.html` - Optimization recommendations
- `report/network_topology.html` - Network structure visualization

#### 📁 Visualize Specific Configuration
```bash
python main.py visualize --input /path/to/rules.txt
python main.py visualize -i production-rules.txt
```

#### 📂 Custom Output Directory
```bash
python main.py visualize --output ./custom-reports
python main.py visualize -o /tmp/firewall-analysis
```

#### 🎨 Specific Visualization Types
```bash
# Interactive rule flow diagram
python main.py visualize --type flow

# Issues and security dashboard  
python main.py visualize --type issues

# Network topology graph
python main.py visualize --type graph

# Rule complexity heatmap
python main.py visualize --type heatmap

# All visualizations (default)
python main.py visualize --type all
```

### 📊 Visual Output Example
```
ℹ Loading sample configuration...
ℹ 📂 Loading configuration from data/sample_rules.txt...
ℹ Analyzing configuration...
ℹ Generating recommendations...
ℹ Creating visualizations in ./report...

────────────────────────────────────────
📊 Visualizations Created
────────────────────────────────────────
  ✓ Interactive Flow Diagram: ./report/rule_flow.html
  ✓ Issues Dashboard: ./report/issues_dashboard.html  
  ✓ Optimization Impact: ./report/optimization_impact.html
  ✓ Network Topology: ./report/network_topology.html
  ✓ Rule Coverage Heatmap: ./report/coverage_heatmap.html

🌐 Open ./report/rule_flow.html in your browser to view the report.
────────────────────────────────────────
```

### 🎛️ Command Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--input` | `-i` | Input file path or "system" | `--input rules.txt` |
| `--output` | `-o` | Output directory | `--output ./reports` |
| `--type` | | Visualization type | `--type flow` |

### 🎨 Visualization Types

| Type | Description | Output File |
|------|-------------|-------------|
| `all` | All visualizations (default) | Multiple files |
| `flow` | Interactive rule flow diagram | `rule_flow.html` |
| `issues` | Issues and security dashboard | `issues_dashboard.html` |
| `graph` | Network topology graph | `network_topology.html` |
| `heatmap` | Rule coverage heatmap | `coverage_heatmap.html` |

---

## 🌐 WebApp Command

### 🎯 Purpose
Launch the beautiful Streamlit-based web interface with interactive dashboard.

### 📋 Basic Syntax
```bash
python main.py webapp [OPTIONS]
```

### 🚀 Usage Examples

#### 🌐 Launch Web Interface (Default)
```bash
python main.py webapp
```
**Opens**: `http://localhost:8501`

#### 🎛️ Custom Port
```bash
python main.py webapp --port 8080
python main.py webapp --port 3000
```

#### 🌍 Public Access
```bash
python main.py webapp --host 0.0.0.0 --port 8080
```
**Accessible from**: Any device on your network via `http://YOUR_IP:8080`

#### 🔧 Development Mode
```bash
python main.py webapp --host localhost --port 8501
```

### 🎨 Web Interface Features

#### 📋 Main Dashboard
- 📁 **File Upload**: Drag & drop firewall configuration files
- 🔍 **Real-time Analysis**: Instant analysis with visual charts
- 📊 **Interactive Charts**: Plotly-based visualizations
- 🎯 **Smart Recommendations**: Priority-based optimization suggestions

#### 🎛️ Sidebar Features
- 📤 **Load Configuration**: Upload files or use sample data
- 💾 **Backup Management**: Create and restore backups
- ⚙️ **Settings**: Configure analysis parameters
- 🔄 **Reset**: Clear session and start fresh

#### 📊 Analysis Tabs
1. **📋 Overview**: Configuration summary and scores
2. **🔍 Analysis**: Detailed issue breakdown with charts
3. **⚡ Recommendations**: Optimization suggestions with priorities
4. **📊 Visualizations**: Interactive dashboards and graphs

### 🎛️ Command Options

| Option | Short | Description | Default | Example |
|--------|-------|-------------|---------|---------|
| `--port` | | Port number | 8501 | `--port 8080` |
| `--host` | | Host address | localhost | `--host 0.0.0.0` |

---

## 💾 Backup Command

### 🎯 Purpose
Create secure backups of firewall configurations before making changes.

### 📋 Basic Syntax
```bash
python main.py backup [OPTIONS]
```

### 🚀 Usage Examples

#### 💾 Backup System Configuration
```bash
sudo python main.py backup --input system --description "Production backup before optimization"
```

#### 📁 Backup Specific File
```bash
python main.py backup --input /path/to/rules.txt --description "Current configuration"
python main.py backup -i rules.txt -d "Before testing"
```

#### 🔄 Simple Backup
```bash
python main.py backup --input rules.txt
```

### 📊 Backup Output Example
```
ℹ 📡 Loading current system rules...
ℹ Creating backup...
✓ Backup created: backups/backup_20250726_143022.json
📋 Backup Details:
  📅 Created: 2025-07-26 14:30:22
  📝 Description: Production backup before optimization
  📊 Rules Count: 47
  🔒 File Size: 15.2 KB
────────────────────────────────────────
```

### 🎛️ Command Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--input` | `-i` | Input source | `--input system` |
| `--description` | `-d` | Backup description | `--description "Before changes"` |

---

## 🔄 Restore Command

### 🎯 Purpose
Restore firewall configuration from previously created backups.

### 📋 Basic Syntax
```bash
python main.py restore [OPTIONS]
```

### 🚀 Usage Examples

#### 🔄 View and Restore Backup
```bash
python main.py restore --backup /path/to/backup.json
```

#### ⚡ Restore and Apply to System
```bash
sudo python main.py restore --backup backup_20250726_143022.json --apply
```

### 📊 Restore Output Example
```
ℹ Loading backup: backups/backup_20250726_143022.json
📋 Backup Information:
  📅 Created: 2025-07-26 14:30:22
  📝 Description: Production backup before optimization  
  📊 Rules: 47 rules across 3 tables
  🔒 Integrity: ✓ Valid

⚠️  Ready to restore configuration. Continue? (y/N): y
✓ Configuration restored successfully!
────────────────────────────────────────
```

### 🎛️ Command Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--backup` | `-b` | Backup file path | `--backup backup.json` |
| `--apply` | | Apply to system | `--apply` |

---

## 🎨 CLI Visual Features

### 🌈 Color Coding System

#### 🔴 Red - Critical/Errors
- Critical security issues
- High-severity problems  
- Error messages
- Dangerous operations

#### 🟡 Yellow - Warnings/Medium
- Medium severity issues
- Warnings and cautions
- Moderate performance problems
- Configuration suggestions

#### 🟢 Green - Success/Good
- Good security scores
- Low severity issues  
- Success messages
- Completed operations

#### 🔵 Blue - Information
- Chain names
- Protocol information
- System information
- Process updates

#### 🟣 Purple - Highlights
- Rule numbers
- Special emphasis
- Key statistics
- Important values

#### 🟠 Cyan - Technical Data
- IP addresses  
- File paths
- URLs and links
- Technical details

### 🎨 Visual Elements

#### 📊 Progress Bars
```
Security Score.......... ████████████████████░░░░░░░░░░ 54.0%
Efficiency Score........ ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 5.0%
```

#### 📈 Bar Charts
```
Conflicting............. ████████████████████████████████ 15
Unreachable............. ██████████████████████████████   13  
Inefficient Order....... ████████████████████████         11
```

#### 🥧 Pie Charts
```
🔥 CRITICAL...... ███████████████████   41.7% (20)
🚨 HIGH.......... ████████████████      33.3% (16)  
⚠️  MEDIUM........ ██████████            20.8% (10)
💡 LOW........... ██                     4.2% (2)
```

#### 🎯 Priority Indicators
- 🔥 **Critical** - Immediate attention required
- 🚨 **High** - Should be addressed soon
- ⚠️ **Medium** - Address when convenient  
- 💡 **Low** - Optional improvements

#### 📋 Status Icons
- ✓ **Success** - Operation completed
- ✗ **Error** - Operation failed
- ⚠ **Warning** - Caution required
- ℹ **Info** - Information message
- 🔄 **Processing** - Operation in progress

---

## 📁 File Formats

### 📥 Input Formats

#### 🐧 iptables-save Format
```bash
# Standard Linux firewall export
iptables-save > rules.txt
python main.py analyze --input rules.txt
```

#### 📜 Plain Text Rules
```bash
# Human-readable iptables commands
python main.py analyze --input manual-rules.txt
```

#### 🖥️ Live System Rules
```bash
# Direct system query (Linux only)
sudo python main.py analyze --input system
```

### 📤 Output Formats

#### 📊 JSON Format
```bash
python main.py analyze --output report.json --format json
```
**Features:**
- Machine-readable
- API integration friendly
- Structured data
- Programming language support

#### 📝 Text Format  
```bash
python main.py analyze --output report.txt --format text
```
**Features:**
- Human-readable
- Terminal-friendly
- Colored output (when supported)
- Easy sharing

#### 🌐 HTML Format
```bash
python main.py analyze --output report.html --format html
```
**Features:**
- Interactive visualizations
- Professional presentation
- Shareable reports
- Charts and graphics

---

## 🛠️ Advanced Usage

### 🔧 Environment Variables
```bash
# Set log level
export FIREWALL_OPTIMIZER_LOG_LEVEL=DEBUG

# Custom config directory
export FIREWALL_OPTIMIZER_CONFIG_DIR=/path/to/configs

# Backup directory
export FIREWALL_OPTIMIZER_BACKUP_DIR=/custom/backups
```

### 📝 Configuration Files
```yaml
# config/settings.yaml
analysis:
  max_rules: 1000
  timeout: 300
  parallel_processing: true
  
visualization:
  chart_width: 800
  chart_height: 600
  theme: "dark"
  
security:
  require_backup: true
  dry_run_default: true
```

### 🔄 Batch Processing
```bash
# Process multiple files
for file in /etc/firewall/*.rules; do
    echo "Processing $file..."
    python main.py analyze --input "$file" --output "analysis_$(basename $file .rules).json"
done

# Generate summary report
python scripts/generate_summary.py --input analysis_*.json --output summary.html
```

### 🌐 Integration with Other Tools

#### 🔗 CI/CD Pipeline Integration
```yaml
# .github/workflows/firewall-check.yml
name: Firewall Analysis
on: [push, pull_request]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Analyze firewall rules
        run: python main.py analyze --input firewall/rules.txt --output analysis.json --format json
      - name: Upload analysis results
        uses: actions/upload-artifact@v2
        with:
          name: firewall-analysis
          path: analysis.json
```

#### 🐳 Docker Integration
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["python", "main.py", "webapp", "--host", "0.0.0.0"]
```

#### 📊 Monitoring Integration
```bash
# Export metrics to Prometheus
python main.py analyze --input system --output /metrics/firewall.json

# Send alerts to Slack
python scripts/alert_integration.py --analysis analysis.json --webhook $SLACK_WEBHOOK
```

### 🔒 Security Hardening
```bash
# Run in restricted environment
python main.py analyze --input rules.txt --dry-run --no-system-access

# Audit mode with full logging
python main.py optimize --input system --audit-mode --log-level DEBUG

# Validate before applying
python main.py optimize --input system --validate-only --output validation.json
```

---

## 🚨 Safety Features

### 🛡️ Built-in Protections

#### ✅ Dry-Run by Default
All commands run in safe mode by default - no system changes unless explicitly requested.

```bash
# Safe analysis (default)
python main.py analyze --input system

# Safe optimization (generates recommendations only)
python main.py optimize --input system

# Explicit dry-run
python main.py optimize --input system --dry-run
```

#### 💾 Automatic Backups
System changes require backups to be created first.

```bash
# Backup created automatically
sudo python main.py optimize --input system --apply --backup

# Manual backup first
sudo python main.py backup --input system --description "Before changes"
sudo python main.py optimize --input system --apply
```

#### 🔍 Validation Checks
All rules are validated before application.

```bash
# Validation output example
✓ Syntax validation passed
✓ Logic validation passed  
✓ Security validation passed
⚠ Performance warning: Rule order could be optimized
✓ Ready to apply changes
```

#### 📝 Audit Logging
All operations are logged for security and troubleshooting.

```bash
# Log locations
~/.firewall-optimizer/logs/operations.log
~/.firewall-optimizer/logs/security.log
~/.firewall-optimizer/logs/changes.log
```

#### 🔒 Permission Checks
System operations require appropriate privileges.

```bash
# Root required for system changes
sudo python main.py optimize --input system --apply

# User operations work without root
python main.py analyze --input rules.txt
```

### 🛡️ Best Practices

#### 1. 💾 Always Backup First
```bash
# CORRECT: Backup before changes
sudo python main.py backup --input system --description "Before optimization"
sudo python main.py optimize --input system --apply

# BETTER: Automatic backup
sudo python main.py optimize --input system --apply --backup
```

#### 2. 🧪 Test in Staging First
```bash
# Test on staging environment
python main.py analyze --input staging-rules.txt
python main.py optimize --input staging-rules.txt --output optimized-staging.txt

# Apply to staging
sudo python main.py restore --backup optimized-staging.txt --apply

# Test thoroughly, then apply to production
```

#### 3. 📊 Review Recommendations
```bash
# Review before applying
python main.py optimize --input system > recommendations.txt
less recommendations.txt

# Apply selectively
sudo python main.py optimize --input system --apply --interactive
```

#### 4. 📝 Monitor Changes
```bash
# Enable detailed logging
export FIREWALL_OPTIMIZER_LOG_LEVEL=INFO
python main.py optimize --input system --apply --backup

# Monitor logs
tail -f ~/.firewall-optimizer/logs/operations.log
```

#### 5. 🔄 Keep Backups
```bash
# Organize backups
mkdir -p /backup/firewall/$(date +%Y%m%d)
python main.py backup --input system --description "Daily backup"

# Retention policy
find /backup/firewall -type f -mtime +30 -delete
```

---

## 🐛 Troubleshooting

### 🔍 Common Issues & Solutions

#### ❌ Permission Denied
```bash
# Problem
python main.py analyze --input system
# Error: Permission denied

# Solution
sudo python main.py analyze --input system
```

#### ❌ Module Not Found
```bash
# Problem  
python main.py analyze
# Error: ModuleNotFoundError: No module named 'optimizer'

# Solution
pip install -r requirements.txt
# or
python -m pip install -r requirements.txt
```

#### ❌ Port Already in Use
```bash
# Problem
python main.py webapp
# Error: Port 8501 is already in use

# Solution
python main.py webapp --port 8080
# or find and kill process using port
lsof -i :8501
kill -9 <PID>
```

#### ❌ Visualization Dependencies Missing
```bash
# Problem
python main.py visualize
# Warning: Plotly not available for visualizations

# Solution
pip install plotly matplotlib networkx seaborn
```

#### ❌ Rich/CLI Graphics Not Working
```bash
# Problem
python main.py analyze
# Warning: Rich library not available for progress bars

# Solution  
pip install rich plotext colorama
```

### 🔧 Debug Commands

#### 🔍 Check System Dependencies
```bash
# Verify Python version
python --version

# Check installed packages
pip list | grep -E "(streamlit|plotly|rich|colorama)"

# Test optimizer import
python -c "import optimizer; print('✓ Optimizer module loaded successfully')"

# Check file permissions
ls -la data/sample_rules.txt
```

#### 📊 Enable Debug Mode
```bash
# Verbose output
python main.py analyze --verbose

# Debug logging
export FIREWALL_OPTIMIZER_LOG_LEVEL=DEBUG
python main.py analyze --input system

# Trace mode
python -u main.py analyze --input system 2>&1 | tee debug.log
```

#### 🧪 Test Installation
```bash
# Run installation test
python test_installation.py

# Verify sample data
python -c "
import os
if os.path.exists('data/sample_rules.txt'):
    print('✓ Sample data found')
    with open('data/sample_rules.txt') as f:
        lines = len(f.readlines())
    print(f'✓ Sample rules: {lines} lines')
else:
    print('✗ Sample data missing')
"
```

### 🆘 Getting Help

#### 📚 Built-in Help
```bash
# General help
python main.py --help

# Command-specific help
python main.py analyze --help
python main.py optimize --help
python main.py visualize --help
python main.py webapp --help

# Version information
python main.py --version
```

#### 🌐 Online Resources
- 📖 **Documentation**: [README.md](README.md)
- 🚀 **Quick Reference**: [QUICK-REFERENCE.md](QUICK-REFERENCE.md)
- 🐛 **Issue Tracker**: GitHub Issues
- 💬 **Community**: GitHub Discussions

#### 🔧 System Information
```bash
# Collect system info for support
echo "=== System Information ===" > system-info.txt
python --version >> system-info.txt
pip --version >> system-info.txt
echo "=== Installed Packages ===" >> system-info.txt
pip list >> system-info.txt
echo "=== OS Information ===" >> system-info.txt
uname -a >> system-info.txt
```

---

<div align="center">

## 🎉 Congratulations!

You now have complete mastery of the **AI-Powered Firewall Rule Optimizer**!

```
🔥 Start optimizing your firewall security today! 🔥
```

### 📞 Support & Community

[![GitHub](https://img.shields.io/badge/GitHub-Issues-black.svg)](https://github.com)
[![Docs](https://img.shields.io/badge/Docs-Complete-blue.svg)](README.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

*Made with ❤️ for cybersecurity professionals*

</div>
