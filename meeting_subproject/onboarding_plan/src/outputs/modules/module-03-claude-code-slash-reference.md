## Module 3: Claude Code Slash Reference [^1] [^2] [^3] [^4]

- **Learning Objectives:**
  - Utilize built-in and create custom slash commands.
  - Integrate MCP tools with slash commands.

- **Key Concepts Covered:**
  - Built-in slash commands
  - Custom command creation
  - MCP tool integration

- **Recommended Activities:**
  - Slash command exercises
  - Custom command development workshops
  - MCP tool integration labs

- **Time Estimate:** 7 hours

- **Prerequisites:** Command customization skills

- **Success Criteria:**
  - Successfully use and customize slash commands.
  - Integrate MCP tools seamlessly.

- **Resource References:**
  - Slash command documentation
  - MCP tool integration guides

### Key Excerpts

> * [Interactive mode](/en/docs/claude-code/interactive-mode) - Shortcuts, input modes, and interactive features
* [Slash commands](/en/docs/claude-code/slash-commands) - Interactive session commands
* [Quickstart guide](/en/docs/claude-code/quickstart) - Getting started with Claude Code
* [Common workflows](/en/docs/claude-code/common-workflows) - Advanced workflows and patterns
* [Settings](/en/docs/claude-code/settings) - Configuration options
* [SDK documentation](/en/docs/claude-code/sdk) - Programmatic usage and integrations
> — Source: `Claude Code CLI reference.md`

> You can use the environment variable `CLAUDE_PROJECT_DIR` (only available when
Claude Code spawns the hook command) to reference scripts stored in your project,
ensuring they work regardless of Claude's current directory:
> — Source: `Claude Code Hooks Reference.md`

> Custom slash commands allow you to define frequently-used prompts as Markdown files that Claude Code can execute. Commands are organized by scope (project-specific or personal) and support namespacing through directory structures.
> — Source: `Claude Code Slash reference.md`

> Runs when Claude Code starts a new session or resumes an existing session (which
currently does start a new session under the hood). Useful for loading in
development context like existing issues or recent changes to your codebase.
> — Source: `Claude Code Hooks Reference.md`


### Supplemental Research

- [Claude Code: Best Practices and Pro Tips - htdocs.dev](https://htdocs.dev/posts/claude-code-best-practices-and-pro-tips/) — This guide provides tips and tricks for effectively using Claude Code, a command-line tool for agentic coding.
- [Claude Code: Best practices for agentic coding - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices) — A blog post covering tips and tricks that have proven effective for using Claude Code across various codebases, languages, and environments.
- [How I use Claude Code (+ my best tips) - Builder.io](https://www.builder.io/blog/claude-code) — You can also add custom slash commands pretty easily. To add commands, just create a .claude/commands folder, add the command name as a file ...

### Relevant Commands & Hooks

- `Custom slash commands` — Custom slash commands allow you to define frequently-used prompts as Markdown files that Claude Code can execute. Commands are organized by scope (project-speci ([ref](reference/Claude Code Slash reference.md#custom-slash-commands))
- `MCP slash commands` — MCP servers can expose prompts as slash commands that become available in Claude Code. These commands are dynamically discovered from connected MCP servers. ([ref](reference/Claude Code Slash reference.md#mcp-slash-commands))
- `Project-Specific Hook Scripts` — You can use the environment variable CLAUDEPROJECTDIR (only available when Claude Code spawns the hook command) to reference scripts stored in your project, ens ([ref](reference/Claude Code Hooks Reference.md#project-specific-hook-scripts))
- `Complete command reference and documentation access` — Claude Code provides an extensive command system with both built-in and customizable commands: ([ref](reference/Claude Code Technical Guide.md#complete-command-reference-and-documentation-access))
- `CLI flags` — Customize Claude Code's behavior with these command-line flags: | Flag | Description | Example | | :------------------------------- | :------------------------- ([ref](reference/Claude Code CLI reference.md#cli-flags))
- `Configuration` — Claude Code hooks are configured in your [settings files](/en/docs/claude-code/settings): ~/.claude/settings.json - User settings .claude/settings.json - Projec ([ref](reference/Claude Code Hooks Reference.md#configuration))

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
