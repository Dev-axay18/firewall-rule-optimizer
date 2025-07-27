"""
Firewall Rule Visualizer Module

This module provides comprehensive visualization capabilities for firewall rules,
including rule flow diagrams, dependency graphs, performance heatmaps, and
security analysis charts.
"""

import logging
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict, Counter

# Optional visualization imports
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    # Create mock plt for type annotations
    class plt:
        class Figure:
            pass
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

from .parser import FirewallRule, FirewallConfig
from .analyzer import AnalysisResult, IssueType, IssueSeverity
from .recommender import OptimizationPlan, RecommendationType


class FirewallVisualizer:
    """
    Comprehensive visualization system for firewall rules and analysis results
    """
    
    def __init__(self, style: str = "seaborn-v0_8"):
        self.logger = logging.getLogger(__name__)
        
        # Check for required dependencies
        if not MATPLOTLIB_AVAILABLE:
            self.logger.warning("Matplotlib not available. Some visualizations will be disabled.")
        
        if not PLOTLY_AVAILABLE:
            self.logger.warning("Plotly not available. Interactive visualizations will be disabled.")
        
        if not NETWORKX_AVAILABLE:
            self.logger.warning("NetworkX not available. Graph visualizations will be disabled.")
        
        # Setup matplotlib style if available
        if MATPLOTLIB_AVAILABLE:
            try:
                plt.style.use(style)
            except:
                plt.style.use("default")
        
        # Color schemes for different visualizations
        self.colors = {
            'accept': '#2ecc71',
            'drop': '#e74c3c', 
            'reject': '#f39c12',
            'log': '#3498db',
            'chain': '#9b59b6',
            'redundant': '#e67e22',
            'conflict': '#c0392b',
            'unreachable': '#95a5a6',
            'security': '#e74c3c',
            'optimization': '#27ae60'
        }
    
    def _check_plotly_available(self):
        """Check if Plotly is available and raise error if not"""
        if not PLOTLY_AVAILABLE:
            raise ImportError("Plotly is required for interactive visualizations. Install with: pip install plotly")
    
    def _check_matplotlib_available(self):
        """Check if Matplotlib is available and raise error if not"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("Matplotlib is required for static visualizations. Install with: pip install matplotlib")
    
    def _check_networkx_available(self):
        """Check if NetworkX is available and raise error if not"""
        if not NETWORKX_AVAILABLE:
            raise ImportError("NetworkX is required for graph visualizations. Install with: pip install networkx")
    
    def create_rule_flow_diagram(self, config: FirewallConfig, 
                               save_path: Optional[str] = None) -> Optional[Any]:
        """
        Create an interactive flow diagram showing rule processing flow
        
        Args:
            config: FirewallConfig to visualize
            save_path: Optional path to save the visualization
            
        Returns:
            Plotly figure object or None if Plotly not available
        """
        self._check_plotly_available()
        
        fig = go.Figure()
        
        # Process filter table (most common for visualization)
        if 'filter' in config.tables:
            chains = config.tables['filter']
            
            for chain_name, rules in chains.items():
                if not rules:
                    continue
                
                # Create chain visualization
                y_positions = list(range(len(rules)))
                rule_texts = []
                colors = []
                
                for i, rule in enumerate(rules):
                    # Create descriptive text for each rule
                    rule_text = self._format_rule_for_display(rule)
                    rule_texts.append(rule_text)
                    
                    # Assign colors based on action
                    if rule.target == 'ACCEPT':
                        colors.append(self.colors['accept'])
                    elif rule.target == 'DROP':
                        colors.append(self.colors['drop'])
                    elif rule.target == 'REJECT':
                        colors.append(self.colors['reject'])
                    else:
                        colors.append(self.colors['chain'])
                
                # Add scatter plot for this chain
                fig.add_trace(go.Scatter(
                    x=[chain_name] * len(rules),
                    y=y_positions,
                    mode='markers+text',
                    marker=dict(
                        size=15,
                        color=colors,
                        symbol='square'
                    ),
                    text=rule_texts,
                    textposition='middle right',
                    name=f'{chain_name} Chain',
                    hovertemplate='<b>%{text}</b><br>Chain: %{x}<br>Position: %{y}<extra></extra>'
                ))
        
        fig.update_layout(
            title='Firewall Rule Flow Diagram',
            xaxis_title='Chains',
            yaxis_title='Rule Position (Top to Bottom)',
            showlegend=True,
            height=600,
            template='plotly_white'
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def create_issue_dashboard(self, analysis: AnalysisResult, 
                             save_path: Optional[str] = None) -> Optional[Any]:
        """
        Create a comprehensive dashboard showing all identified issues
        
        Args:
            analysis: AnalysisResult containing identified issues
            save_path: Optional path to save the visualization
            
        Returns:
            Plotly figure with subplots or None if Plotly not available
        """
        self._check_plotly_available()
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Issues by Type',
                'Issues by Severity', 
                'Rule Statistics',
                'Security & Efficiency Scores'
            ],
            specs=[[{'type': 'bar'}, {'type': 'pie'}],
                   [{'type': 'bar'}, {'type': 'indicator'}]]
        )
        
        # 1. Issues by Type
        issue_counts = Counter(issue.issue_type.value for issue in analysis.issues)
        if issue_counts:
            fig.add_trace(
                go.Bar(
                    x=list(issue_counts.keys()),
                    y=list(issue_counts.values()),
                    marker_color=[self.colors.get(issue_type, '#3498db') 
                                for issue_type in issue_counts.keys()],
                    name='Issues by Type'
                ),
                row=1, col=1
            )
        
        # 2. Issues by Severity
        severity_counts = Counter(issue.severity.value for issue in analysis.issues)
        if severity_counts:
            colors_severity = ['#27ae60', '#f39c12', '#e67e22', '#c0392b']  # low to critical
            fig.add_trace(
                go.Pie(
                    labels=list(severity_counts.keys()),
                    values=list(severity_counts.values()),
                    marker_colors=colors_severity[:len(severity_counts)],
                    name='Severity'
                ),
                row=1, col=2
            )
        
        # 3. Rule Statistics
        stats = analysis.statistics
        stat_names = []
        stat_values = []
        for key, value in stats.items():
            if key != 'total_tables':  # Skip this for cleaner display
                stat_names.append(key.replace('_', ' ').title())
                stat_values.append(value)
        
        fig.add_trace(
            go.Bar(
                x=stat_names,
                y=stat_values,
                marker_color='#3498db',
                name='Statistics'
            ),
            row=2, col=1
        )
        
        # 4. Scores (Gauge charts)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=analysis.security_score,
                domain={'x': [0, 1], 'y': [0, 0.5]},
                title={'text': "Security Score"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=analysis.rule_efficiency_score,
                domain={'x': [0, 1], 'y': [0.5, 1]},
                title={'text': "Efficiency Score"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title='Firewall Analysis Dashboard',
            height=800,
            showlegend=False,
            template='plotly_white'
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def create_rule_dependency_graph(self, config: FirewallConfig, 
                                   save_path: Optional[str] = None) -> Optional[Any]:
        """
        Create a network graph showing rule dependencies and chain relationships
        
        Args:
            config: FirewallConfig to analyze
            save_path: Optional path to save the visualization
            
        Returns:
            Plotly figure with network graph or None if dependencies not available
        """
        self._check_plotly_available()
        self._check_networkx_available()
        # Create networkx graph
        G = nx.DiGraph()
        
        # Add nodes for chains and rules
        node_colors = []
        node_sizes = []
        node_texts = []
        
        for table_name, chains in config.tables.items():
            for chain_name, rules in chains.items():
                # Add chain node
                chain_node = f"{table_name}:{chain_name}"
                G.add_node(chain_node)
                node_colors.append(self.colors['chain'])
                node_sizes.append(30)
                node_texts.append(f"Chain: {chain_name}")
                
                # Add rule nodes and connections
                for i, rule in enumerate(rules):
                    rule_node = f"{chain_node}:rule_{i}"
                    G.add_node(rule_node)
                    G.add_edge(chain_node, rule_node)
                    
                    # Color based on rule action
                    if rule.target == 'ACCEPT':
                        node_colors.append(self.colors['accept'])
                    elif rule.target == 'DROP':
                        node_colors.append(self.colors['drop'])
                    elif rule.target == 'REJECT':
                        node_colors.append(self.colors['reject'])
                    else:
                        node_colors.append(self.colors['log'])
                    
                    node_sizes.append(15)
                    node_texts.append(f"Rule {i+1}: {rule.target}")
                    
                    # Add jump connections
                    if rule.jump_target and rule.jump_target in [c for _, chains in config.tables.items() for c in chains.keys()]:
                        target_chain = f"{table_name}:{rule.jump_target}"
                        if target_chain in G.nodes():
                            G.add_edge(rule_node, target_chain)
        
        # Create layout
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Extract coordinates
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
        
        # Create figure
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_texts,
            textposition="middle center",
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=2, color='white')
            )
        ))
        
        fig.update_layout(
            title='Firewall Rule Dependency Graph',
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Chains and rule relationships",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(color="grey", size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            template='plotly_white'
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def create_optimization_impact_chart(self, plan: OptimizationPlan, 
                                       save_path: Optional[str] = None) -> Optional[Any]:
        """
        Create a chart showing the impact of optimization recommendations
        
        Args:
            plan: OptimizationPlan containing recommendations
            save_path: Optional path to save the visualization
            
        Returns:
            Plotly figure or None if Plotly not available
        """
        self._check_plotly_available()
        # Analyze recommendations
        rec_types = [rec.rec_type.value for rec in plan.recommendations]
        priorities = [rec.priority.value for rec in plan.recommendations]
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                'Recommendations by Type',
                'Recommendations by Priority',
                'Estimated Impact',
                'Implementation Risk'
            ],
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'pie'}]]
        )
        
        # 1. Recommendations by Type
        type_counts = Counter(rec_types)
        fig.add_trace(
            go.Bar(
                x=list(type_counts.keys()),
                y=list(type_counts.values()),
                marker_color='#3498db',
                name='By Type'
            ),
            row=1, col=1
        )
        
        # 2. Recommendations by Priority
        priority_counts = Counter(priorities)
        priority_colors = {1: '#27ae60', 2: '#f39c12', 3: '#e67e22', 4: '#c0392b'}
        fig.add_trace(
            go.Bar(
                x=[f"Priority {p}" for p in priority_counts.keys()],
                y=list(priority_counts.values()),
                marker_color=[priority_colors.get(p, '#3498db') for p in priority_counts.keys()],
                name='By Priority'
            ),
            row=1, col=2
        )
        
        # 3. Estimated Impact
        savings = plan.estimated_savings
        fig.add_trace(
            go.Bar(
                x=['Rules Reduced', 'Performance %', 'Security %'],
                y=[savings.get('rules_reduced', 0), 
                   savings.get('performance_improvement', 0),
                   savings.get('security_improvement', 0)],
                marker_color=['#e67e22', '#27ae60', '#3498db'],
                name='Impact'
            ),
            row=2, col=1
        )
        
        # 4. Risk Distribution
        risk_levels = [rec.risk_level for rec in plan.recommendations]
        risk_counts = Counter(risk_levels)
        risk_colors = {'low': '#27ae60', 'medium': '#f39c12', 'high': '#e74c3c'}
        
        fig.add_trace(
            go.Pie(
                labels=list(risk_counts.keys()),
                values=list(risk_counts.values()),
                marker_colors=[risk_colors.get(risk, '#3498db') for risk in risk_counts.keys()],
                name='Risk'
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title='Optimization Plan Impact Analysis',
            height=800,
            showlegend=False,
            template='plotly_white'
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def create_rule_heatmap(self, config: FirewallConfig, 
                          save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a heatmap showing rule coverage and patterns
        
        Args:
            config: FirewallConfig to analyze
            save_path: Optional path to save the visualization
            
        Returns:
            Matplotlib figure
        """
        # Collect data for heatmap
        protocols = []
        ports = []
        actions = []
        
        for table_name, chains in config.tables.items():
            for chain_name, rules in chains.items():
                for rule in rules:
                    protocols.append(rule.protocol or 'any')
                    
                    if rule.destination_port:
                        try:
                            port = int(rule.destination_port)
                            if port <= 65535:
                                ports.append(port)
                            else:
                                ports.append(0)  # Invalid port
                        except ValueError:
                            ports.append(0)  # Port range or invalid
                    else:
                        ports.append(0)  # Any port
                    
                    actions.append(rule.target)
        
        if not protocols:
            # No data to visualize
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No rules to visualize', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        # Create DataFrame
        df = pd.DataFrame({
            'Protocol': protocols,
            'Port': ports,
            'Action': actions
        })
        
        # Create pivot table for heatmap
        port_ranges = ['0', '1-1023', '1024-49151', '49152-65535']
        df['PortRange'] = df['Port'].apply(lambda x: 
            '0' if x == 0 else
            '1-1023' if 1 <= x <= 1023 else
            '1024-49151' if 1024 <= x <= 49151 else
            '49152-65535')
        
        # Create pivot table
        pivot = df.groupby(['Protocol', 'PortRange', 'Action']).size().unstack(fill_value=0)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create heatmap
        if not pivot.empty:
            sns.heatmap(pivot, annot=True, fmt='d', cmap='YlOrRd', ax=ax)
        
        ax.set_title('Firewall Rules Coverage Heatmap')
        ax.set_xlabel('Actions')
        ax.set_ylabel('Protocol and Port Range')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def _format_rule_for_display(self, rule: FirewallRule) -> str:
        """Format a rule for display in visualizations"""
        parts = []
        
        if rule.protocol:
            parts.append(f"proto:{rule.protocol}")
        
        if rule.source_ip:
            parts.append(f"src:{rule.source_ip}")
        
        if rule.destination_port:
            parts.append(f"port:{rule.destination_port}")
        
        parts.append(f"→{rule.target}")
        
        return " ".join(parts) if parts else rule.raw_rule[:50]
    
    def create_comprehensive_report(self, config: FirewallConfig, 
                                  analysis: AnalysisResult,
                                  plan: OptimizationPlan,
                                  output_dir: str = ".") -> Dict[str, str]:
        """
        Create a comprehensive HTML report with all visualizations
        
        Args:
            config: FirewallConfig
            analysis: AnalysisResult
            plan: OptimizationPlan
            output_dir: Directory to save report files
            
        Returns:
            Dictionary with paths to generated files
        """
        import os
        
        files_created = {}
        
        # Create individual visualizations
        try:
            # Rule flow diagram
            flow_fig = self.create_rule_flow_diagram(config)
            flow_path = os.path.join(output_dir, "rule_flow.html")
            flow_fig.write_html(flow_path)
            files_created['flow_diagram'] = flow_path
            
            # Issue dashboard
            dashboard_fig = self.create_issue_dashboard(analysis)
            dashboard_path = os.path.join(output_dir, "issue_dashboard.html")
            dashboard_fig.write_html(dashboard_path)
            files_created['dashboard'] = dashboard_path
            
            # Dependency graph
            graph_fig = self.create_rule_dependency_graph(config)
            graph_path = os.path.join(output_dir, "dependency_graph.html")
            graph_fig.write_html(graph_path)
            files_created['dependency_graph'] = graph_path
            
            # Optimization impact
            impact_fig = self.create_optimization_impact_chart(plan)
            impact_path = os.path.join(output_dir, "optimization_impact.html")
            impact_fig.write_html(impact_path)
            files_created['optimization_impact'] = impact_path
            
            # Rule heatmap
            heatmap_fig = self.create_rule_heatmap(config)
            heatmap_path = os.path.join(output_dir, "rule_heatmap.png")
            heatmap_fig.savefig(heatmap_path, dpi=300, bbox_inches='tight')
            plt.close(heatmap_fig)
            files_created['heatmap'] = heatmap_path
            
        except Exception as e:
            self.logger.error(f"Error creating visualizations: {e}")
        
        return files_created


def main():
    """Example usage of the visualizer"""
    from .parser import IptablesParser
    from .analyzer import FirewallAnalyzer
    from .recommender import FirewallRecommender
    
    # Example usage
    parser = IptablesParser()
    analyzer = FirewallAnalyzer()
    recommender = FirewallRecommender()
    visualizer = FirewallVisualizer()
    
    sample_rules = """
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]

-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT
-A INPUT -j DROP

COMMIT
"""
    
    config = parser.parse_iptables_save(sample_rules)
    analysis = analyzer.analyze_configuration(config)
    plan = recommender.generate_recommendations(config, analysis)
    
    # Create visualizations
    flow_fig = visualizer.create_rule_flow_diagram(config)
    dashboard_fig = visualizer.create_issue_dashboard(analysis)
    
    print("Visualizations created successfully!")
    print("Use flow_fig.show() and dashboard_fig.show() to display them")


if __name__ == "__main__":
    main()
