"""
Firewall Rule Parser Module

This module handles parsing of iptables rules from various formats including
iptables-save output, individual rule strings, and configuration files.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class RuleAction(Enum):
    """Enumeration of possible rule actions"""
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"
    LOG = "LOG"
    RETURN = "RETURN"
    REDIRECT = "REDIRECT"
    MASQUERADE = "MASQUERADE"
    JUMP = "JUMP"


class RuleTable(Enum):
    """Enumeration of iptables tables"""
    FILTER = "filter"
    NAT = "nat"
    MANGLE = "mangle"
    RAW = "raw"
    SECURITY = "security"


class ChainPolicy(Enum):
    """Enumeration of chain policies"""
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"


@dataclass
class FirewallRule:
    """
    Represents a single firewall rule with all its components
    """
    table: str = "filter"
    chain: str = ""
    target: str = ""
    protocol: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    source_port: Optional[str] = None
    destination_port: Optional[str] = None
    interface_in: Optional[str] = None
    interface_out: Optional[str] = None
    state: Optional[str] = None
    module: Optional[str] = None
    jump_target: Optional[str] = None
    line_number: int = 0
    raw_rule: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization to set computed properties"""
        if self.target in ["ACCEPT", "DROP", "REJECT", "LOG", "RETURN"]:
            self.action = RuleAction(self.target)
        else:
            self.action = RuleAction.JUMP
            self.jump_target = self.target


@dataclass
class ChainInfo:
    """Information about an iptables chain"""
    name: str
    policy: ChainPolicy
    packet_count: int = 0
    byte_count: int = 0
    is_user_defined: bool = False


@dataclass
class FirewallConfig:
    """Complete firewall configuration"""
    tables: Dict[str, Dict[str, List[FirewallRule]]] = field(default_factory=dict)
    chains: Dict[str, ChainInfo] = field(default_factory=dict)
    comments: List[str] = field(default_factory=list)


