# Copilot Instructions for AI-Powered Firewall Rule Optimizer

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is an AI-Powered Firewall Rule Optimizer and Visualizer project that analyzes Linux iptables firewall rules to detect redundant or conflicting rules and suggest optimization strategies.

## Key Guidelines
- Focus on security best practices when handling firewall rules
- Always validate input rules before processing
- Implement proper error handling for firewall operations
- Use structured data formats for rule representation
- Follow the principle of least privilege for security recommendations
- Ensure all changes are reversible with proper backup mechanisms

## Architecture
- `optimizer/` contains core analysis and optimization logic
- `web_ui/` contains the Streamlit interface
- `data/` contains sample rules and test data
- Use modular design with clear separation of concerns

## Security Considerations
- Never execute firewall changes without user confirmation
- Always create backups before modifications
- Validate all input rules for security vulnerabilities
- Log all operations for audit purposes
