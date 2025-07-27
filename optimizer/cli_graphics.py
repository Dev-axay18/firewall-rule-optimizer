"""
CLI Graphics utilities for beautiful terminal visualizations.
Provides ASCII charts, progress bars, and visual elements.
"""

import sys
from typing import Dict, List, Optional, Tuple, Any

try:
    from rich.console import Console
    from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
    from rich.table import Table
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    import plotext as plt
    PLOTEXT_AVAILABLE = True
except ImportError:
    PLOTEXT_AVAILABLE = False

from .colors import Colors


class CLIGraphics:
    """CLI Graphics utilities for terminal visualizations"""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.colors = Colors()
    
    def create_progress_bars(self, scores: Dict[str, float], width: int = 40) -> List[str]:
        """
        Create ASCII progress bars for scores
        
        Args:
            scores: Dictionary of score names to values (0-100)
            width: Width of progress bar
            
        Returns:
            List of formatted progress bar strings
        """
        bars = []
        
        for name, score in scores.items():
            # Calculate filled portion
            filled = int((score / 100) * width)
            empty = width - filled
            
            # Create bar with colors
            if RICH_AVAILABLE:
                bar = f"  {name:<20} {Colors.PROGRESS_FILL * filled}{Colors.PROGRESS_EMPTY * empty} {Colors.percentage(score)}"
            else:
                # Simple ASCII bar
                bar_char = '█' if score > 50 else '▓' if score > 20 else '░'
                bar = f"  {name:<20} {'█' * filled}{'░' * empty} {score:.1f}%"
            
            bars.append(bar)
        
        return bars
    
    def create_issues_bar_chart(self, issue_counts: Dict[str, int], max_width: int = 40) -> List[str]:
        """
        Create horizontal bar chart for issue distribution
        
        Args:
            issue_counts: Dictionary of issue types to counts
            max_width: Maximum width for bars
            
        Returns:
            List of formatted bar chart lines
        """
        if not issue_counts:
            return ["  No issues found"]
        
        max_count = max(issue_counts.values())
        if max_count == 0:
            return ["  No issues found"]
        
        chart_lines = []
        
        for issue_type, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            # Calculate bar width proportional to count
            bar_width = int((count / max_count) * max_width)
            
            # Format issue type name
            formatted_name = issue_type.replace('_', ' ').title()
            if len(formatted_name) > 20:
                formatted_name = formatted_name[:17] + "..."
            
            # Create bar
            bar = '█' * bar_width
            
            # Color based on severity (heuristic)
            if 'critical' in issue_type.lower() or 'security' in issue_type.lower():
                colored_bar = Colors.error(bar)
            elif 'conflict' in issue_type.lower() or 'unreachable' in issue_type.lower():
                colored_bar = Colors.warning(bar)
            else:
                colored_bar = Colors.info(bar)
            
            line = f"  {formatted_name:<20} {colored_bar:<{max_width + 20}} {count}"
            chart_lines.append(line)
        
        return chart_lines
    
    def create_severity_pie_chart(self, severity_counts: Dict[str, int], width: int = 50) -> List[str]:
        """
        Create ASCII pie chart representation for severity distribution
        
        Args:
            severity_counts: Dictionary of severity levels to counts
            width: Width of the chart area
            
        Returns:
            List of formatted pie chart lines
        """
        if not severity_counts:
            return ["  No severity data available"]
        
        total = sum(severity_counts.values())
        if total == 0:
            return ["  No severity data available"]
        
        chart_lines = []
        
        # Priority emojis and colors
        severity_config = {
            'CRITICAL': ('🔥', Colors.critical),
            'HIGH': ('🚨', Colors.high),
            'MEDIUM': ('⚠️', Colors.medium),
            'LOW': ('💡', Colors.low)
        }
        
        for severity, count in severity_counts.items():
            percentage = (count / total) * 100
            emoji, color_func = severity_config.get(severity.upper(), ('ℹ️', Colors.info))
            
            # Create visual representation
            bar_width = int((percentage / 100) * 30)
            bar = '█' * bar_width
            
            line = f"    {emoji} {severity.upper():<8} {color_func(bar):<40} {percentage:5.1f}% ({count})"
            chart_lines.append(line)
        
        return chart_lines
    
    def create_optimization_impact_gauge(self, impact_score: float, max_width: int = 50) -> List[str]:
        """
        Create optimization impact gauge
        
        Args:
            impact_score: Impact score (0-100)
            max_width: Maximum width of gauge
            
        Returns:
            List of formatted gauge lines
        """
        gauge_lines = []
        
        # Create gauge bar
        filled = int((impact_score / 100) * max_width)
        empty = max_width - filled
        
        # Color based on impact level
        if impact_score >= 80:
            gauge_color = Colors.success
            impact_level = "🚀 EXCELLENT"
        elif impact_score >= 60:
            gauge_color = Colors.warning
            impact_level = "⚡ GOOD"
        elif impact_score >= 40:
            gauge_color = Colors.info
            impact_level = "📈 MODERATE"
        else:
            gauge_color = Colors.error
            impact_level = "🔧 LOW"
        
        gauge_bar = gauge_color('█' * filled) + Colors.muted('░' * empty)
        
        gauge_lines.append(f"  🎯 Performance Gain: {impact_score:.1f}% {gauge_bar}")
        gauge_lines.append(f"     Impact Level: {impact_level}")
        
        return gauge_lines
    
    def create_priority_distribution_chart(self, priority_counts: Dict[str, int]) -> List[str]:
        """
        Create priority distribution chart
        
        Args:
            priority_counts: Dictionary of priority levels to counts
            
        Returns:
            List of formatted chart lines
        """
        if not priority_counts:
            return ["  No priority data available"]
        
        total = sum(priority_counts.values())
        if total == 0:
            return ["  No priority data available"]
        
        chart_lines = []
        
        # Priority configuration
        priority_config = {
            'CRITICAL': ('🔥', Colors.critical),
            'HIGH': ('🚨', Colors.high),
            'MEDIUM': ('⚠️', Colors.medium),
            'LOW': ('💡', Colors.low)
        }
        
        # Sort by priority importance
        priority_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        
        for priority in priority_order:
            if priority in priority_counts:
                count = priority_counts[priority]
                percentage = (count / total) * 100
                emoji, color_func = priority_config[priority]
                
                # Create visual bar
                bar_width = int((percentage / 100) * 25)
                bar = '█' * bar_width
                
                line = f"  {emoji} {priority:<8} {color_func(bar):<35} {percentage:5.1f}% ({count})"
                chart_lines.append(line)
        
        return chart_lines
    
    def create_simple_table(self, headers: List[str], rows: List[List[str]], title: Optional[str] = None) -> List[str]:
        """
        Create a simple ASCII table
        
        Args:
            headers: Table headers
            rows: Table rows
            title: Optional table title
            
        Returns:
            List of formatted table lines
        """
        if RICH_AVAILABLE and self.console:
            # Use rich table if available
            table = Table(title=title, box=box.ROUNDED)
            
            for header in headers:
                table.add_column(header, style="bold")
            
            for row in rows:
                table.add_row(*row)
            
            # Capture table output
            with self.console.capture() as capture:
                self.console.print(table)
            
            return capture.get().split('\n')
        
        else:
            # Simple ASCII table
            table_lines = []
            
            if title:
                table_lines.append(f"  {Colors.header(title)}")
                table_lines.append("")
            
            # Calculate column widths
            col_widths = [len(header) for header in headers]
            for row in rows:
                for i, cell in enumerate(row):
                    if i < len(col_widths):
                        col_widths[i] = max(col_widths[i], len(str(cell)))
            
            # Create header
            header_line = "  " + " | ".join(f"{header:<{col_widths[i]}}" for i, header in enumerate(headers))
            table_lines.append(Colors.header(header_line))
            
            # Create separator
            separator = "  " + "-" * len(header_line.replace(Colors.HEADER, '').replace(Colors.RESET, ''))
            table_lines.append(Colors.muted(separator))
            
            # Create rows
            for row in rows:
                row_line = "  " + " | ".join(f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row))
                table_lines.append(row_line)
            
            return table_lines
    
    def print_ascii_art_banner(self, text: str) -> None:
        """Print ASCII art banner for section headers"""
        width = max(60, len(text) + 20)
        border = "=" * width
        
        print(Colors.header(border))
        print(Colors.header(f"{text:^{width}}"))
        print(Colors.header(border))
    
    def create_loading_animation(self, message: str = "Processing...") -> None:
        """
        Show a simple loading animation (for future enhancement)
        
        Args:
            message: Loading message to display
        """
        if RICH_AVAILABLE and self.console:
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task(message, total=100)
                # This is a placeholder - actual implementation would update progress
                progress.update(task, advance=100)
        else:
            print(f"  {Colors.info('🔄')} {message}")
    
    def format_number_with_units(self, number: int) -> str:
        """Format large numbers with appropriate units"""
        if number >= 1_000_000:
            return f"{number / 1_000_000:.1f}M"
        elif number >= 1_000:
            return f"{number / 1_000:.1f}K"
        else:
            return str(number)
    
    def create_performance_metrics_display(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Create a performance metrics display
        
        Args:
            metrics: Dictionary of metric names to values
            
        Returns:
            List of formatted metric lines
        """
        lines = []
        
        for metric_name, value in metrics.items():
            formatted_name = metric_name.replace('_', ' ').title()
            
            if isinstance(value, (int, float)):
                if 'percentage' in metric_name.lower() or 'percent' in metric_name.lower():
                    formatted_value = Colors.percentage(value)
                elif 'time' in metric_name.lower():
                    formatted_value = f"{value:.2f}s"
                elif 'count' in metric_name.lower() or 'number' in metric_name.lower():
                    formatted_value = self.format_number_with_units(int(value))
                else:
                    formatted_value = str(value)
            else:
                formatted_value = str(value)
            
            line = f"  {formatted_name:<30} {formatted_value}"
            lines.append(line)
        
        return lines


    def print_cli_chart_summary(self, analysis):
        """
        Print CLI chart summary for analysis results
        
        Args:
            analysis: Analysis results object
        """
        # Calculate scores
        scores = {}
        if hasattr(analysis, 'security_score'):
            scores['Security Score'] = analysis.security_score
        if hasattr(analysis, 'efficiency_score'):
            scores['Efficiency Score'] = analysis.efficiency_score
        
        # Print score overview
        print(f"\n{Colors.info('────────────────────────────────────────')}")
        print(f"{Colors.header('📊 Score Overview')}")
        print(f"{Colors.info('────────────────────────────────────────')}")
        
        for score_line in self.create_progress_bars(scores):
            print(score_line)
        
        # Count issues by type
        issue_counts = {}
        if hasattr(analysis, 'issues') and analysis.issues:
            for issue in analysis.issues:
                issue_type = getattr(issue, 'issue_type', 'Unknown')
                if hasattr(issue_type, 'value'):
                    issue_key = issue_type.value.replace('_', ' ').title()
                else:
                    issue_key = str(issue_type).replace('_', ' ').title()
                
                issue_counts[issue_key] = issue_counts.get(issue_key, 0) + 1
        
        # Print issues distribution if there are issues
        if issue_counts:
            print(f"\n{Colors.info('────────────────────────────────────────')}")
            print(f"{Colors.header('📊 Issues Distribution')}")
            print(f"{Colors.info('────────────────────────────────────────')}")
            
            for chart_line in self.create_issues_bar_chart(issue_counts):
                print(chart_line)
        
        # Count severity levels
        severity_counts = {}
        if hasattr(analysis, 'issues') and analysis.issues:
            for issue in analysis.issues:
                severity = getattr(issue, 'severity', 'unknown')
                
                # Handle different severity value types
                if hasattr(severity, 'value'):
                    # It's an enum
                    severity_key = str(severity.value).upper()
                elif isinstance(severity, (int, float)):
                    # It's a numeric severity - map to text
                    severity_map = {1: 'CRITICAL', 2: 'HIGH', 3: 'MEDIUM', 4: 'LOW'}
                    severity_key = severity_map.get(int(severity), 'MEDIUM')
                elif isinstance(severity, str):
                    # It's already a string
                    severity_key = severity.upper()
                else:
                    # Convert to string and uppercase
                    severity_key = str(severity).upper()
                
                severity_counts[severity_key] = severity_counts.get(severity_key, 0) + 1
        
        # Print severity distribution if there are issues
        if severity_counts:
            print(f"\n{Colors.header('🥧 Severity Distribution')}")
            print(f"{Colors.info('────────────────────────────────────────')}")
            
            for chart_line in self.create_severity_pie_chart(severity_counts):
                print(chart_line)

    def create_optimization_impact_gauge(self, plan):
        """
        Create and print optimization impact gauge for a plan
        
        Args:
            plan: Optimization plan object
        """
        # Extract impact score from plan
        impact_score = 0
        if hasattr(plan, 'estimated_improvement'):
            impact_score = getattr(plan, 'estimated_improvement', 0)
        elif hasattr(plan, 'performance_improvement'):
            impact_score = getattr(plan, 'performance_improvement', 0)
        elif hasattr(plan, 'impact_score'):
            impact_score = getattr(plan, 'impact_score', 0)
        
        # Default to a reasonable value if we can't find impact score
        if impact_score == 0 and hasattr(plan, 'recommendations') and plan.recommendations:
            # Estimate impact based on number of recommendations
            impact_score = min(len(plan.recommendations) * 10, 80)
        
        print(f"\n{Colors.header('⚡ Optimization Impact')}")
        print(f"{Colors.info('────────────────────────────────────────')}")
        
        for gauge_line in self._create_impact_gauge_display(impact_score):
            print(gauge_line)

    def _create_impact_gauge_display(self, impact_score: float, max_width: int = 50) -> List[str]:
        """
        Create optimization impact gauge display (internal method)
        
        Args:
            impact_score: Impact score (0-100)
            max_width: Maximum width of gauge
            
        Returns:
            List of formatted gauge lines
        """
        gauge_lines = []
        
        # Create gauge bar
        filled = int((impact_score / 100) * max_width)
        empty = max_width - filled
        
        # Color based on impact level
        if impact_score >= 80:
            gauge_color = Colors.success
            impact_level = "🚀 EXCELLENT"
        elif impact_score >= 60:
            gauge_color = Colors.warning
            impact_level = "⚡ GOOD"
        elif impact_score >= 40:
            gauge_color = Colors.info
            impact_level = "📈 MODERATE"
        else:
            gauge_color = Colors.error
            impact_level = "🔧 LOW"
        
        gauge_bar = gauge_color('█' * filled) + Colors.muted('░' * empty)
        
        gauge_lines.append(f"  🎯 Performance Gain: {impact_score:.1f}% {gauge_bar}")
        gauge_lines.append(f"     Impact Level: {impact_level}")
        
        return gauge_lines

    def create_recommendation_priority_chart(self, recommendations):
        """
        Create and print recommendation priority chart
        
        Args:
            recommendations: List of recommendation objects
        """
        if not recommendations:
            print(f"\n{Colors.info('No recommendations available')}")
            return
        
        # Count by priority
        priority_counts = {}
        for rec in recommendations:
            priority = getattr(rec, 'priority', 'unknown')
            
            # Handle different priority value types
            if hasattr(priority, 'value'):
                # It's an enum
                priority_key = str(priority.value).upper()
            elif isinstance(priority, (int, float)):
                # It's a numeric priority - map to text
                priority_map = {1: 'CRITICAL', 2: 'HIGH', 3: 'MEDIUM', 4: 'LOW'}
                priority_key = priority_map.get(int(priority), 'MEDIUM')
            elif isinstance(priority, str):
                # It's already a string
                priority_key = priority.upper()
            else:
                # Convert to string and uppercase
                priority_key = str(priority).upper()
            
            priority_counts[priority_key] = priority_counts.get(priority_key, 0) + 1
        
        print(f"\n{Colors.header('🎯 Recommendation Priorities')}")
        print(f"{Colors.info('────────────────────────────────────────')}")
        
        for chart_line in self.create_priority_distribution_chart(priority_counts):
            print(chart_line)


def create_cli_graphics():
    """Factory function to create CLIGraphics instance"""
    return CLIGraphics()