class IptablesParser:
    """
    Parser for iptables rules and configurations
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._setup_regex_patterns()
    
    def _setup_regex_patterns(self):
        """Setup regex patterns for parsing"""
        # Basic rule pattern
        self.rule_pattern = re.compile(
            r'^-A\s+(\S+)\s+(.*)$'
        )
        
        # Chain definition pattern
        self.chain_pattern = re.compile(
            r'^:(\S+)\s+(\S+)\s+\[(\d+):(\d+)\]$'
        )
        
        # Table pattern
        self.table_pattern = re.compile(r'^\*(\w+)$')
        
        # Parameter patterns
        self.param_patterns = {
            'protocol': re.compile(r'-p\s+(\S+)'),
            'source': re.compile(r'-s\s+(\S+)'),
            'destination': re.compile(r'-d\s+(\S+)'),
            'sport': re.compile(r'--sport\s+(\S+)'),
            'dport': re.compile(r'--dport\s+(\S+)'),
            'in_interface': re.compile(r'-i\s+(\S+)'),
            'out_interface': re.compile(r'-o\s+(\S+)'),
            'target': re.compile(r'-j\s+(\S+)'),
            'state': re.compile(r'--ctstate\s+(\S+)'),
            'module': re.compile(r'-m\s+(\S+)')
        }
    
    def parse_iptables_save(self, content: str) -> FirewallConfig:
        """
        Parse iptables-save output into a structured configuration
        
        Args:
            content: String content from iptables-save
            
        Returns:
            FirewallConfig object containing parsed rules and chains
        """
        config = FirewallConfig()
        current_table = "filter"
        line_number = 0
        
        lines = content.strip().split('\n')
        
        for line in lines:
            line_number += 1
            line = line.strip()
            
            # Skip empty lines and comments (except table markers)
            if not line or (line.startswith('#') and not line.startswith('# Generated')):
                if line.startswith('#'):
                    config.comments.append(line)
                continue
            
            # Parse table marker
            table_match = self.table_pattern.match(line)
            if table_match:
                current_table = table_match.group(1)
                if current_table not in config.tables:
                    config.tables[current_table] = {}
                continue
            
            # Parse chain definition
            chain_match = self.chain_pattern.match(line)
            if chain_match:
                chain_name = chain_match.group(1)
                policy = chain_match.group(2)
                packet_count = int(chain_match.group(3))
                byte_count = int(chain_match.group(4))
                
                # Determine if it's a user-defined chain
                is_user_defined = policy == '-'
                if is_user_defined:
                    policy = "ACCEPT"  # Default for user chains
                
                config.chains[chain_name] = ChainInfo(
                    name=chain_name,
                    policy=ChainPolicy(policy),
                    packet_count=packet_count,
                    byte_count=byte_count,
                    is_user_defined=is_user_defined
                )
                
                # Initialize chain in current table
                if chain_name not in config.tables[current_table]:
                    config.tables[current_table][chain_name] = []
                continue
            
            # Parse rule
            rule_match = self.rule_pattern.match(line)
            if rule_match:
                chain_name = rule_match.group(1)
                rule_params = rule_match.group(2)
                
                rule = self._parse_rule_parameters(
                    rule_params, current_table, chain_name, line_number, line
                )
                
                # Add to appropriate table and chain
                if current_table not in config.tables:
                    config.tables[current_table] = {}
                if chain_name not in config.tables[current_table]:
                    config.tables[current_table][chain_name] = []
                
                config.tables[current_table][chain_name].append(rule)
        
        return config
    
    def _parse_rule_parameters(self, params: str, table: str, chain: str, 
                             line_number: int, raw_rule: str) -> FirewallRule:
        """
        Parse individual rule parameters
        
        Args:
            params: Parameter string from rule
            table: Current table name
            chain: Current chain name
            line_number: Line number in original file
            raw_rule: Original rule string
            
        Returns:
            FirewallRule object
        """
        rule = FirewallRule(
            table=table,
            chain=chain,
            line_number=line_number,
            raw_rule=raw_rule
        )
        
        # Extract parameters using regex patterns
        for param_name, pattern in self.param_patterns.items():
            match = pattern.search(params)
            if match:
                value = match.group(1)
                
                if param_name == 'protocol':
                    rule.protocol = value
                elif param_name == 'source':
                    rule.source_ip = value
                elif param_name == 'destination':
                    rule.destination_ip = value
                elif param_name == 'sport':
                    rule.source_port = value
                elif param_name == 'dport':
                    rule.destination_port = value
                elif param_name == 'in_interface':
                    rule.interface_in = value
                elif param_name == 'out_interface':
                    rule.interface_out = value
                elif param_name == 'target':
                    rule.target = value
                elif param_name == 'state':
                    rule.state = value
                elif param_name == 'module':
                    rule.module = value
        
        # Store all parameters for advanced analysis
        rule.parameters = self._extract_all_parameters(params)
        
        return rule
    
    def _extract_all_parameters(self, params: str) -> Dict[str, Any]:
        """
        Extract all parameters from a rule string for advanced analysis
        
        Args:
            params: Parameter string
            
        Returns:
            Dictionary of all parameters found
        """
        parameters = {}
        
        # Split by spaces but preserve quoted strings
        tokens = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', params)
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.startswith('-'):
                param_name = token.lstrip('-')
                
                # Get parameter value if available
                if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                    parameters[param_name] = tokens[i + 1]
                    i += 2
                else:
                    parameters[param_name] = True
                    i += 1
            else:
                i += 1
        
        return parameters
    
    def parse_rule_string(self, rule_string: str) -> FirewallRule:
        """
        Parse a single iptables rule string
        
        Args:
            rule_string: Single rule string
            
        Returns:
            FirewallRule object
        """
        rule_string = rule_string.strip()
        
        # Handle different rule formats
        if rule_string.startswith('iptables'):
            # Extract the actual rule part
            rule_match = re.search(r'iptables\s+(.+)', rule_string)
            if rule_match:
                params = rule_match.group(1)
            else:
                params = rule_string
        elif rule_string.startswith('-A'):
            # Already in iptables-save format
            match = self.rule_pattern.match(rule_string)
            if match:
                chain = match.group(1)
                params = match.group(2)
                return self._parse_rule_parameters(
                    params, "filter", chain, 1, rule_string
                )
        else:
            params = rule_string
        
        # Parse as generic rule
        return self._parse_rule_parameters(
            params, "filter", "INPUT", 1, rule_string
        )
    
    def validate_rule(self, rule: FirewallRule) -> Tuple[bool, List[str]]:
        """
        Validate a firewall rule for common issues
        
        Args:
            rule: FirewallRule to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for required fields
        if not rule.chain:
            errors.append("Rule missing chain specification")
        
        if not rule.target:
            errors.append("Rule missing target/action")
        
        # Validate IP addresses
        if rule.source_ip and not self._is_valid_ip_or_network(rule.source_ip):
            errors.append(f"Invalid source IP: {rule.source_ip}")
        
        if rule.destination_ip and not self._is_valid_ip_or_network(rule.destination_ip):
            errors.append(f"Invalid destination IP: {rule.destination_ip}")
        
        # Validate ports
        if rule.source_port and not self._is_valid_port(rule.source_port):
            errors.append(f"Invalid source port: {rule.source_port}")
        
        if rule.destination_port and not self._is_valid_port(rule.destination_port):
            errors.append(f"Invalid destination port: {rule.destination_port}")
        
        return len(errors) == 0, errors
    
    def _is_valid_ip_or_network(self, ip_str: str) -> bool:
        """Validate IP address or network notation"""
        try:
            import ipaddress
            ipaddress.ip_network(ip_str, strict=False)
            return True
        except ValueError:
            return False
    
    def _is_valid_port(self, port_str: str) -> bool:
        """Validate port number or range"""
        try:
            if ':' in port_str:
                # Port range
                start, end = port_str.split(':', 1)
                return (1 <= int(start) <= 65535 and 
                       1 <= int(end) <= 65535 and 
                       int(start) <= int(end))
            else:
                # Single port
                port = int(port_str)
                return 1 <= port <= 65535
        except ValueError:
            return False


def main():
    """Example usage of the parser"""
    parser = IptablesParser()
    
    # Example rule parsing
    sample_rule = "-A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT"
    rule = parser.parse_rule_string(sample_rule)
    
    print(f"Parsed rule:")
    print(f"  Chain: {rule.chain}")
    print(f"  Protocol: {rule.protocol}")
    print(f"  Source: {rule.source_ip}")
    print(f"  Destination Port: {rule.destination_port}")
    print(f"  Target: {rule.target}")
    
    # Validate the rule
    is_valid, errors = parser.validate_rule(rule)
    print(f"  Valid: {is_valid}")
    if errors:
        print(f"  Errors: {errors}")


if __name__ == "__main__":
    main()
