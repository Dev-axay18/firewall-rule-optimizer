#!/usr/bin/env python3
"""
Test script to verify the firewall optimizer installation and functionality
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test built-in modules
        import re
        import json
        import logging
        import datetime
        print("✅ Built-in modules: OK")
    except ImportError as e:
        print(f"❌ Built-in modules failed: {e}")
        return False
    
    try:
        # Test if optimizer package works
        from optimizer import IptablesParser, FirewallAnalyzer
        print("✅ Optimizer package: OK")
    except ImportError as e:
        print(f"❌ Optimizer package failed: {e}")
        return False
    
    # Test optional packages (graceful degradation)
    optional_packages = [
        ('pandas', 'Data analysis'),
        ('numpy', 'Numerical computing'),
        ('matplotlib', 'Plotting'),
        ('plotly', 'Interactive plots'),
        ('networkx', 'Graph analysis'),
        ('streamlit', 'Web interface')
    ]
    
    for package, description in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package} ({description}): OK")
        except ImportError:
            print(f"⚠️ {package} ({description}): Not installed (optional)")
    
    return True

def test_basic_functionality():
    """Test basic firewall optimizer functionality"""
    print("\nTesting basic functionality...")
    
    try:
        from optimizer import IptablesParser, FirewallAnalyzer
        
        # Test parser
        parser = IptablesParser()
        sample_rules = """
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -j DROP
COMMIT
"""
        
        config = parser.parse_iptables_save(sample_rules)
        print(f"✅ Parser: Parsed {sum(len(rules) for chains in config.tables.values() for rules in chains.values())} rules")
        
        # Test analyzer
        analyzer = FirewallAnalyzer()
        analysis = analyzer.analyze_configuration(config)
        print(f"✅ Analyzer: Found {len(analysis.issues)} issues, Security score: {analysis.security_score:.1f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_sample_data():
    """Test if sample data exists and can be loaded"""
    print("\nTesting sample data...")
    
    sample_path = "data/sample_rules.txt"
    if os.path.exists(sample_path):
        try:
            with open(sample_path, 'r') as f:
                content = f.read()
            print(f"✅ Sample data: Loaded {len(content)} characters")
            return True
        except Exception as e:
            print(f"❌ Sample data read failed: {e}")
            return False
    else:
        print("⚠️ Sample data file not found (this is OK)")
        return True

def main():
    """Main test function"""
    print("🔥 AI-Powered Firewall Rule Optimizer - Installation Test")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_imports()
    all_tests_passed &= test_basic_functionality()
    all_tests_passed &= test_sample_data()
    
    print("\n" + "=" * 60)
    
    if all_tests_passed:
        print("🎉 All tests passed! The firewall optimizer is ready to use.")
        print("\nNext steps:")
        print("1. Install optional packages if needed:")
        print("   pip install streamlit pandas numpy matplotlib plotly networkx")
        print("2. Run the CLI interface:")
        print("   python main.py analyze --input data/sample_rules.txt") 
        print("3. Launch the web interface:")
        print("   python main.py webapp")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("The basic functionality should still work without optional packages.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
