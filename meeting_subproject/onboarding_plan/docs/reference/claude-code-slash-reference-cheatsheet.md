# Claude Code Slash reference — Cheatsheet

## Built-in slash commands
## Custom slash commands
## Syntax

```bash
/<command-name> [arguments]
```

## Command types

```bash
# Create a project command
mkdir -p .claude/commands
echo "Analyze this code for performance issues and suggest optimizations:" > .claude/commands/optimize.md
# Create a personal command
mkdir -p ~/.claude/commands
echo "Review this code for security vulnerabilities:" > ~/.claude/commands/security-review.md
```

## Features

```bash
# Command definition
echo 'Fix issue #$ARGUMENTS following our coding standards' > .claude/commands/fix-issue.md
# Usage
> /fix-issue 123
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
```

## Context
## Your task

```bash
#### File references
Include file contents in commands using the `@` prefix to [reference files](/en/docs/claude-code/common-workflows#reference-files-and-directories).
For example:
#### Thinking mode
Slash commands can trigger extended thinking by including [extended thinking keywords](/en/docs/claude-code/common-workflows#use-extended-thinking).
```

## Frontmatter

```bash
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [message]
description: Create a git commit
model: claude-3-5-haiku-20241022
---
```

## MCP slash commands
## Command format

```bash
/mcp__<server-name>__<prompt-name> [arguments]
```

## Features

```bash
# Without arguments
> /mcp__github__list_prs
# With arguments
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Bug title" high
```

## Managing MCP connections
## See also
