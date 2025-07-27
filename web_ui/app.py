"""
Streamlit Web UI for AI-Powered Firewall Rule Optimizer

This module provides a user-friendly web interface for the firewall optimizer
using Streamlit. Users can upload firewall configurations, view analysis results,
explore recommendations, and visualize their firewall rules.
"""

# Check if Streamlit is available
try:
    import streamlit as st
    import pandas as pd
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    print("Streamlit not available. Web interface disabled.")
    print("Install with: pip install streamlit pandas")

import os
import tempfile
import io
from typing import Optional, Dict, Any
import logging

# Import optimizer components
try:
    from optimizer import (
        IptablesParser, FirewallAnalyzer, FirewallRecommender, 
        FirewallVisualizer, ConfigManager, BackupManager, SystemInterface
    )
except ImportError:
    # Fallback for development
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from optimizer import (
        IptablesParser, FirewallAnalyzer, FirewallRecommender, 
        FirewallVisualizer, ConfigManager, BackupManager, SystemInterface
    )


class FirewallOptimizerApp:
    """Main Streamlit application class"""
    
    def __init__(self):
        self.setup_page_config()
        self.setup_session_state()
        self.setup_components()
    
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Firewall Rule Optimizer",
            page_icon="🔥",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def setup_session_state(self):
        """Initialize session state variables"""
        if 'config' not in st.session_state:
            st.session_state.config = None
        if 'analysis' not in st.session_state:
            st.session_state.analysis = None
        if 'recommendations' not in st.session_state:
            st.session_state.recommendations = None
        if 'current_rules' not in st.session_state:
            st.session_state.current_rules = ""
    
    def setup_components(self):
        """Initialize optimizer components"""
        self.parser = IptablesParser()
        self.analyzer = FirewallAnalyzer()
        self.recommender = FirewallRecommender()
        self.visualizer = FirewallVisualizer()
        self.config_manager = ConfigManager()
        self.backup_manager = BackupManager()
        self.system_interface = SystemInterface(dry_run=True)
    
    def run(self):
        """Main application entry point"""
        self.render_header()
        self.render_sidebar()
        self.render_main_content()
    
    def render_header(self):
        """Render application header"""
        st.title("🔥 AI-Powered Firewall Rule Optimizer")
        st.markdown("""
        **Analyze, optimize, and visualize your iptables firewall rules with AI-powered insights.**
        
        This tool helps you identify redundant rules, security vulnerabilities, and optimization opportunities
        in your firewall configuration.
        """)
        
        # Status indicators
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.session_state.config:
                st.success("✅ Configuration Loaded")
            else:
                st.info("📄 No Configuration")
        
        with col2:
            if st.session_state.analysis:
                st.success("✅ Analysis Complete")
            else:
                st.info("🔍 No Analysis")
        
        with col3:
            if st.session_state.recommendations:
                st.success("✅ Recommendations Ready")
            else:
                st.info("💡 No Recommendations")
        
        with col4:
            backups = self.backup_manager.list_backups()
            st.info(f"💾 {len(backups)} Backups")
    
    def render_sidebar(self):
        """Render sidebar with navigation and controls"""
        st.sidebar.title("Navigation")
        
        # File upload section
        st.sidebar.header("📁 Load Configuration")
        
        upload_method = st.sidebar.radio(
            "Choose input method:",
            ["Upload File", "Paste Text", "Load from System", "Use Sample"]
        )
        
        if upload_method == "Upload File":
            self.handle_file_upload()
        elif upload_method == "Paste Text":
            self.handle_text_input()
        elif upload_method == "Load from System":
            self.handle_system_load()
        elif upload_method == "Use Sample":
            self.handle_sample_load()
        
        # Analysis controls
        st.sidebar.header("🔍 Analysis Options")
        
        if st.sidebar.button("🚀 Run Analysis", disabled=not st.session_state.config):
            self.run_analysis()
        
        if st.sidebar.button("💡 Generate Recommendations", 
                           disabled=not st.session_state.analysis):
            self.generate_recommendations()
        
        # Backup controls
        st.sidebar.header("💾 Backup Management")
        
        if st.sidebar.button("Create Backup", disabled=not st.session_state.config):
            self.create_backup()
        
        self.show_backup_list()
        
        # Settings
        st.sidebar.header("⚙️ Settings")
        
        dry_run = st.sidebar.checkbox("Dry Run Mode", value=True)
        self.system_interface.dry_run = dry_run
        
        if st.sidebar.button("Reset Session"):
            self.reset_session()
    
    def render_main_content(self):
        """Render main content area"""
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Overview", "🔍 Analysis", "💡 Recommendations", 
            "📊 Visualizations", "⚙️ Configuration"
        ])
        
        with tab1:
            self.render_overview_tab()
        
        with tab2:
            self.render_analysis_tab()
        
        with tab3:
            self.render_recommendations_tab()
        
        with tab4:
            self.render_visualizations_tab()
        
        with tab5:
            self.render_configuration_tab()
    
    def handle_file_upload(self):
        """Handle file upload"""
        uploaded_file = st.sidebar.file_uploader(
            "Choose iptables-save file",
            type=['txt', 'conf', 'rules'],
            help="Upload output from 'iptables-save' command"
        )
        
        if uploaded_file is not None:
            try:
                content = uploaded_file.read().decode('utf-8')
                self.load_configuration(content)
                st.sidebar.success("✅ File loaded successfully!")
            except Exception as e:
                st.sidebar.error(f"❌ Error loading file: {e}")
    
    def handle_text_input(self):
        """Handle text input"""
        rules_text = st.sidebar.text_area(
            "Paste iptables rules:",
            height=150,
            placeholder="Paste the output of 'iptables-save' here..."
        )
        
        if st.sidebar.button("Load Rules"):
            if rules_text.strip():
                try:
                    self.load_configuration(rules_text)
                    st.sidebar.success("✅ Rules loaded successfully!")
                except Exception as e:
                    st.sidebar.error(f"❌ Error loading rules: {e}")
            else:
                st.sidebar.warning("⚠️ Please enter some rules first")
    
    def handle_system_load(self):
        """Handle loading from system"""
        if st.sidebar.button("Load Current System Rules"):
            try:
                with st.spinner("Loading system rules..."):
                    rules_content = self.system_interface.get_current_rules()
                    self.load_configuration(rules_content)
                    st.sidebar.success("✅ System rules loaded!")
            except Exception as e:
                st.sidebar.error(f"❌ Error loading system rules: {e}")
    
    def handle_sample_load(self):
        """Handle loading sample configuration"""
        if st.sidebar.button("Load Sample Configuration"):
            try:
                sample_path = os.path.join("data", "sample_rules.txt")
                if os.path.exists(sample_path):
                    with open(sample_path, 'r') as f:
                        content = f.read()
                    self.load_configuration(content)
                    st.sidebar.success("✅ Sample configuration loaded!")
                else:
                    # Use built-in sample
                    sample_rules = self.system_interface._get_sample_rules()
                    self.load_configuration(sample_rules)
                    st.sidebar.success("✅ Sample configuration loaded!")
            except Exception as e:
                st.sidebar.error(f"❌ Error loading sample: {e}")
    
    def load_configuration(self, content: str):
        """Load firewall configuration from content"""
        try:
            config = self.parser.parse_iptables_save(content)
            st.session_state.config = config
            st.session_state.current_rules = content
            # Reset dependent state
            st.session_state.analysis = None
            st.session_state.recommendations = None
        except Exception as e:
            st.error(f"Failed to parse configuration: {e}")
            raise
    
    def run_analysis(self):
        """Run firewall analysis"""
        try:
            with st.spinner("Analyzing firewall configuration..."):
                analysis = self.analyzer.analyze_configuration(st.session_state.config)
                st.session_state.analysis = analysis
            st.success("✅ Analysis completed!")
        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")
    
    def generate_recommendations(self):
        """Generate optimization recommendations"""
        try:
            with st.spinner("Generating recommendations..."):
                recommendations = self.recommender.generate_recommendations(
                    st.session_state.config, st.session_state.analysis
                )
                st.session_state.recommendations = recommendations
            st.success("✅ Recommendations generated!")
        except Exception as e:
            st.error(f"❌ Recommendation generation failed: {e}")
    
    def create_backup(self):
        """Create configuration backup"""
        try:
            description = st.text_input("Backup description (optional):")
            backup_path = self.backup_manager.create_backup(
                st.session_state.config, description
            )
            st.success(f"✅ Backup created: {os.path.basename(backup_path)}")
        except Exception as e:
            st.error(f"❌ Backup creation failed: {e}")
    
    def show_backup_list(self):
        """Show list of available backups"""
        backups = self.backup_manager.list_backups()
        
        if backups:
            st.sidebar.write("Available backups:")
            for backup in backups[:5]:  # Show last 5 backups
                if st.sidebar.button(
                    f"📄 {backup['timestamp']}", 
                    key=f"backup_{backup['filename']}"
                ):
                    try:
                        config = self.backup_manager.restore_backup(backup['path'])
                        st.session_state.config = config
                        st.sidebar.success("✅ Backup restored!")
                        st.rerun()
                    except Exception as e:
                        st.sidebar.error(f"❌ Restore failed: {e}")
    
    def reset_session(self):
        """Reset session state"""
        for key in ['config', 'analysis', 'recommendations', 'current_rules']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    def render_overview_tab(self):
        """Render overview tab"""
        if not st.session_state.config:
            st.info("👆 Please load a firewall configuration using the sidebar to get started.")
            return
        
        config = st.session_state.config
        
        st.header("📋 Configuration Overview")
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        total_rules = sum(len(rules) for chains in config.tables.values() 
                         for rules in chains.values())
        total_chains = sum(len(chains) for chains in config.tables.values())
        total_tables = len(config.tables)
        
        with col1:
            st.metric("Total Rules", total_rules)
        with col2:
            st.metric("Total Chains", total_chains)
        with col3:
            st.metric("Total Tables", total_tables)
        with col4:
            if st.session_state.analysis:
                st.metric("Issues Found", len(st.session_state.analysis.issues))
            else:
                st.metric("Issues Found", "—")
        
        # Tables breakdown
        st.subheader("Tables and Chains")
        
        for table_name, chains in config.tables.items():
            with st.expander(f"📊 Table: {table_name}"):
                for chain_name, rules in chains.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{chain_name}**")
                    with col2:
                        st.write(f"{len(rules)} rules")
                    
                    if rules:
                        # Show first few rules
                        for i, rule in enumerate(rules[:3]):
                            st.code(rule.raw_rule, language='bash')
                        
                        if len(rules) > 3:
                            st.write(f"... and {len(rules) - 3} more rules")
        
        # Raw configuration
        with st.expander("📄 Raw Configuration"):
            st.code(st.session_state.current_rules, language='bash')
    
    def render_analysis_tab(self):
        """Render analysis tab"""
        if not st.session_state.analysis:
            if st.session_state.config:
                st.info("👆 Click 'Run Analysis' in the sidebar to analyze your configuration.")
            else:
                st.info("Please load a configuration first.")
            return
        
        analysis = st.session_state.analysis
        
        st.header("🔍 Analysis Results")
        
        # Overall scores
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Security Score",
                f"{analysis.security_score:.1f}/100",
                delta=f"{analysis.security_score - 80:.1f}" if analysis.security_score < 80 else None
            )
        
        with col2:
            st.metric(
                "Efficiency Score", 
                f"{analysis.rule_efficiency_score:.1f}/100",
                delta=f"{analysis.rule_efficiency_score - 80:.1f}" if analysis.rule_efficiency_score < 80 else None
            )
        
        # Issues summary
        if analysis.issues:
            st.subheader("🚨 Issues Found")
            
            # Group issues by type
            from collections import defaultdict
            issues_by_type = defaultdict(list)
            for issue in analysis.issues:
                issues_by_type[issue.issue_type].append(issue)
            
            for issue_type, issues in issues_by_type.items():
                with st.expander(f"{issue_type.value.title()} ({len(issues)} issues)"):
                    for issue in issues:
                        severity_color = {
                            'low': '🟢',
                            'medium': '🟡', 
                            'high': '🟠',
                            'critical': '🔴'
                        }.get(issue.severity.value, '⚪')
                        
                        st.write(f"{severity_color} **{issue.severity.value.title()}**: {issue.description}")
                        if issue.recommendation:
                            st.write(f"💡 *Recommendation: {issue.recommendation}*")
                        
                        if issue.affected_rules:
                            st.write("**Affected Rules:**")
                            for rule in issue.affected_rules:
                                st.code(f"Line {rule.line_number}: {rule.raw_rule}")
                        
                        st.divider()
        else:
            st.success("🎉 No issues found! Your firewall configuration looks good.")
        
        # Statistics
        st.subheader("📊 Statistics")
        stats_df = pd.DataFrame([
            {"Metric": k.replace('_', ' ').title(), "Value": v}
            for k, v in analysis.statistics.items()
        ])
        st.dataframe(stats_df, use_container_width=True)
    
    def render_recommendations_tab(self):
        """Render recommendations tab"""
        if not st.session_state.recommendations:
            if st.session_state.analysis:
                st.info("👆 Click 'Generate Recommendations' in the sidebar.")
            else:
                st.info("Please run analysis first.")
            return
        
        plan = st.session_state.recommendations
        
        st.header("💡 Optimization Recommendations")
        
        if not plan.recommendations:
            st.success("🎉 No optimization recommendations needed! Your configuration is already optimal.")
            return
        
        # Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Recommendations", len(plan.recommendations))
        with col2:
            rules_reduced = plan.estimated_savings.get('rules_reduced', 0)
            st.metric("Rules Can Be Reduced", rules_reduced)
        with col3:
            perf_improvement = plan.estimated_savings.get('performance_improvement', 0)
            st.metric("Est. Performance Gain", f"{perf_improvement:.1f}%")
        
        # Recommendations by priority
        from optimizer.recommender import RecommendationPriority
        
        for priority in [RecommendationPriority.CRITICAL, RecommendationPriority.HIGH, 
                        RecommendationPriority.MEDIUM, RecommendationPriority.LOW]:
            
            priority_recs = plan.get_by_priority(priority)
            if not priority_recs:
                continue
            
            priority_color = {
                RecommendationPriority.CRITICAL: "🔴",
                RecommendationPriority.HIGH: "🟠", 
                RecommendationPriority.MEDIUM: "🟡",
                RecommendationPriority.LOW: "🟢"
            }[priority]
            
            with st.expander(f"{priority_color} {priority.name.title()} Priority ({len(priority_recs)} recommendations)"):
                for i, rec in enumerate(priority_recs):
                    st.write(f"**{i+1}. {rec.title}**")
                    st.write(rec.description)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"🎯 **Impact**: {rec.estimated_impact}")
                    with col2:
                        st.write(f"⚠️ **Risk**: {rec.risk_level}")
                    
                    if rec.implementation_notes:
                        st.write(f"📝 **Implementation**: {rec.implementation_notes}")
                    
                    if rec.affected_rules:
                        st.write("**Affected rules:**")
                        for rule in rec.affected_rules:
                            st.code(f"Line {rule.line_number}: {rule.raw_rule}")
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ Apply", key=f"apply_{i}_{priority.value}"):
                            st.info("This would apply the recommendation (implementation pending)")
                    with col2:
                        if st.button(f"❌ Dismiss", key=f"dismiss_{i}_{priority.value}"):
                            st.info("Recommendation dismissed")
                    
                    st.divider()
    
    def render_visualizations_tab(self):
        """Render visualizations tab"""
        if not st.session_state.config:
            st.info("Please load a configuration first.")
            return
        
        st.header("📊 Visualizations")
        
        # Check for visualization dependencies
        try:
            import plotly.graph_objects as go
            import matplotlib.pyplot as plt
            plotly_available = True
            matplotlib_available = True
        except ImportError:
            plotly_available = False
            matplotlib_available = False
        
        if not plotly_available and not matplotlib_available:
            st.error("⚠️ Visualization libraries not available. Please install plotly and matplotlib:")
            st.code("pip install plotly matplotlib")
            return
        
        viz_type = st.selectbox(
            "Choose visualization:",
            [
                "Rule Flow Diagram",
                "Issues Dashboard", 
                "Dependency Graph",
                "Optimization Impact",
                "Rule Coverage Heatmap"
            ]
        )
        
        try:
            if viz_type == "Rule Flow Diagram":
                if not plotly_available:
                    st.warning("Plotly required for interactive diagrams. Install with: pip install plotly")
                    return
                with st.spinner("Creating rule flow diagram..."):
                    fig = self.visualizer.create_rule_flow_diagram(st.session_state.config)
                    st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Issues Dashboard" and st.session_state.analysis:
                if not plotly_available:
                    st.warning("Plotly required for dashboard. Install with: pip install plotly")
                    return
                with st.spinner("Creating issues dashboard..."):
                    fig = self.visualizer.create_issue_dashboard(st.session_state.analysis)
                    st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Dependency Graph":
                if not plotly_available:
                    st.warning("Plotly required for graph visualization. Install with: pip install plotly")
                    return
                with st.spinner("Creating dependency graph..."):
                    fig = self.visualizer.create_rule_dependency_graph(st.session_state.config)
                    st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Optimization Impact" and st.session_state.recommendations:
                if not plotly_available:
                    st.warning("Plotly required for impact charts. Install with: pip install plotly")
                    return
                with st.spinner("Creating optimization impact chart..."):
                    fig = self.visualizer.create_optimization_impact_chart(st.session_state.recommendations)
                    st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Rule Coverage Heatmap":
                if not matplotlib_available:
                    st.warning("Matplotlib required for heatmaps. Install with: pip install matplotlib")
                    return
                with st.spinner("Creating rule coverage heatmap..."):
                    fig = self.visualizer.create_rule_heatmap(st.session_state.config)
                    st.pyplot(fig)
            
            else:
                if viz_type == "Issues Dashboard" and not st.session_state.analysis:
                    st.info("Please run analysis first to view the issues dashboard.")
                elif viz_type == "Optimization Impact" and not st.session_state.recommendations:
                    st.info("Please generate recommendations first to view optimization impact.")
                else:
                    st.info(f"Please complete the required steps to view {viz_type}")
                
        except Exception as e:
            st.error(f"Failed to create visualization: {e}")
            st.write("**Error details:**")
            st.code(str(e))
            
            # Provide helpful error messages
            if "plotly" in str(e).lower():
                st.info("💡 Try installing plotly: pip install plotly")
            elif "matplotlib" in str(e).lower():
                st.info("💡 Try installing matplotlib: pip install matplotlib")
            elif "networkx" in str(e).lower():
                st.info("💡 Try installing networkx: pip install networkx")
    
    def render_configuration_tab(self):
        """Render configuration tab"""
        st.header("⚙️ Configuration & Settings")
        
        # App configuration
        st.subheader("Application Settings")
        
        # Analysis settings
        with st.expander("🔍 Analysis Settings"):
            check_redundant = st.checkbox("Check redundant rules", value=True)
            check_conflicts = st.checkbox("Check conflicting rules", value=True)
            check_ordering = st.checkbox("Check rule ordering", value=True)
            check_unreachable = st.checkbox("Check unreachable rules", value=True)
            check_security = st.checkbox("Check security issues", value=True)
            
            confidence_threshold = st.slider(
                "Confidence threshold", 0.0, 1.0, 0.8, 0.1,
                help="Minimum confidence level for recommendations"
            )
        
        # Backup settings
        with st.expander("💾 Backup Settings"):
            backup_dir = st.text_input("Backup directory", value="./backups")
            max_backups = st.number_input("Maximum backups to keep", 1, 100, 10)
            auto_backup = st.checkbox("Auto backup before changes", value=True)
        
        # Visualization settings
        with st.expander("📊 Visualization Settings"):
            theme = st.selectbox("Chart theme", ["plotly_white", "plotly_dark", "seaborn"])
            save_format = st.selectbox("Default save format", ["html", "png", "pdf"])
            include_interactive = st.checkbox("Include interactive features", value=True)
        
        # Security settings
        with st.expander("🔒 Security Settings"):
            allow_modifications = st.checkbox("Allow system modifications", value=False)
            require_confirmation = st.checkbox("Require confirmation for changes", value=True)
            validate_before_apply = st.checkbox("Validate rules before applying", value=True)
        
        if st.button("💾 Save Configuration"):
            # Update configuration
            self.config_manager.set('analysis.check_redundant_rules', check_redundant)
            self.config_manager.set('analysis.check_conflicting_rules', check_conflicts)
            self.config_manager.set('analysis.check_rule_ordering', check_ordering)
            self.config_manager.set('analysis.check_unreachable_rules', check_unreachable)
            self.config_manager.set('analysis.check_security_issues', check_security)
            self.config_manager.set('analysis.confidence_threshold', confidence_threshold)
            
            self.config_manager.set('backup.directory', backup_dir)
            self.config_manager.set('backup.max_backups', max_backups)
            self.config_manager.set('backup.auto_backup_before_changes', auto_backup)
            
            self.config_manager.set('visualization.default_theme', theme)
            self.config_manager.set('visualization.save_format', save_format)
            self.config_manager.set('visualization.include_interactive', include_interactive)
            
            self.config_manager.set('security.allow_system_modifications', allow_modifications)
            self.config_manager.set('security.require_confirmation', require_confirmation)
            self.config_manager.set('security.validate_rules_before_apply', validate_before_apply)
            
            self.config_manager.save_config()
            st.success("✅ Configuration saved!")
        
        # System information
        st.subheader("System Information")
        st.write(f"**Operating System**: {os.name}")
        st.write(f"**Python Version**: {st.version_info if hasattr(st, 'version_info') else 'Unknown'}")
        st.write(f"**Working Directory**: {os.getcwd()}")


def main():
    """Main entry point for the Streamlit app"""
    if not STREAMLIT_AVAILABLE:
        print("Error: Streamlit is not installed.")
        print("Install with: pip install streamlit pandas")
        print("Then run: python main.py webapp")
        return
    
    try:
        app = FirewallOptimizerApp()
        app.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.write("Please check the logs for more details.")


if __name__ == "__main__":
    main()
