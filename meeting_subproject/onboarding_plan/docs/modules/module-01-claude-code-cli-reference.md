## Module 1: Claude Code CLI Reference [^1] [^2] [^3] [^4]

- **Learning Objectives:**
  - Understand and utilize basic CLI commands and flags.
  - Start and manage interactive REPL sessions.
  - Process queries using the SDK.

- **Key Concepts Covered:**
  - CLI commands and flags
  - Session management
  - Command customization

- **Recommended Activities:**
  - Interactive CLI command exercises
  - REPL session walkthrough
  - SDK query processing tasks

- **Time Estimate:** 5 hours

- **Prerequisites:** Basic command-line interface (CLI) skills

- **Success Criteria:**
  - Demonstrate the ability to execute and customize CLI commands.
  - Successfully manage sessions using the REPL.

- **Resource References:**
  - Internal CLI command documentation
  - SDK usage guidelines

### Key Excerpts

> You can use the environment variable `CLAUDE_PROJECT_DIR` (only available when
Claude Code spawns the hook command) to reference scripts stored in your project,
ensuring they work regardless of Claude's current directory:
> — Source: `Claude Code Hooks Reference.md`

> * [Interactive mode](/en/docs/claude-code/interactive-mode) - Shortcuts, input modes, and interactive features
* [CLI reference](/en/docs/claude-code/cli-reference) - Command-line flags and options
* [Settings](/en/docs/claude-code/settings) - Configuration options
* [Memory management](/en/docs/claude-code/memory) - Managing Claude's memory across sessions
> — Source: `Claude Code Slash reference.md`

> * [Interactive mode](/en/docs/claude-code/interactive-mode) - Shortcuts, input modes, and interactive features
* [Slash commands](/en/docs/claude-code/slash-commands) - Interactive session commands
* [Quickstart guide](/en/docs/claude-code/quickstart) - Getting started with Claude Code
* [Common workflows](/en/docs/claude-code/common-workflows) - Advanced workflows and patterns
* [Settings](/en/docs/claude-code/settings) - Configuration options
* [SDK documentation](/en/docs/claude-code/sdk) - Programmatic usage and integrations
> — Source: `Claude Code CLI reference.md`

> Runs when Claude Code starts a new session or resumes an existing session (which
currently does start a new session under the hood). Useful for loading in
development context like existing issues or recent changes to your codebase.
> — Source: `Claude Code Hooks Reference.md`


### Supplemental Research

- [Claude Code: Best Practices and Pro Tips - htdocs.dev](https://htdocs.dev/posts/claude-code-best-practices-and-pro-tips/) — This guide provides tips and tricks for effectively using Claude Code, a command-line tool for agentic coding. Using Claude Code as a Bash CLI.
- [Claude Code: Best practices for agentic coding - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices) — A blog post covering tips and tricks that have proven effective for using Claude Code across various codebases, languages, and environments.
- [Cooking with Claude Code: The Complete Guide - Sid Bharath](https://www.siddharthbharath.com/claude-code-the-complete-guide/) — Check code follows our TypeScript and React conventions 2. Verify proper error handling and loading states 3. Ensure accessibility standards are ...

### Relevant Commands & Hooks

- `CLI flags` — Customize Claude Code's behavior with these command-line flags: | Flag | Description | Example | | :------------------------------- | :------------------------- ([ref](reference/Claude Code CLI reference.md#cli-flags))
- `Project-Specific Hook Scripts` — You can use the environment variable CLAUDEPROJECTDIR (only available when Claude Code spawns the hook command) to reference scripts stored in your project, ens ([ref](reference/Claude Code Hooks Reference.md#project-specific-hook-scripts))
- `Complete command reference and documentation access` — Claude Code provides an extensive command system with both built-in and customizable commands: ([ref](reference/Claude Code Technical Guide.md#complete-command-reference-and-documentation-access))
- `Custom slash commands` — Custom slash commands allow you to define frequently-used prompts as Markdown files that Claude Code can execute. Commands are organized by scope (project-speci ([ref](reference/Claude Code Slash reference.md#custom-slash-commands))
- `MCP slash commands` — MCP servers can expose prompts as slash commands that become available in Claude Code. These commands are dynamically discovered from connected MCP servers. ([ref](reference/Claude Code Slash reference.md#mcp-slash-commands))
- `See also` — [Interactive mode](/en/docs/claude-code/interactive-mode) - Shortcuts, input modes, and interactive features [CLI reference](/en/docs/claude-code/cli-reference) ([ref](reference/Claude Code Slash reference.md#see-also))

---

> Note: This module is synthesized from meeting summaries in `/Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries`.


---

## References
[^1]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/Claude Code CLI reference.md
[^2]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/Claude Code Hooks Reference.md
[^3]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/Claude Code Slash reference.md
[^4]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/Claude Code Technical Guide.md
[^5]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/claude-code-masterclass-insights.md
[^6]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/cloud-code-workshop-insights.md
