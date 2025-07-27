"""
Firewall Rule Recommender Module

This module provides intelligent recommendations for optimizing firewall rules
based on analysis results. It suggests specific actions to improve rule
efficiency, security, and maintainability.
"""

import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import copy

from .parser import FirewallRule, FirewallConfig
from .analyzer import AnalysisResult, RuleIssue, IssueType, IssueSeverity


class RecommendationType(Enum):
    """Types of recommendations"""
    DELETE_RULE = "delete_rule"
    REORDER_RULES = "reorder_rules"
    MERGE_RULES = "merge_rules"
    SPLIT_RULE = "split_rule"
    MODIFY_RULE = "modify_rule"
    ADD_RULE = "add_rule"
    ADD_LOGGING = "add_logging"
    RESTRICT_SOURCE = "restrict_source"


class RecommendationPriority(Enum):
    """Priority levels for recommendations"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Recommendation:
    """A specific recommendation for improving firewall rules"""
    rec_type: RecommendationType
    priority: RecommendationPriority
    title: str
    description: str
    affected_rules: List[FirewallRule]
    new_rules: List[FirewallRule] = field(default_factory=list)
    implementation_notes: str = ""
    risk_level: str = "low"  # low, medium, high
    estimated_impact: str = ""
    
    def to_dict(self) -> Dict:
        """Convert recommendation to dictionary format"""
        return {
            'type': self.rec_type.value,
            'priority': self.priority.value,
            'title': self.title,
            'description': self.description,
            'affected_rule_lines': [rule.line_number for rule in self.affected_rules],
            'risk_level': self.risk_level,
            'estimated_impact': self.estimated_impact,
            'implementation_notes': self.implementation_notes
        }


@dataclass
class OptimizationPlan:
    """Complete optimization plan with all recommendations"""
    recommendations: List[Recommendation] = field(default_factory=list)
    estimated_savings: Dict[str, float] = field(default_factory=dict)
    backup_required: bool = True
    
    def add_recommendation(self, recommendation: Recommendation):
        """Add a recommendation to the plan"""
        self.recommendations.append(recommendation)
    
    def get_by_priority(self, priority: RecommendationPriority) -> List[Recommendation]:
        """Get all recommendations of a specific priority"""
        return [rec for rec in self.recommendations if rec.priority == priority]
    
    def get_by_type(self, rec_type: RecommendationType) -> List[Recommendation]:
        """Get all recommendations of a specific type"""
        return [rec for rec in self.recommendations if rec.rec_type == rec_type]


class FirewallRecommender:
    """
    Generates intelligent recommendations for firewall rule optimization
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_recommendations(self, config: FirewallConfig, 
                               analysis: AnalysisResult) -> OptimizationPlan:
        """
        Generate optimization recommendations based on analysis results
        
        Args:
            config: Original firewall configuration
            analysis: Analysis results containing identified issues
            
        Returns:
            OptimizationPlan with specific recommendations
        """
        plan = OptimizationPlan()
        
        # Process each type of issue
        self._handle_redundant_rules(analysis, plan)
        self._handle_conflicting_rules(analysis, plan)
        self._handle_ordering_issues(analysis, plan)
        self._handle_unreachable_rules(analysis, plan)
        self._handle_security_issues(analysis, plan)
        self._handle_permissive_rules(analysis, plan)
        
        # Add general optimization recommendations
        self._add_general_optimizations(config, plan)
        
        # Calculate estimated impact
        plan.estimated_savings = self._calculate_estimated_savings(plan, analysis)
        
        # Sort recommendations by priority
        plan.recommendations.sort(key=lambda x: x.priority.value, reverse=True)
        
        return plan
    
    def _handle_redundant_rules(self, analysis: AnalysisResult, plan: OptimizationPlan):
        """Handle redundant rule issues"""
        redundant_issues = analysis.get_issues_by_type(IssueType.REDUNDANT)
        
        for issue in redundant_issues:
            if len(issue.affected_rules) >= 2:
                # Keep the first occurrence, remove duplicates
                primary_rule = issue.affected_rules[0]
                duplicate_rules = issue.affected_rules[1:]
                
                for duplicate in duplicate_rules:
                    recommendation = Recommendation(
                        rec_type=RecommendationType.DELETE_RULE,
                        priority=RecommendationPriority.MEDIUM,
                        title=f"Remove redundant rule at line {duplicate.line_number}",
                        description=f"This rule is identical to the rule at line {primary_rule.line_number} and can be safely removed.",
                        affected_rules=[duplicate],
                        risk_level="low",
                        estimated_impact="Improved performance, reduced complexity",
                        implementation_notes=f"Delete rule: {duplicate.raw_rule}"
                    )
                    plan.add_recommendation(recommendation)
    
    def _handle_conflicting_rules(self, analysis: AnalysisResult, plan: OptimizationPlan):
        """Handle conflicting rule issues"""
        conflicting_issues = analysis.get_issues_by_type(IssueType.CONFLICTING)
        
        for issue in conflicting_issues:
            if len(issue.affected_rules) >= 2:
                rule1, rule2 = issue.affected_rules[0], issue.affected_rules[1]
                
                # Suggest resolution based on rule types
                if rule1.target == "DROP" or rule2.target == "DROP":
                    # Security-first approach: prefer DROP
                    priority = RecommendationPriority.HIGH
                    description = "Conflicting rules detected with security implications. Consider keeping the more restrictive rule."
                else:
                    priority = RecommendationPriority.MEDIUM
                    description = "Conflicting rules detected. Review and consolidate to ensure intended behavior."
                
                recommendation = Recommendation(
                    rec_type=RecommendationType.MODIFY_RULE,
                    priority=priority,
                    title="Resolve conflicting rules",
                    description=description,
                    affected_rules=issue.affected_rules,
                    risk_level="medium",
                    estimated_impact="Predictable firewall behavior",
                    implementation_notes="Review rules and determine intended behavior, then modify or remove as needed"
                )
                plan.add_recommendation(recommendation)
    
    def _handle_ordering_issues(self, analysis: AnalysisResult, plan: OptimizationPlan):
        """Handle inefficient rule ordering issues"""
        ordering_issues = analysis.get_issues_by_type(IssueType.INEFFICIENT_ORDER)
        
        for issue in ordering_issues:
            if len(issue.affected_rules) >= 2:
                general_rule, specific_rule = issue.affected_rules[0], issue.affected_rules[1]
                
                recommendation = Recommendation(
                    rec_type=RecommendationType.REORDER_RULES,
                    priority=RecommendationPriority.MEDIUM,
                    title=f"Reorder rules for better performance",
                    description=f"Move specific rule (line {specific_rule.line_number}) before general rule (line {general_rule.line_number})",
                    affected_rules=issue.affected_rules,
                    risk_level="low",
                    estimated_impact="Improved packet processing performance",
                    implementation_notes="Move more specific rules earlier in the chain for better performance"
                )
                plan.add_recommendation(recommendation)
    
    def _handle_unreachable_rules(self, analysis: AnalysisResult, plan: OptimizationPlan):
        """Handle unreachable rule issues"""
        unreachable_issues = analysis.get_issues_by_type(IssueType.UNREACHABLE)
        
        for issue in unreachable_issues:
            unreachable_rule = issue.affected_rules[-1]  # Usually the last rule is unreachable
            
            recommendation = Recommendation(
                rec_type=RecommendationType.DELETE_RULE,
                priority=RecommendationPriority.MEDIUM,
                title=f"Remove unreachable rule at line {unreachable_rule.line_number}",
                description="This rule will never be executed due to previous rules matching all its traffic.",
                affected_rules=[unreachable_rule],
                risk_level="low",
                estimated_impact="Reduced rule set complexity",
                implementation_notes=f"Remove rule: {unreachable_rule.raw_rule}"
            )
            plan.add_recommendation(recommendation)
    
    def _handle_security_issues(self, analysis: AnalysisResult, plan: OptimizationPlan):
        """Handle security-related issues"""
        security_issues = analysis.get_issues_by_type(IssueType.SECURITY_RISK)
        
        for issue in security_issues:
            rule = issue.affected_rules[0]
            
            if "Administrative port" in issue.description:
                # Suggest restricting source IPs for admin ports
                recommendation = Recommendation(
                    rec_type=RecommendationType.RESTRICT_SOURCE,
                    priority=RecommendationPriority.HIGH,
                    title=f"Restrict access to administrative port {rule.destination_port}",
                    description=f"Port {rule.destination_port} is open to all sources. Limit access to specific trusted IPs.",
                    affected_rules=[rule],
                    risk_level="high",
                    estimated_impact="Reduced attack surface, improved security",
                    implementation_notes=f"Add source IP restriction like '-s 192.168.1.0/24' to rule"
                )
                plan.add_recommendation(recommendation)
        
        # Handle missing logging issues
        logging_issues = analysis.get_issues_by_type(IssueType.MISSING_LOG)
        for issue in logging_issues:
            rule = issue.affected_rules[0]
            
            recommendation = Recommendation(
                rec_type=RecommendationType.ADD_LOGGING,
                priority=RecommendationPriority.LOW,
                title=f"Add logging to DROP rule at line {rule.line_number}",
                description="Enable logging for this DROP rule to improve security monitoring.",
                affected_rules=[rule],
                risk_level="low",
                estimated_impact="Better security monitoring and incident response",
                implementation_notes="Add a LOG rule before the DROP rule with appropriate log prefix"
            )
            plan.add_recommendation(recommendation)
    
    def _handle_permissive_rules(self, analysis: AnalysisResult, plan: OptimizationPlan):
        """Handle overly permissive rules"""
        permissive_issues = analysis.get_issues_by_type(IssueType.OVERLY_PERMISSIVE)
        
        for issue in permissive_issues:
            rule = issue.affected_rules[0]
            
            recommendation = Recommendation(
                rec_type=RecommendationType.MODIFY_RULE,
                priority=RecommendationPriority.HIGH,
                title=f"Add restrictions to overly permissive rule",
                description="This rule accepts all traffic without restrictions. Add specific criteria.",
                affected_rules=[rule],
                risk_level="high",
                estimated_impact="Improved security posture",
                implementation_notes="Add protocol, port, or source IP restrictions to limit rule scope"
            )
            plan.add_recommendation(recommendation)
    
    def _add_general_optimizations(self, config: FirewallConfig, plan: OptimizationPlan):
        """Add general optimization recommendations"""
        
        # Analyze rule patterns for optimization opportunities
        all_rules = []
        for table_name, chains in config.tables.items():
            for chain_name, rules in chains.items():
                all_rules.extend(rules)
        
        # Check for rules that could be merged
        mergeable_groups = self._find_mergeable_rules(all_rules)
        for group in mergeable_groups:
            if len(group) > 1:
                recommendation = Recommendation(
                    rec_type=RecommendationType.MERGE_RULES,
                    priority=RecommendationPriority.LOW,
                    title=f"Consider merging {len(group)} similar rules",
                    description="These rules have similar patterns and might be merged for efficiency.",
                    affected_rules=group,
                    risk_level="low",
                    estimated_impact="Simplified rule set",
                    implementation_notes="Review rules and merge if they serve the same purpose"
                )
                plan.add_recommendation(recommendation)
        
        # Check for missing default policies
        self._check_default_policies(config, plan)
    
    def _find_mergeable_rules(self, rules: List[FirewallRule]) -> List[List[FirewallRule]]:
        """Find groups of rules that could potentially be merged"""
        groups = []
        
        # Group rules by similar patterns
        pattern_groups = {}
        
        for rule in rules:
            if rule.target not in ["ACCEPT", "DROP", "REJECT"]:
                continue
            
            # Create a pattern key based on protocol, target, and other criteria
            pattern = (
                rule.protocol,
                rule.target,
                rule.source_ip,
                rule.interface_in,
                rule.interface_out
            )
            
            if pattern not in pattern_groups:
                pattern_groups[pattern] = []
            pattern_groups[pattern].append(rule)
        
        # Find groups with multiple rules that differ only in ports
        for pattern, group_rules in pattern_groups.items():
            if len(group_rules) > 1:
                # Check if they only differ in destination ports
                ports = set()
                for rule in group_rules:
                    if rule.destination_port:
                        ports.add(rule.destination_port)
                
                if len(ports) == len(group_rules) and len(ports) > 1:
                    # All rules differ only in ports - potential merge candidate
                    groups.append(group_rules)
        
        return groups
    
    def _check_default_policies(self, config: FirewallConfig, plan: OptimizationPlan):
        """Check for and recommend default policy improvements"""
        
        for table_name, chains in config.tables.items():
            if table_name == "filter":
                for chain_name in ["INPUT", "FORWARD", "OUTPUT"]:
                    if chain_name in chains:
                        rules = chains[chain_name]
                        
                        # Check if there's an explicit default DROP at the end
                        if rules:
                            last_rule = rules[-1]
                            if (last_rule.target != "DROP" or 
                                last_rule.protocol or 
                                last_rule.source_ip or 
                                last_rule.destination_ip):
                                
                                # Suggest adding explicit default policy
                                new_rule = FirewallRule(
                                    table=table_name,
                                    chain=chain_name,
                                    target="DROP",
                                    raw_rule=f"-A {chain_name} -j DROP"
                                )
                                
                                recommendation = Recommendation(
                                    rec_type=RecommendationType.ADD_RULE,
                                    priority=RecommendationPriority.MEDIUM,
                                    title=f"Add explicit default DROP policy to {chain_name}",
                                    description="Add an explicit default DROP rule at the end of the chain for better security.",
                                    affected_rules=[],
                                    new_rules=[new_rule],
                                    risk_level="medium",
                                    estimated_impact="Improved security posture with explicit default policy",
                                    implementation_notes=f"Add rule: -A {chain_name} -j DROP"
                                )
                                plan.add_recommendation(recommendation)
    
    def _calculate_estimated_savings(self, plan: OptimizationPlan, 
                                   analysis: AnalysisResult) -> Dict[str, float]:
        """Calculate estimated performance and security improvements"""
        savings = {
            'rules_reduced': 0,
            'performance_improvement': 0.0,
            'security_improvement': 0.0
        }
        
        # Count rules that would be removed
        for rec in plan.recommendations:
            if rec.rec_type == RecommendationType.DELETE_RULE:
                savings['rules_reduced'] += len(rec.affected_rules)
        
        # Estimate performance improvement (rough calculation)
        total_rules = analysis.statistics.get('total_rules', 1)
        if total_rules > 0:
            savings['performance_improvement'] = (savings['rules_reduced'] / total_rules) * 100
        
        # Estimate security improvement based on security recommendations
        security_recs = len([rec for rec in plan.recommendations 
                           if rec.rec_type in [RecommendationType.RESTRICT_SOURCE, 
                                             RecommendationType.ADD_LOGGING]])
        
        security_issues = len(analysis.get_issues_by_type(IssueType.SECURITY_RISK))
        if security_issues > 0:
            savings['security_improvement'] = (security_recs / security_issues) * 100
        
        return savings
    
    def generate_optimized_config(self, original_config: FirewallConfig, 
                                plan: OptimizationPlan) -> FirewallConfig:
        """
        Generate an optimized configuration by applying recommendations
        
        Args:
            original_config: Original firewall configuration
            plan: Optimization plan with recommendations
            
        Returns:
            Optimized FirewallConfig
        """
        # Create a deep copy of the original configuration
        optimized_config = copy.deepcopy(original_config)
        
        # Apply recommendations in order of priority
        sorted_recs = sorted(plan.recommendations, 
                           key=lambda x: x.priority.value, reverse=True)
        
        for rec in sorted_recs:
            if rec.rec_type == RecommendationType.DELETE_RULE:
                self._apply_delete_recommendation(optimized_config, rec)
            elif rec.rec_type == RecommendationType.ADD_RULE:
                self._apply_add_recommendation(optimized_config, rec)
            # Add more recommendation types as needed
        
        return optimized_config
    
    def _apply_delete_recommendation(self, config: FirewallConfig, rec: Recommendation):
        """Apply a delete rule recommendation"""
        for rule in rec.affected_rules:
            # Find and remove the rule from the configuration
            for table_name, chains in config.tables.items():
                for chain_name, rules in chains.items():
                    if rule in rules:
                        rules.remove(rule)
                        break
    
    def _apply_add_recommendation(self, config: FirewallConfig, rec: Recommendation):
        """Apply an add rule recommendation"""
        for new_rule in rec.new_rules:
            table = new_rule.table
            chain = new_rule.chain
            
            if table not in config.tables:
                config.tables[table] = {}
            if chain not in config.tables[table]:
                config.tables[table][chain] = []
            
            config.tables[table][chain].append(new_rule)


def main():
    """Example usage of the recommender"""
    from .parser import IptablesParser
    from .analyzer import FirewallAnalyzer
    
    # Example usage
    parser = IptablesParser()
    analyzer = FirewallAnalyzer()
    recommender = FirewallRecommender()
    
    sample_rules = """
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]

-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -j DROP

COMMIT
"""
    
    config = parser.parse_iptables_save(sample_rules)
    analysis = analyzer.analyze_configuration(config)
    plan = recommender.generate_recommendations(config, analysis)
    
    print(f"Optimization Plan:")
    print(f"Total recommendations: {len(plan.recommendations)}")
    print(f"Estimated rules reduction: {plan.estimated_savings.get('rules_reduced', 0)}")
    
    for rec in plan.recommendations:
        print(f"\n{rec.priority.name} Priority: {rec.title}")
        print(f"  Description: {rec.description}")
        print(f"  Risk Level: {rec.risk_level}")
        print(f"  Impact: {rec.estimated_impact}")


if __name__ == "__main__":
    main()
