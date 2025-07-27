"""
Firewall Rule Analyzer Module

This module analyzes parsed firewall rules to identify issues like:
- Redundant rules
- Conflicting rules  
- Inefficient rule ordering
- Unreachable rules
- Security vulnerabilities
"""

import logging
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, field
from enum import Enum
import ipaddress
from collections import defaultdict

from .parser import FirewallRule, FirewallConfig, RuleAction


class IssueType(Enum):
    """Types of issues that can be found in firewall rules"""
    REDUNDANT = "redundant"
    CONFLICTING = "conflicting"
    UNREACHABLE = "unreachable"
    INEFFICIENT_ORDER = "inefficient_order"
    SECURITY_RISK = "security_risk"
    OVERLY_PERMISSIVE = "overly_permissive"
    MISSING_LOG = "missing_log"


class IssueSeverity(Enum):
    """Severity levels for issues"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RuleIssue:
    """Represents an issue found in firewall rules"""
    issue_type: IssueType
    severity: IssueSeverity
    description: str
    affected_rules: List[FirewallRule]
    recommendation: str
    confidence: float = 1.0  # 0.0 to 1.0


@dataclass
class AnalysisResult:
    """Results of firewall rule analysis"""
    issues: List[RuleIssue] = field(default_factory=list)
    statistics: Dict[str, int] = field(default_factory=dict)
    rule_efficiency_score: float = 0.0
    security_score: float = 0.0
    
    def add_issue(self, issue: RuleIssue):
        """Add an issue to the results"""
        self.issues.append(issue)
    
    def get_issues_by_type(self, issue_type: IssueType) -> List[RuleIssue]:
        """Get all issues of a specific type"""
        return [issue for issue in self.issues if issue.issue_type == issue_type]
    
    def get_issues_by_severity(self, severity: IssueSeverity) -> List[RuleIssue]:
        """Get all issues of a specific severity"""
        return [issue for issue in self.issues if issue.severity == severity]


class FirewallAnalyzer:
    """
    Analyzer for firewall configurations to identify optimization opportunities
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_configuration(self, config: FirewallConfig) -> AnalysisResult:
        """
        Perform comprehensive analysis of firewall configuration
        
        Args:
            config: FirewallConfig to analyze
            
        Returns:
            AnalysisResult containing all found issues
        """
        result = AnalysisResult()
        
        # Analyze each table
        for table_name, chains in config.tables.items():
            for chain_name, rules in chains.items():
                if not rules:
                    continue
                
                # Run various analyses
                self._check_redundant_rules(rules, result)
                self._check_conflicting_rules(rules, result)
                self._check_rule_ordering(rules, result)
                self._check_unreachable_rules(rules, result)
                self._check_security_issues(rules, result)
                self._check_permissive_rules(rules, result)
        
        # Calculate overall scores
        result.statistics = self._calculate_statistics(config)
        result.rule_efficiency_score = self._calculate_efficiency_score(result)
        result.security_score = self._calculate_security_score(result)
        
        return result
    
    def _check_redundant_rules(self, rules: List[FirewallRule], result: AnalysisResult):
        """Check for redundant (duplicate) rules"""
        seen_rules = {}
        
        for rule in rules:
            # Create a signature for the rule
            signature = self._create_rule_signature(rule)
            
            if signature in seen_rules:
                # Found redundant rule
                original_rule = seen_rules[signature]
                issue = RuleIssue(
                    issue_type=IssueType.REDUNDANT,
                    severity=IssueSeverity.MEDIUM,
                    description=f"Redundant rule found: duplicate of rule at line {original_rule.line_number}",
                    affected_rules=[original_rule, rule],
                    recommendation="Remove the duplicate rule to improve performance and reduce complexity"
                )
                result.add_issue(issue)
            else:
                seen_rules[signature] = rule
    
    def _check_conflicting_rules(self, rules: List[FirewallRule], result: AnalysisResult):
        """Check for conflicting rules"""
        for i, rule1 in enumerate(rules):
            for rule2 in rules[i+1:]:
                if self._rules_conflict(rule1, rule2):
                    severity = IssueSeverity.HIGH if rule1.target == "DROP" or rule2.target == "DROP" else IssueSeverity.MEDIUM
                    
                    issue = RuleIssue(
                        issue_type=IssueType.CONFLICTING,
                        severity=severity,
                        description=f"Conflicting rules: {rule1.target} vs {rule2.target} for same traffic",
                        affected_rules=[rule1, rule2],
                        recommendation="Review rule order and consolidate conflicting rules"
                    )
                    result.add_issue(issue)
    
    def _check_rule_ordering(self, rules: List[FirewallRule], result: AnalysisResult):
        """Check for inefficient rule ordering"""
        for i, rule in enumerate(rules):
            # Check if a more specific rule comes after a general one
            for j in range(i):
                earlier_rule = rules[j]
                
                if self._is_more_general(earlier_rule, rule) and rule.target != earlier_rule.target:
                    issue = RuleIssue(
                        issue_type=IssueType.INEFFICIENT_ORDER,
                        severity=IssueSeverity.MEDIUM,
                        description=f"Specific rule at line {rule.line_number} comes after general rule at line {earlier_rule.line_number}",
                        affected_rules=[earlier_rule, rule],
                        recommendation="Move more specific rules before general ones for better performance"
                    )
                    result.add_issue(issue)
    
    def _check_unreachable_rules(self, rules: List[FirewallRule], result: AnalysisResult):
        """Check for unreachable rules"""
        for i, rule in enumerate(rules):
            # Check if any previous rule would catch all traffic that this rule would match
            for j in range(i):
                earlier_rule = rules[j]
                
                if (self._rule_covers_completely(earlier_rule, rule) and 
                    earlier_rule.target in ["ACCEPT", "DROP", "REJECT"]):
                    
                    issue = RuleIssue(
                        issue_type=IssueType.UNREACHABLE,
                        severity=IssueSeverity.MEDIUM,
                        description=f"Rule at line {rule.line_number} is unreachable due to rule at line {earlier_rule.line_number}",
                        affected_rules=[earlier_rule, rule],
                        recommendation="Remove unreachable rule or reorder rules"
                    )
                    result.add_issue(issue)
                    break
    
    def _check_security_issues(self, rules: List[FirewallRule], result: AnalysisResult):
        """Check for security-related issues"""
        for rule in rules:
            # Check for overly broad access
            if (rule.target == "ACCEPT" and 
                rule.source_ip in [None, "0.0.0.0/0", "any"] and
                rule.destination_port in ["22", "3389", "23"]):  # SSH, RDP, Telnet
                
                issue = RuleIssue(
                    issue_type=IssueType.SECURITY_RISK,
                    severity=IssueSeverity.HIGH,
                    description=f"Administrative port {rule.destination_port} open to all sources",
                    affected_rules=[rule],
                    recommendation="Restrict access to administrative ports to specific source IPs"
                )
                result.add_issue(issue)
            
            # Check for missing logging on DROP rules
            if rule.target == "DROP" and "LOG" not in rule.raw_rule:
                issue = RuleIssue(
                    issue_type=IssueType.MISSING_LOG,
                    severity=IssueSeverity.LOW,
                    description="DROP rule without logging",
                    affected_rules=[rule],
                    recommendation="Consider adding logging to DROP rules for security monitoring"
                )
                result.add_issue(issue)
    
    def _check_permissive_rules(self, rules: List[FirewallRule], result: AnalysisResult):
        """Check for overly permissive rules"""
        for rule in rules:
            if (rule.target == "ACCEPT" and 
                not rule.source_ip and 
                not rule.destination_ip and 
                not rule.destination_port and
                not rule.protocol):
                
                issue = RuleIssue(
                    issue_type=IssueType.OVERLY_PERMISSIVE,
                    severity=IssueSeverity.HIGH,
                    description="Rule accepts all traffic without restrictions",
                    affected_rules=[rule],
                    recommendation="Add specific restrictions to limit the scope of this rule"
                )
                result.add_issue(issue)
    
    def _create_rule_signature(self, rule: FirewallRule) -> str:
        """Create a unique signature for a rule to detect duplicates"""
        components = [
            rule.chain,
            rule.target,
            rule.protocol or "",
            rule.source_ip or "",
            rule.destination_ip or "",
            rule.source_port or "",
            rule.destination_port or "",
            rule.interface_in or "",
            rule.interface_out or "",
            rule.state or ""
        ]
        return "|".join(components)
    
    def _rules_conflict(self, rule1: FirewallRule, rule2: FirewallRule) -> bool:
        """Check if two rules conflict with each other"""
        # Rules conflict if they match the same traffic but have different actions
        if rule1.target == rule2.target:
            return False
        
        # Check if rules match the same traffic pattern
        return (self._rules_match_same_traffic(rule1, rule2) and 
                rule1.target != rule2.target and
                rule1.target in ["ACCEPT", "DROP", "REJECT"] and
                rule2.target in ["ACCEPT", "DROP", "REJECT"])
    
    def _rules_match_same_traffic(self, rule1: FirewallRule, rule2: FirewallRule) -> bool:
        """Check if two rules would match the same traffic"""
        # Compare all matching criteria
        criteria = [
            'protocol', 'source_ip', 'destination_ip', 
            'source_port', 'destination_port', 'interface_in', 'interface_out'
        ]
        
        for criterion in criteria:
            val1 = getattr(rule1, criterion)
            val2 = getattr(rule2, criterion)
            
            # If one is None (any) and other is specific, they overlap
            if val1 is None or val2 is None:
                continue
            
            # If values are different, they don't match same traffic
            if val1 != val2:
                # Special case for IP ranges
                if criterion in ['source_ip', 'destination_ip']:
                    if not self._ip_ranges_overlap(val1, val2):
                        return False
                else:
                    return False
        
        return True
    
    def _is_more_general(self, rule1: FirewallRule, rule2: FirewallRule) -> bool:
        """Check if rule1 is more general than rule2"""
        # Rule1 is more general if it has fewer restrictions
        rule1_restrictions = sum(1 for attr in ['protocol', 'source_ip', 'destination_ip', 
                                               'source_port', 'destination_port'] 
                               if getattr(rule1, attr) is not None)
        
        rule2_restrictions = sum(1 for attr in ['protocol', 'source_ip', 'destination_ip', 
                                               'source_port', 'destination_port'] 
                               if getattr(rule2, attr) is not None)
        
        return rule1_restrictions < rule2_restrictions
    
    def _rule_covers_completely(self, general_rule: FirewallRule, specific_rule: FirewallRule) -> bool:
        """Check if general_rule would match all traffic that specific_rule would match"""
        # Compare each criterion
        criteria = [
            ('protocol', lambda g, s: g is None or g == s),
            ('source_ip', lambda g, s: g is None or self._ip_contains(g, s)),
            ('destination_ip', lambda g, s: g is None or self._ip_contains(g, s)),
            ('source_port', lambda g, s: g is None or self._port_contains(g, s)),
            ('destination_port', lambda g, s: g is None or self._port_contains(g, s)),
            ('interface_in', lambda g, s: g is None or g == s),
            ('interface_out', lambda g, s: g is None or g == s)
        ]
        
        for attr, check_func in criteria:
            general_val = getattr(general_rule, attr)
            specific_val = getattr(specific_rule, attr)
            
            if not check_func(general_val, specific_val):
                return False
        
        return True
    
    def _ip_ranges_overlap(self, ip1: str, ip2: str) -> bool:
        """Check if two IP ranges overlap"""
        try:
            net1 = ipaddress.ip_network(ip1, strict=False)
            net2 = ipaddress.ip_network(ip2, strict=False)
            return net1.overlaps(net2)
        except ValueError:
            # If parsing fails, assume they might overlap
            return True
    
    def _ip_contains(self, general: str, specific: str) -> bool:
        """Check if general IP range contains specific IP range"""
        try:
            if general is None:
                return True
            if specific is None:
                return False
            
            general_net = ipaddress.ip_network(general, strict=False)
            specific_net = ipaddress.ip_network(specific, strict=False)
            return general_net.supernet_of(specific_net) or general_net == specific_net
        except ValueError:
            return general == specific
    
    def _port_contains(self, general: str, specific: str) -> bool:
        """Check if general port range contains specific port"""
        if general is None:
            return True
        if specific is None:
            return False
        
        try:
            if ':' in general:
                g_start, g_end = map(int, general.split(':'))
            else:
                g_start = g_end = int(general)
            
            if ':' in specific:
                s_start, s_end = map(int, specific.split(':'))
            else:
                s_start = s_end = int(specific)
            
            return g_start <= s_start and s_end <= g_end
        except ValueError:
            return general == specific
    
    def _calculate_statistics(self, config: FirewallConfig) -> Dict[str, int]:
        """Calculate configuration statistics"""
        stats = {
            'total_rules': 0,
            'total_chains': 0,
            'total_tables': len(config.tables),
            'accept_rules': 0,
            'drop_rules': 0,
            'reject_rules': 0,
            'custom_chains': 0
        }
        
        for table_name, chains in config.tables.items():
            stats['total_chains'] += len(chains)
            
            for chain_name, rules in chains.items():
                stats['total_rules'] += len(rules)
                
                # Count chain types
                if chain_name not in ['INPUT', 'OUTPUT', 'FORWARD', 'PREROUTING', 'POSTROUTING']:
                    stats['custom_chains'] += 1
                
                # Count rule types
                for rule in rules:
                    if rule.target == 'ACCEPT':
                        stats['accept_rules'] += 1
                    elif rule.target == 'DROP':
                        stats['drop_rules'] += 1
                    elif rule.target == 'REJECT':
                        stats['reject_rules'] += 1
        
        return stats
    
    def _calculate_efficiency_score(self, result: AnalysisResult) -> float:
        """Calculate efficiency score based on issues found"""
        base_score = 100.0
        
        # Deduct points for issues
        for issue in result.issues:
            if issue.issue_type == IssueType.REDUNDANT:
                base_score -= 5
            elif issue.issue_type == IssueType.INEFFICIENT_ORDER:
                base_score -= 3
            elif issue.issue_type == IssueType.UNREACHABLE:
                base_score -= 4
        
        return max(0.0, min(100.0, base_score))
    
    def _calculate_security_score(self, result: AnalysisResult) -> float:
        """Calculate security score based on issues found"""
        base_score = 100.0
        
        # Deduct points for security issues
        for issue in result.issues:
            if issue.issue_type == IssueType.SECURITY_RISK:
                if issue.severity == IssueSeverity.CRITICAL:
                    base_score -= 20
                elif issue.severity == IssueSeverity.HIGH:
                    base_score -= 15
                elif issue.severity == IssueSeverity.MEDIUM:
                    base_score -= 10
            elif issue.issue_type == IssueType.OVERLY_PERMISSIVE:
                base_score -= 8
        
        return max(0.0, min(100.0, base_score))


def main():
    """Example usage of the analyzer"""
    from .parser import IptablesParser
    
    # Example analysis
    parser = IptablesParser()
    analyzer = FirewallAnalyzer()
    
    sample_rules = """
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]

-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -j DROP
-A INPUT -p tcp --dport 443 -j ACCEPT

COMMIT
"""
    
    config = parser.parse_iptables_save(sample_rules)
    result = analyzer.analyze_configuration(config)
    
    print(f"Analysis Results:")
    print(f"Total issues found: {len(result.issues)}")
    print(f"Efficiency Score: {result.rule_efficiency_score:.1f}/100")
    print(f"Security Score: {result.security_score:.1f}/100")
    
    for issue in result.issues:
        print(f"\n{issue.issue_type.value.title()} ({issue.severity.value}):")
        print(f"  {issue.description}")
        print(f"  Recommendation: {issue.recommendation}")


if __name__ == "__main__":
    main()
