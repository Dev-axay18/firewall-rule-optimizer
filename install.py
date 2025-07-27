#!/usr/bin/env python3
"""
Simple installation script for the firewall optimizer
"""

import os
import sys
import subprocess

def install_package(package):
    """Install a package using pip"""
    try:
        print(f"Installing {package}...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {package} installed successfully")
            return True
        else:
            print(f"❌ Failed to install {package}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing {package}: {e}")
        return False

def main():
    """Main installation function"""
    print("🔥 Firewall Optimizer Installation")
    print("=" * 40)
    
    # Required packages
    packages = [
        'pyyaml',       # For configuration files
        'streamlit',    # For web interface
        'pandas',       # For data processing
        'numpy',        # For numerical operations
        'matplotlib',   # For static plots
        'plotly',       # For interactive plots
        'networkx',     # For graph analysis
        'seaborn',      # For statistical plots
        'pyparsing',    # For text parsing
        'click'         # For CLI
    ]
    
    print(f"Installing {len(packages)} packages...")
    print()
    
    success_count = 0
    
    for package in packages:
        if install_package(package):
            success_count += 1
        print()
    
    print("=" * 40)
    print(f"Installation complete: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("✅ All packages installed successfully!")
        print("\nYou can now run:")
        print("  python main.py webapp    # Launch web interface")
        print("  python main.py analyze   # Analyze sample rules")
    else:
        print("⚠️  Some packages failed to install.")
        print("The application will work with limited functionality.")
        print("\nYou can try installing missing packages manually:")
        for package in packages:
            print(f"  pip install {package}")

if __name__ == "__main__":
    main()
