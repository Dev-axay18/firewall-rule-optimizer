"""
Firewall Optimizer Utilities Module

This module provides utility functions and classes for the firewall optimizer,
including configuration management, backup operations, logging setup, and
common helper functions.
"""

import os
import json
import logging
import datetime
import subprocess
import shutil
from typing import Dict, List, Optional, Tuple, Any, Union
from pathlib import Path
import hashlib
import tempfile
from contextlib import contextmanager

# Try to import yaml with fallback
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("Warning: PyYAML not installed. Configuration files will use JSON format.")

from .parser import FirewallConfig, FirewallRule


class ConfigManager:
    """
    Configuration manager for the firewall optimizer application
    """
    
    def __init__(self, config_file: Optional[str] = None):
        if config_file:
            self.config_file = config_file
        else:
            # Use YAML if available, otherwise JSON
            self.config_file = "optimizer_config.yaml" if HAS_YAML else "optimizer_config.json"
        
        self.config = self._load_default_config()
        self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration settings"""
        return {
            'backup': {
                'enabled': True,
                'directory': './backups',
                'max_backups': 10,
                'auto_backup_before_changes': True
            },
            'analysis': {
                'check_redundant_rules': True,
                'check_conflicting_rules': True,
                'check_rule_ordering': True,
                'check_unreachable_rules': True,
                'check_security_issues': True,
                'confidence_threshold': 0.8
            },
            'recommendations': {
                'auto_apply_low_risk': False,
                'require_confirmation': True,
                'max_batch_size': 5
            },
            'logging': {
                'level': 'INFO',
                'file': 'optimizer.log',
                'max_size_mb': 10,
                'backup_count': 5
            },
            'visualization': {
                'default_theme': 'plotly_white',
                'save_format': 'html',
                'include_interactive': True
            },
            'security': {
                'allow_system_modifications': False,
                'require_sudo_confirmation': True,
                'validate_rules_before_apply': True
            }
        }
    
    def _load_config(self):
        """Load configuration from file if it exists"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    if HAS_YAML and self.config_file.endswith('.yaml'):
                        user_config = yaml.safe_load(f)
                    else:
                        # Fall back to JSON
                        user_config = json.load(f)
                    
                    if user_config:
                        self._deep_update(self.config, user_config)
            except Exception as e:
                logging.warning(f"Failed to load config file {self.config_file}: {e}")
    
    def _deep_update(self, base_dict: Dict, update_dict: Dict):
        """Deep update of nested dictionaries"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                if HAS_YAML and self.config_file.endswith('.yaml'):
                    yaml.dump(self.config, f, default_flow_style=False, indent=2)
                else:
                    # Fall back to JSON
                    json.dump(self.config, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save config file {self.config_file}: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path: Path to config value (e.g., 'backup.enabled')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation
        
        Args:
            key_path: Path to config value (e.g., 'backup.enabled')
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value


class BackupManager:
    """
    Manager for creating and restoring firewall rule backups
    """
    
    def __init__(self, backup_dir: str = "./backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def create_backup(self, config: FirewallConfig, 
                     description: str = "") -> str:
        """
        Create a backup of the firewall configuration
        
        Args:
            config: FirewallConfig to backup
            description: Optional description for the backup
            
        Returns:
            Path to the created backup file
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"firewall_backup_{timestamp}.json"
        backup_path = self.backup_dir / backup_filename
        
        backup_data = {
            'timestamp': timestamp,
            'description': description,
            'config_hash': self._calculate_config_hash(config),
            'tables': {}
        }
        
        # Convert config to serializable format
        for table_name, chains in config.tables.items():
            backup_data['tables'][table_name] = {}
            for chain_name, rules in chains.items():
                backup_data['tables'][table_name][chain_name] = [
                    {
                        'raw_rule': rule.raw_rule,
                        'line_number': rule.line_number,
                        'table': rule.table,
                        'chain': rule.chain,
                        'target': rule.target,
                        'protocol': rule.protocol,
                        'source_ip': rule.source_ip,
                        'destination_ip': rule.destination_ip,
                        'source_port': rule.source_port,
                        'destination_port': rule.destination_port,
                        'interface_in': rule.interface_in,
                        'interface_out': rule.interface_out,
                        'state': rule.state,
                        'module': rule.module,
                        'parameters': rule.parameters
                    }
                    for rule in rules
                ]
        
        # Save backup
        try:
            with open(backup_path, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            self.logger.info(f"Backup created: {backup_path}")
            
            # Clean up old backups
            self._cleanup_old_backups()
            
            return str(backup_path)
        
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            raise
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """
        List all available backups
        
        Returns:
            List of backup information dictionaries
        """
        backups = []
        
        for backup_file in self.backup_dir.glob("firewall_backup_*.json"):
            try:
                with open(backup_file, 'r') as f:
                    backup_data = json.load(f)
                
                backups.append({
                    'filename': backup_file.name,
                    'path': str(backup_file),
                    'timestamp': backup_data.get('timestamp', 'unknown'),
                    'description': backup_data.get('description', ''),
                    'size': backup_file.stat().st_size,
                    'config_hash': backup_data.get('config_hash', '')
                })
            
            except Exception as e:
                self.logger.warning(f"Failed to read backup {backup_file}: {e}")
        
        # Sort by timestamp descending
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
        return backups
    
    def restore_backup(self, backup_path: str) -> FirewallConfig:
        """
        Restore a firewall configuration from backup
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            Restored FirewallConfig
        """
        from .parser import FirewallRule, FirewallConfig, ChainInfo, ChainPolicy
        
        try:
            with open(backup_path, 'r') as f:
                backup_data = json.load(f)
            
            config = FirewallConfig()
            
            # Restore tables and rules
            for table_name, chains in backup_data['tables'].items():
                config.tables[table_name] = {}
                
                for chain_name, rules_data in chains.items():
                    rules = []
                    
                    for rule_data in rules_data:
                        rule = FirewallRule(
                            table=rule_data.get('table', table_name),
                            chain=rule_data.get('chain', chain_name),
                            target=rule_data.get('target', ''),
                            protocol=rule_data.get('protocol'),
                            source_ip=rule_data.get('source_ip'),
                            destination_ip=rule_data.get('destination_ip'),
                            source_port=rule_data.get('source_port'),
                            destination_port=rule_data.get('destination_port'),
                            interface_in=rule_data.get('interface_in'),
                            interface_out=rule_data.get('interface_out'),
                            state=rule_data.get('state'),
                            module=rule_data.get('module'),
                            line_number=rule_data.get('line_number', 0),
                            raw_rule=rule_data.get('raw_rule', ''),
                            parameters=rule_data.get('parameters', {})
                        )
                        rules.append(rule)
                    
                    config.tables[table_name][chain_name] = rules
            
            self.logger.info(f"Configuration restored from backup: {backup_path}")
            return config
        
        except Exception as e:
            self.logger.error(f"Failed to restore backup {backup_path}: {e}")
            raise
    
    def _calculate_config_hash(self, config: FirewallConfig) -> str:
        """Calculate hash of configuration for integrity checking"""
        config_str = ""
        
        for table_name, chains in config.tables.items():
            for chain_name, rules in chains.items():
                for rule in rules:
                    config_str += rule.raw_rule
        
        return hashlib.sha256(config_str.encode()).hexdigest()[:16]
    
    def _cleanup_old_backups(self, max_backups: int = 10):
        """Clean up old backup files"""
        backups = list(self.backup_dir.glob("firewall_backup_*.json"))
        
        if len(backups) > max_backups:
            # Sort by modification time and remove oldest
            backups.sort(key=lambda x: x.stat().st_mtime)
            
            for old_backup in backups[:-max_backups]:
                try:
                    old_backup.unlink()
                    self.logger.info(f"Removed old backup: {old_backup}")
                except Exception as e:
                    self.logger.warning(f"Failed to remove old backup {old_backup}: {e}")


class SystemInterface:
    """
    Interface for interacting with the system firewall
    """
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.logger = logging.getLogger(__name__)
    
    def get_current_rules(self) -> str:
        """
        Get current iptables rules using iptables-save
        
        Returns:
            String output from iptables-save
        """
        try:
            if os.name == 'nt':  # Windows
                self.logger.warning("iptables not available on Windows. Using sample data.")
                return self._get_sample_rules()
            
            result = subprocess.run(
                ['iptables-save'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get current rules: {e}")
            return self._get_sample_rules()
        except FileNotFoundError:
            self.logger.warning("iptables-save not found. Using sample data.")
            return self._get_sample_rules()
    
    def apply_rules(self, rules_content: str) -> bool:
        """
        Apply firewall rules using iptables-restore
        
        Args:
            rules_content: Content to apply via iptables-restore
            
        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            self.logger.info("DRY RUN: Would apply the following rules:")
            self.logger.info(rules_content)
            return True
        
        try:
            if os.name == 'nt':  # Windows
                self.logger.warning("Cannot apply iptables rules on Windows")
                return False
            
            # Create temporary file for rules
            with tempfile.NamedTemporaryFile(mode='w', suffix='.rules', delete=False) as f:
                f.write(rules_content)
                temp_file = f.name
            
            try:
                # Apply rules
                result = subprocess.run(
                    ['iptables-restore', temp_file],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                self.logger.info("Rules applied successfully")
                return True
            
            finally:
                # Clean up temporary file
                os.unlink(temp_file)
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to apply rules: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error applying rules: {e}")
            return False
    
    def validate_rules(self, rules_content: str) -> Tuple[bool, List[str]]:
        """
        Validate firewall rules without applying them
        
        Args:
            rules_content: Rules content to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            if os.name == 'nt':  # Windows
                # Basic validation for Windows
                lines = rules_content.strip().split('\n')
                for i, line in enumerate(lines, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if not (line.startswith('*') or line.startswith(':') or 
                               line.startswith('-A') or line == 'COMMIT'):
                            errors.append(f"Line {i}: Invalid rule format: {line}")
            else:
                # Use iptables-restore --test on Linux
                with tempfile.NamedTemporaryFile(mode='w', suffix='.rules', delete=False) as f:
                    f.write(rules_content)
                    temp_file = f.name
                
                try:
                    result = subprocess.run(
                        ['iptables-restore', '--test', temp_file],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode != 0:
                        errors.append(f"Validation failed: {result.stderr}")
                
                finally:
                    os.unlink(temp_file)
        
        except Exception as e:
            errors.append(f"Validation error: {e}")
        
        return len(errors) == 0, errors
    
    def _get_sample_rules(self) -> str:
        """Get sample rules for testing/demo purposes"""
        return """# Generated by iptables-save v1.8.7 on Sat Jul 26 2025
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT
-A INPUT -j DROP
COMMIT
# Completed on Sat Jul 26 2025
"""


def setup_logging(config: ConfigManager):
    """
    Setup logging configuration
    
    Args:
        config: ConfigManager instance
    """
    log_level = getattr(logging, config.get('logging.level', 'INFO').upper())
    log_file = config.get('logging.file', 'optimizer.log')
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup file handler with rotation
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=config.get('logging.max_size_mb', 10) * 1024 * 1024,
        backupCount=config.get('logging.backup_count', 5)
    )
    file_handler.setFormatter(formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


@contextmanager
def safe_file_operation(file_path: str, backup: bool = True):
    """
    Context manager for safe file operations with automatic backup
    
    Args:
        file_path: Path to file to operate on
        backup: Whether to create backup before operation
    """
    backup_path = None
    
    try:
        if backup and os.path.exists(file_path):
            backup_path = f"{file_path}.backup.{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(file_path, backup_path)
        
        yield file_path
    
    except Exception as e:
        # Restore backup if operation failed
        if backup_path and os.path.exists(backup_path):
            try:
                shutil.copy2(backup_path, file_path)
                logging.info(f"Restored backup from {backup_path}")
            except Exception as restore_error:
                logging.error(f"Failed to restore backup: {restore_error}")
        raise e
    
    finally:
        # Clean up backup if operation was successful
        if backup_path and os.path.exists(backup_path):
            try:
                os.remove(backup_path)
            except Exception as cleanup_error:
                logging.warning(f"Failed to clean up backup: {cleanup_error}")


def format_size(size_bytes: int) -> str:
    """
    Format byte size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def validate_ip_address(ip_str: str) -> bool:
    """
    Validate IP address or network notation
    
    Args:
        ip_str: IP address string to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        import ipaddress
        ipaddress.ip_network(ip_str, strict=False)
        return True
    except ValueError:
        return False


def validate_port(port_str: str) -> bool:
    """
    Validate port number or range
    
    Args:
        port_str: Port string to validate
        
    Returns:
        True if valid, False otherwise
    """
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
    """Example usage of utilities"""
    # Example configuration management
    config = ConfigManager()
    print(f"Backup enabled: {config.get('backup.enabled')}")
    
    # Example backup management
    backup_manager = BackupManager()
    backups = backup_manager.list_backups()
    print(f"Available backups: {len(backups)}")
    
    # Example system interface
    system = SystemInterface(dry_run=True)
    current_rules = system.get_current_rules()
    print(f"Current rules length: {len(current_rules)} characters")


if __name__ == "__main__":
    main()
