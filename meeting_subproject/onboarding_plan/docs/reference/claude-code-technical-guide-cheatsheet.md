# Claude Code Technical Guide — Cheatsheet

## Project indexing fundamentally reimagined
## What happens technically during "indexing"
## Essential commands for project understanding

```bash
# Core workflow commands
claude                              # Start in project directory
/init                              # Generate initial CLAUDE.md context
/config                           # Access project settings
/memory                          # Edit memory files
# Project exploration patterns
```

## Complete command reference and documentation access
## Built-in slash commands
## Custom command system

```bash
# .claude/commands/security-audit.md
Perform comprehensive security analysis on $ARGUMENTS:
1. Search for SQL injection vulnerabilities
2. Check authentication/authorization patterns
3. Analyze input validation
4. Review dependency security
```

## Accessing documentation locally

```bash
# Setup local documentation structure
mkdir -p ~/.claude/local-docs/{commands,config,examples}
# Create comprehensive command reference
# ~/.claude/local-docs/commands/reference.md
# ~/.claude/CLAUDE.md
@~/.claude/local-docs/commands/reference.md
```

## CLAUDE.md configuration mastery
## Memory hierarchy (in order of precedence)
## Optimal CLAUDE.md structure

```bash
# Project: [Your Application Name]
```

## Project Overview
## Tech Stack
## Development Commands
## Code Standards
## Instructions for Claude
## Project Structure
## IMPORTANT Workflow Rules
## Advanced CLAUDE.md features

```bash
# Import project documentation
@README.md
@docs/architecture.md
@package.json
# Include personal workflow preferences
@~/.claude/my-coding-standards.md
```

## Vibe coding mastery and workflow optimization
## Core vibe coding principles
## Optimal project structure for vibe coding

```bash
project-root/
├── .claude/
│   ├── commands/           # Custom workflow automations
│   │   ├── review.md      # Code review patterns
│   │   ├── optimize.md    # Performance optimization
│   │   └── feature.md     # Feature development workflow
```

## The "Explore, Plan, Code, Commit" pattern

```bash
"Read the authentication system but don't write code yet"
"Understand the database schema before making changes"
"Analyze the existing component patterns"
"Think harder about implementing OAuth integration"
"Create a detailed plan for the shopping cart feature"
"Outline the testing strategy for this microservice"
```

## Technical implementation and context management
## Context architecture fundamentals

```bash
Total Context = Input Tokens + Current Turn + Thinking Tokens + Tool Use Tokens
```

## Performance optimization strategies

```bash
/clear                    # Reset context between unrelated tasks
/compact "focus on auth"  # Compress conversation with specific focus
/cost                     # Monitor token usage in real-time
"Create a subagent to analyze the test suite architecture"
"Have a specialized agent review security vulnerabilities"  
```

## Advanced technical features

```bash
// .mcp.json configuration
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
```

## Latest features and cutting-edge capabilities
## Claude 4 model capabilities (2025)
## Revolutionary new features

```bash
/security-review          # Ad-hoc security analysis
/install-github-app       # Setup Claude Code GitHub integration
# Dynamic argument passing
/project:fix-issue        # Uses $ARGUMENTS placeholder
/user:security-audit      # Personal commands across all projects
```

## Claude Code SDK (June 2025)

```bash
# Python SDK
pip install claude-code-sdk
# Usage example
from claude_code import ClaudeCode
client = ClaudeCode()
response = client.analyze_codebase("./src", focus="security")
```

## Enterprise and infrastructure advances
## Implementation recommendations
