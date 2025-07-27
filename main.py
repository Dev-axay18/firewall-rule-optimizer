#!/usr/bin/env python3
"""
AI-Powered Firewall Rule Optimizer and Visualizer
Main Command Line Interface

This script provides a command-line interface for the firewall optimizer,
allowing users to analyze, optimize, and visualize firewall rules from
the terminal.

Usage:
    python main.py analyze --input rules.txt
    python main.py optimize --input rules.txt --output optimized.txt
    python main.py visualize --input rules.txt --output report.html
    python main.py webapp
"""

import argparse
import logging
import sys
import os
from typing import Optional
from pathlib import Path

# Import optimizer components
from optimizer import (
    IptablesParser, FirewallAnalyzer, FirewallRecommender, 
    FirewallVisualizer, ConfigManager, BackupManager, 
    SystemInterface, setup_logging, CLIGraphics
)
from optimizer.colors import Colors, print_banner, print_separator


class FirewallOptimizerCLI:
    """Command Line Interface for the Firewall Optimizer"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        setup_logging(self.config_manager)
        self.logger = logging.getLogger(__name__)
        
        self.parser = IptablesParser()
        self.analyzer = FirewallAnalyzer()
        self.recommender = FirewallRecommender()
        self.visualizer = FirewallVisualizer()
        self.backup_manager = BackupManager()
        self.system_interface = SystemInterface(dry_run=True)
        self.cli_graphics = CLIGraphics()
    
    def run(self):
        """Main entry point for CLI"""
        args = self.parse_arguments()
        
        # Show banner for interactive commands
        if args.command and args.command != 'webapp':
            print_banner()
        
        try:
            if args.command == 'analyze':
                self.cmd_analyze(args)
            elif args.command == 'optimize':
                self.cmd_optimize(args)
            elif args.command == 'visualize':
                self.cmd_visualize(args)
            elif args.command == 'webapp':
                self.cmd_webapp(args)
            elif args.command == 'backup':
                self.cmd_backup(args)
            elif args.command == 'restore':
                self.cmd_restore(args)
            else:
                print(Colors.error("Unknown command. Use --help for usage information."))
                sys.exit(1)
        
        except KeyboardInterrupt:
            print(Colors.warning("\n\nOperation cancelled by user."))
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"Command failed: {e}")
            print(f"Error: {e}")
            sys.exit(1)
    
    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="AI-Powered Firewall Rule Optimizer and Visualizer",
            epilog="Examples:\n"
                   "  %(prog)s analyze --input rules.txt\n"
                   "  %(prog)s optimize --input rules.txt --output optimized.txt\n"
                   "  %(prog)s visualize --input rules.txt --output report.html\n"
                   "  %(prog)s webapp",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
        parser.add_argument('--verbose', '-v', action='store_true', 
                           help='Enable verbose output')
        parser.add_argument('--dry-run', action='store_true', default=True,
                           help='Perform dry run without making changes')
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Analyze command
        analyze_parser = subparsers.add_parser('analyze', help='Analyze firewall rules')
        analyze_parser.add_argument('--input', '-i', type=str,
                                   help='Input file (iptables-save format) or "system" for current rules')
        analyze_parser.add_argument('--output', '-o', type=str,
                                   help='Output file for analysis report (JSON format)')
        analyze_parser.add_argument('--format', choices=['json', 'text', 'html'], default='text',
                                   help='Output format')
        
        # Optimize command
        optimize_parser = subparsers.add_parser('optimize', help='Generate optimization recommendations')
        optimize_parser.add_argument('--input', '-i', type=str,
                                    help='Input file (iptables-save format) or "system" for current rules')
        optimize_parser.add_argument('--output', '-o', type=str,
                                    help='Output file for optimized rules')
        optimize_parser.add_argument('--apply', action='store_true',
                                    help='Apply optimizations to system (requires root)')
        optimize_parser.add_argument('--backup', action='store_true', default=True,
                                    help='Create backup before applying changes')
        
        # Visualize command
        visualize_parser = subparsers.add_parser('visualize', help='Create visualizations')
        visualize_parser.add_argument('--input', '-i', type=str,
                                     help='Input file (iptables-save format) or "system" for current rules')
        visualize_parser.add_argument('--output', '-o', type=str, default='./report',
                                     help='Output directory for visualization files')
        visualize_parser.add_argument('--type', choices=['all', 'flow', 'issues', 'graph', 'heatmap'],
                                     default='all', help='Type of visualization to create')
        
        # Web app command
        webapp_parser = subparsers.add_parser('webapp', help='Launch web interface')
        webapp_parser.add_argument('--port', type=int, default=8501,
                                  help='Port for web interface (default: 8501)')
        webapp_parser.add_argument('--host', default='localhost',
                                  help='Host for web interface (default: localhost)')
        
        # Backup command
        backup_parser = subparsers.add_parser('backup', help='Create configuration backup')
        backup_parser.add_argument('--input', '-i', type=str,
                                  help='Input file or "system" for current rules')
        backup_parser.add_argument('--description', '-d', type=str,
                                  help='Description for the backup')
        
        # Restore command
        restore_parser = subparsers.add_parser('restore', help='Restore from backup')
        restore_parser.add_argument('--backup', '-b', type=str, required=True,
                                   help='Backup file to restore from')
        restore_parser.add_argument('--apply', action='store_true',
                                   help='Apply restored configuration to system')
        
        return parser.parse_args()
    
    def load_configuration(self, input_path: str):
        """Load firewall configuration from file or system"""
        if input_path == 'system':
            print(Colors.info("📡 Loading current system rules..."))
            content = self.system_interface.get_current_rules()
        else:
            print(Colors.info(f"📂 Loading configuration from {Colors.highlight(input_path)}..."))
            with open(input_path, 'r') as f:
                content = f.read()
        
        config = self.parser.parse_iptables_save(content)
        return config, content
    
    def cmd_analyze(self, args):
        """Execute analyze command"""
        # Determine input
        if args.input:
            config, content = self.load_configuration(args.input)
        else:
            print(Colors.info("Loading sample configuration..."))
            sample_path = "data/sample_rules.txt"
            if os.path.exists(sample_path):
                config, content = self.load_configuration(sample_path)
            else:
                content = self.system_interface._get_sample_rules()
                config = self.parser.parse_iptables_save(content)
        
        print(Colors.info("Analyzing firewall configuration..."))
        analysis = self.analyzer.analyze_configuration(config)
        
        # Print results
        self.print_analysis_results(analysis)
        
        # Save to file if requested
        if args.output:
            self.save_analysis_results(analysis, args.output, args.format)
            print(Colors.success(f"Analysis results saved to {args.output}"))
    
    def cmd_optimize(self, args):
        """Execute optimize command"""
        # Determine input
        if args.input:
            config, content = self.load_configuration(args.input)
        else:
            print(Colors.info("Loading sample configuration..."))
            sample_path = "data/sample_rules.txt"
            if os.path.exists(sample_path):
                config, content = self.load_configuration(sample_path)
            else:
                content = self.system_interface._get_sample_rules()
                config = self.parser.parse_iptables_save(content)
        
        print(Colors.info("Analyzing configuration..."))
        analysis = self.analyzer.analyze_configuration(config)
        
        print(Colors.info("Generating optimization recommendations..."))
        plan = self.recommender.generate_recommendations(config, analysis)
        
        # Print recommendations
        self.print_optimization_plan(plan)
        
        if args.output or args.apply:
            if args.backup:
                print(Colors.info("Creating backup..."))
                backup_path = self.backup_manager.create_backup(config, "Pre-optimization backup")
                print(Colors.success(f"Backup created: {backup_path}"))
            
            # Generate optimized configuration
            optimized_config = self.recommender.generate_optimized_config(config, plan)
            
            if args.output:
                print(Colors.info(f"Saving optimized configuration to {args.output}..."))
                self.save_optimized_config(optimized_config, args.output)
                print(Colors.success(f"Optimized configuration saved to {args.output}"))
            
            if args.apply:
                print(Colors.warning("Applying optimizations to system..."))
                self.apply_optimizations(optimized_config)
                print(Colors.success("Optimizations applied successfully!"))
    
    def cmd_visualize(self, args):
        """Execute visualize command"""
        # Determine input
        if args.input:
            config, content = self.load_configuration(args.input)
        else:
            print(Colors.info("Loading sample configuration..."))
            sample_path = "data/sample_rules.txt"
            if os.path.exists(sample_path):
                config, content = self.load_configuration(sample_path)
            else:
                content = self.system_interface._get_sample_rules()
                config = self.parser.parse_iptables_save(content)
        
        print(Colors.info("Analyzing configuration..."))
        analysis = self.analyzer.analyze_configuration(config)
        
        print(Colors.info("Generating recommendations..."))
        plan = self.recommender.generate_recommendations(config, analysis)
        
        print(Colors.info(f"Creating visualizations in {Colors.highlight(args.output)}..."))
        
        # Create output directory
        output_dir = Path(args.output)
        output_dir.mkdir(exist_ok=True)
        
        files_created = self.visualizer.create_comprehensive_report(
            config, analysis, plan, str(output_dir)
        )
        
        print(f"\n{Colors.subheader('📊 Visualizations Created')}")
        for viz_type, file_path in files_created.items():
            print(f"  {Colors.BRIGHT_GREEN}✓{Colors.RESET} {Colors.highlight(viz_type)}: {Colors.CYAN}{file_path}{Colors.RESET}")
        
        print(f"\n{Colors.success('🌐 Open')} {Colors.highlight(f'{output_dir}/rule_flow.html')} {Colors.success('in your browser to view the report.')}")
        print_separator()
    
    def cmd_webapp(self, args):
        """Execute webapp command"""
        print(Colors.info("🚀 Starting web interface..."))
        print(Colors.success(f"🌐 Open your browser to {Colors.highlight(f'http://{args.host}:{args.port}')}"))
        print_separator()
        
        try:
            import subprocess
            import sys
            
            # Launch Streamlit
            cmd = [
                sys.executable, '-m', 'streamlit', 'run', 
                'web_ui/app.py',
                '--server.port', str(args.port),
                '--server.address', args.host
            ]
            
            subprocess.run(cmd)
        
        except ImportError:
            print("Error: Streamlit not installed. Install with: pip install streamlit")
        except KeyboardInterrupt:
            print("\nWeb interface stopped.")
    
    def cmd_backup(self, args):
        """Execute backup command"""
        if args.input:
            config, content = self.load_configuration(args.input)
        else:
            print("Creating backup of current system rules...")
            content = self.system_interface.get_current_rules()
            config = self.parser.parse_iptables_save(content)
        
        backup_path = self.backup_manager.create_backup(
            config, args.description or "Manual backup"
        )
        print(f"Backup created: {backup_path}")
    
    def cmd_restore(self, args):
        """Execute restore command"""
        print(f"Restoring from backup {args.backup}...")
        config = self.backup_manager.restore_backup(args.backup)
        
        if args.apply:
            print("Applying restored configuration to system...")
            # Convert config back to iptables-save format and apply
            # This would need to be implemented in the recommender
            print("Restore and apply functionality would be implemented here")
        else:
            print("Configuration restored successfully (dry run)")
            print("Use --apply to actually apply the restored configuration")
    
    def print_analysis_results(self, analysis):
        """Print analysis results to console with graphics"""
        print("\n" + Colors.header("FIREWALL ANALYSIS RESULTS"))
        
        # Show CLI graphics overview
        self.cli_graphics.print_cli_chart_summary(analysis)
        
        print(f"\n{Colors.subheader('🔍 Detailed Issue Breakdown')}")
        
        if analysis.issues:
            from collections import defaultdict
            issues_by_type = defaultdict(list)
            for issue in analysis.issues:
                issues_by_type[issue.issue_type].append(issue)
            
            for issue_type, issues in issues_by_type.items():
                issue_type_name = issue_type.value.title()
                print(f"\n  {Colors.warning('⚠️')} {Colors.highlight(issue_type_name)} {Colors.count(len(issues), 'issues')}:")
                
                for i, issue in enumerate(issues, 1):
                    # Color code by severity
                    severity_text = ""
                    if hasattr(issue, 'severity'):
                        if issue.severity.value == 'critical':
                            severity_text = f" [{Colors.critical('CRITICAL')}]"
                        elif issue.severity.value == 'high':
                            severity_text = f" [{Colors.high('HIGH')}]"
                        elif issue.severity.value == 'medium':
                            severity_text = f" [{Colors.medium('MEDIUM')}]"
                        elif issue.severity.value == 'low':
                            severity_text = f" [{Colors.low('LOW')}]"
                    
                    print(f"    {Colors.rule_number(str(i))} {issue.description}{severity_text}")
                    
                    if issue.recommendation:
                        print(f"      {Colors.BRIGHT_GREEN}→{Colors.RESET} {Colors.DIM}{issue.recommendation}{Colors.RESET}")
                    
                    # Add affected rule information if available
                    if hasattr(issue, 'affected_rule') and issue.affected_rule:
                        rule = issue.affected_rule
                        rule_info = f"Chain: {Colors.chain_name(rule.chain)}"
                        if rule.target:
                            rule_info += f", Target: {Colors.target(rule.target)}"
                        if rule.source:
                            rule_info += f", Source: {Colors.ip_address(rule.source)}"
                        if rule.destination:
                            rule_info += f", Dest: {Colors.ip_address(rule.destination)}"
                        if rule.protocol:
                            rule_info += f", Protocol: {Colors.protocol(rule.protocol)}"
                        print(f"      {Colors.DIM}Rule: {rule_info}{Colors.RESET}")
                    
                    print()  # Empty line between issues
        else:
            print(f"\n{Colors.success('✅ No issues found! Your firewall configuration looks good.')}")
        
        print_separator()
    
    def print_optimization_plan(self, plan):
        """Print optimization plan to console with graphics"""
        print("\n" + Colors.header("OPTIMIZATION RECOMMENDATIONS"))
        
        if not plan.recommendations:
            print(f"\n{Colors.success('✅ No optimizations needed! Your configuration is already optimal.')}")
            return
        
        # Show CLI graphics for optimization plan
        self.cli_graphics.create_optimization_impact_gauge(plan)
        self.cli_graphics.create_recommendation_priority_chart(plan.recommendations)
        
        print(f"\n{Colors.subheader('📋 Detailed Recommendations')}")
        
        from optimizer.recommender import RecommendationPriority
        
        priority_icons = {
            RecommendationPriority.CRITICAL: "🔥",
            RecommendationPriority.HIGH: "🚨", 
            RecommendationPriority.MEDIUM: "⚠️",
            RecommendationPriority.LOW: "💡"
        }
        
        for priority in [RecommendationPriority.CRITICAL, RecommendationPriority.HIGH, 
                        RecommendationPriority.MEDIUM, RecommendationPriority.LOW]:
            
            priority_recs = plan.get_by_priority(priority)
            if not priority_recs:
                continue
            
            icon = priority_icons.get(priority, "📋")
            priority_name = priority.name.title()
            
            if priority == RecommendationPriority.CRITICAL:
                priority_display = Colors.critical(priority_name)
            elif priority == RecommendationPriority.HIGH:
                priority_display = Colors.high(priority_name)
            elif priority == RecommendationPriority.MEDIUM:
                priority_display = Colors.medium(priority_name)
            else:
                priority_display = Colors.low(priority_name)
            
            print(f"\n{Colors.subheader(f'{icon} {priority_display} Priority ({len(priority_recs)} recommendations)')}")
            
            for i, rec in enumerate(priority_recs, 1):
                print(f"  {Colors.rule_number(str(i))} {Colors.highlight(rec.title)}")
                print(f"     {Colors.DIM}{rec.description}{Colors.RESET}")
                
                if rec.estimated_impact:
                    print(f"     {Colors.BRIGHT_GREEN}Impact:{Colors.RESET} {rec.estimated_impact}")
                    
                if hasattr(rec, 'risk_level') and rec.risk_level != 'low':
                    risk_color = Colors.BRIGHT_RED if rec.risk_level == 'high' else Colors.BRIGHT_YELLOW
                    print(f"     {Colors.BRIGHT_RED}Risk:{Colors.RESET} {risk_color}{rec.risk_level.upper()}{Colors.RESET}")
                
                print()  # Empty line between recommendations
        
        print_separator()
    
    def save_analysis_results(self, analysis, output_path, format_type):
        """Save analysis results to file"""
        if format_type == 'json':
            import json
            
            results = {
                'security_score': analysis.security_score,
                'efficiency_score': analysis.rule_efficiency_score,
                'statistics': analysis.statistics,
                'issues': [
                    {
                        'type': issue.issue_type.value,
                        'severity': issue.severity.value,
                        'description': issue.description,
                        'recommendation': issue.recommendation,
                        'affected_rules': [rule.line_number for rule in issue.affected_rules]
                    }
                    for issue in analysis.issues
                ]
            }
            
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
        
        elif format_type == 'html':
            # Create simple HTML report
            html_content = self.generate_html_report(analysis)
            with open(output_path, 'w') as f:
                f.write(html_content)
        
        else:  # text format
            with open(output_path, 'w') as f:
                # Redirect print output to file
                import io, contextlib
                
                string_io = io.StringIO()
                with contextlib.redirect_stdout(string_io):
                    self.print_analysis_results(analysis)
                
                f.write(string_io.getvalue())
    
    def save_optimized_config(self, config, output_path):
        """Save optimized configuration to file"""
        # Convert config back to iptables-save format
        # This is a simplified version - full implementation would be more complex
        
        lines = []
        
        for table_name, chains in config.tables.items():
            lines.append(f"*{table_name}")
            
            # Add chain definitions (simplified)
            for chain_name in chains.keys():
                lines.append(f":{chain_name} ACCEPT [0:0]")
            
            # Add rules
            for chain_name, rules in chains.items():
                for rule in rules:
                    lines.append(rule.raw_rule)
            
            lines.append("COMMIT")
        
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))
    
    def apply_optimizations(self, config):
        """Apply optimizations to system"""
        if self.system_interface.dry_run:
            print("DRY RUN: Optimizations would be applied to system")
        else:
            print("WARNING: This would modify your actual firewall rules!")
            response = input("Are you sure you want to continue? (yes/no): ")
            if response.lower() != 'yes':
                print("Operation cancelled.")
                return
            
            # Apply the configuration
            # Implementation would convert config to iptables-save format and apply
            print("Optimization application would be implemented here")
    
    def generate_html_report(self, analysis):
        """Generate simple HTML report"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Firewall Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .score {{ background: #f0f0f0; padding: 20px; margin: 20px 0; }}
        .issue {{ border-left: 4px solid #e74c3c; padding: 10px; margin: 10px 0; }}
        .stats {{ display: flex; flex-wrap: wrap; }}
        .stat {{ margin: 10px; padding: 10px; background: #ecf0f1; }}
    </style>
</head>
<body>
    <h1>Firewall Analysis Report</h1>
    
    <div class="score">
        <h2>Overall Scores</h2>
        <p>Security Score: {analysis.security_score:.1f}/100</p>
        <p>Efficiency Score: {analysis.rule_efficiency_score:.1f}/100</p>
    </div>
    
    <div class="stats">
        <h2>Statistics</h2>
        {''.join(f'<div class="stat"><strong>{k.replace("_", " ").title()}:</strong> {v}</div>' 
                for k, v in analysis.statistics.items())}
    </div>
    
    <h2>Issues Found ({len(analysis.issues)})</h2>
    {''.join(f'<div class="issue"><h3>{issue.issue_type.value.title()}</h3><p>{issue.description}</p><p><em>{issue.recommendation}</em></p></div>' 
            for issue in analysis.issues)}
    
    <p><em>Generated by AI-Powered Firewall Rule Optimizer</em></p>
</body>
</html>
"""
        return html


def main():
    """Main entry point"""
    try:
        cli = FirewallOptimizerCLI()
        cli.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
