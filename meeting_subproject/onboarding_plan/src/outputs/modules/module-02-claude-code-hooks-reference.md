## Module 2: Claude Code Hooks Reference [^1] [^2] [^3] [^4]

- **Learning Objectives:**
  - Configure and structure hooks within Claude Code.
  - Implement and manage hook events like PreToolUse and PostToolUse.

- **Key Concepts Covered:**
  - Hook configuration and structure
  - Event-driven programming
  - JSON input/output handling

- **Recommended Activities:**
  - Hook setup and configuration exercises
  - Event implementation projects
  - JSON handling tutorials

- **Time Estimate:** 6 hours

- **Prerequisites:** JSON input/output handling skills

- **Success Criteria:**
  - Configure hooks appropriately for different scenarios.
  - Implement and manage hook events effectively.

- **Resource References:**
  - Event-driven programming guides
  - JSON handling resources

### Key Excerpts

> You can use the environment variable `CLAUDE_PROJECT_DIR` (only available when
Claude Code spawns the hook command) to reference scripts stored in your project,
ensuring they work regardless of Claude's current directory:
> — Source: `Claude Code Hooks Reference.md`

> Claude Code hooks work seamlessly with
[Model Context Protocol (MCP) tools](/en/docs/claude-code/mcp). When MCP servers
provide tools, they appear with a special naming pattern that you can match in
your hooks.
> — Source: `Claude Code Hooks Reference.md`

> * **Timeout**: 60-second execution limit by default, configurable per command.
  * A timeout for an individual command does not affect the other commands.
* **Parallelization**: All matching hooks run in parallel
* **Deduplication**: Multiple identical hook commands are deduplicated automatically
* **Environment**: Runs in current directory with Claude Code's environment
  * The `CLAUDE_PROJECT_DIR` environment variable is available and contains the
    absolute path to the project root directory (where Claude Code was started)
* **Input**: JSON via stdin
* **Output**:
  * PreToolUse/PostToolUse/Stop/SubagentStop: Progress shown in transcript (Ctrl-R)
  * Notification/SessionEnd: Logged to debug only (`--debug`)
  * UserPromptSubmit/SessionStart: stdout added as context for Claude
> — Source: `Claude Code Hooks Reference.md`

> 1. **Inspect hook execution** - Use `claude --debug` to see detailed hook
   execution
2. **Validate JSON schemas** - Test hook input/output with external tools
3. **Check environment variables** - Verify Claude Code's environment is correct
4. **Test edge cases** - Try hooks with unusual file paths or inputs
5. **Monitor system resources** - Check for resource exhaustion during hook
   execution
6. **Use structured logging** - Implement logging in your hook scripts
> — Source: `Claude Code Hooks Reference.md`


### Supplemental Research

- [Get started with Claude Code hooks - Anthropic API](https://docs.anthropic.com/en/docs/claude-code/hooks-guide) — For comprehensive security best practices and safety guidelines, see Security Considerations in the hooks reference documentation. For troubleshooting steps ...
- [Hooks reference - Anthropic API](https://docs.anthropic.com/en/docs/claude-code/hooks) — This page provides reference documentation for implementing hooks in Claude Code. For a quickstart guide with examples, see Get started with Claude Code hooks.
- [Claude Code: Best practices for agentic coding - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices) — This post covers tips and tricks that have proven effective for using Claude Code across various codebases, languages, and environments.

### Relevant Commands & Hooks

- `Configuration` — Claude Code hooks are configured in your [settings files](/en/docs/claude-code/settings): ~/.claude/settings.json - User settings .claude/settings.json - Projec ([ref](reference/Claude Code Hooks Reference.md#configuration))
- `Project-Specific Hook Scripts` — You can use the environment variable CLAUDEPROJECTDIR (only available when Claude Code spawns the hook command) to reference scripts stored in your project, ens ([ref](reference/Claude Code Hooks Reference.md#project-specific-hook-scripts))
- `Hook Output` — There are two ways for hooks to return output back to Claude Code. The output communicates whether to block and any feedback that should be shown to Claude and ([ref](reference/Claude Code Hooks Reference.md#hook-output))
- `JSON Output Example: UserPromptSubmit to Add Context and Validation` — <Note> For UserPromptSubmit hooks, you can inject context using either method: Exit code 0 with stdout: Claude sees the context (special case for UserPromptSubm ([ref](reference/Claude Code Hooks Reference.md#json-output-example-userpromptsubmit-to-add-context-and-validation))
- `Working with MCP Tools` — Claude Code hooks work seamlessly with [Model Context Protocol (MCP) tools](/en/docs/claude-code/mcp). When MCP servers provide tools, they appear with a specia ([ref](reference/Claude Code Hooks Reference.md#working-with-mcp-tools))
- `Disclaimer` — USE AT YOUR OWN RISK: Claude Code hooks execute arbitrary shell commands on your system automatically. By using hooks, you acknowledge that: You are solely resp ([ref](reference/Claude Code Hooks Reference.md#disclaimer))

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
