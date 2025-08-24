## Module 2: Interactive Session Control with Slash Commands [^1] [^2] [^3] [^4]

- **Learning Objectives:**
  - Use slash commands to enhance interactive sessions.

- **Key Concepts Covered:**
  - Built-in and custom slash commands.

- **Recommended Activities:**
  - Slash command scripts exercises.
  - Role-play scenarios using slash commands.

- **Time Estimates:**
  - Approximately 4 hours.

- **Prerequisites:**
  - Familiarity with CLI and basic scripting.

- **Success Criteria:**
  - Demonstrate effective use of slash commands in sessions.

- **Resource References:**
  - Claude Code Slash Reference.

---

### Key Excerpts

> * [Interactive mode](/en/docs/claude-code/interactive-mode) - Shortcuts, input modes, and interactive features
* [Slash commands](/en/docs/claude-code/slash-commands) - Interactive session commands
* [Quickstart guide](/en/docs/claude-code/quickstart) - Getting started with Claude Code
* [Common workflows](/en/docs/claude-code/common-workflows) - Advanced workflows and patterns
* [Settings](/en/docs/claude-code/settings) - Configuration options
* [SDK documentation](/en/docs/claude-code/sdk) - Programmatic usage and integrations
> — Source: `Claude Code CLI reference.md`

> Custom slash commands allow you to define frequently-used prompts as Markdown files that Claude Code can execute. Commands are organized by scope (project-specific or personal) and support namespacing through directory structures.
> — Source: `Claude Code Slash reference.md`

> Execute bash commands before the slash command runs using the `!` prefix. The output is included in the command context. You *must* include `allowed-tools` with the `Bash` tool, but you can choose the specific bash commands to allow.
> — Source: `Claude Code Slash reference.md`

> ### Best Practices for Using Cloud Code
- Key discussion points:
  - The significance of using hooks and slash commands to maintain context.
  - Strategies for using subagents effectively in complex tasks.
- **Decisions made:** Advocated for a more structured approach to using Cloud Code.
- **Action items:**
  - Create a project index to keep track of essential files and dependencies.
> — Source: `cloud-code-masterclass-insights.md`


### Supplemental Research

- [Enabling interactivity with Slash commands - Slack API](https://api.slack.com/interactivity/slash-commands) — First, head to your App Management dashboard, select the app you wish to work with, then select Slash Commands under Features in the navigation menu. You'll be ...
- [Claude Code: Best practices for agentic coding - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices) — A blog post covering tips and tricks that have proven effective for using Claude Code across various codebases, languages, and environments.
- [Step-by-Step Guide to Building Custom Slash Commands in Slack](https://moldstud.com/articles/p-step-by-step-guide-to-building-custom-slash-commands-in-slack) — Learn how to create custom slash commands in Slack with this detailed step-by-step guide. Enhance your team's productivity and streamline ...

### Relevant Commands & Hooks

- `See also` — [Interactive mode](/en/docs/claude-code/interactive-mode) - Shortcuts, input modes, and interactive features [Slash commands](/en/docs/claude-code/slash-command ([ref](reference/Claude Code CLI reference.md#see-also))
- `Built-in slash commands` — | Command | Purpose | | :------------------------ | :----------------------------------------------------------------------------------------------------------- ([ref](reference/Claude Code Slash reference.md#built-in-slash-commands))
- `Custom slash commands` — Custom slash commands allow you to define frequently-used prompts as Markdown files that Claude Code can execute. Commands are organized by scope (project-speci ([ref](reference/Claude Code Slash reference.md#custom-slash-commands))
- `Bash command execution` — Execute bash commands before the slash command runs using the ! prefix. The output is included in the command context. You must include allowed-tools with the B ([ref](reference/Claude Code Slash reference.md#bash-command-execution))
- `Thinking mode` — Slash commands can trigger extended thinking by including [extended thinking keywords](/en/docs/claude-code/common-workflows#use-extended-thinking). ([ref](reference/Claude Code Slash reference.md#thinking-mode))
- `MCP slash commands` — MCP servers can expose prompts as slash commands that become available in Claude Code. These commands are dynamically discovered from connected MCP servers. ([ref](reference/Claude Code Slash reference.md#mcp-slash-commands))

---

> Note: This module is synthesized from meeting summaries in `/Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries`.


---

## References
[^1]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/Claude Code CLI reference.md
[^2]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/Claude Code Hooks Reference.md
[^3]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/Claude Code Slash reference.md
[^4]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/Claude Code Technical Guide.md
[^5]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/claude-code-insights.md
[^6]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/claude-code-masterclass-insights.md
[^7]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/cloud-code-discussion-insights.md
[^8]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/cloud-code-insights.md
[^9]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/cloud-code-masterclass-insights.md
[^10]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/cloud-code-masterclass.md
[^11]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/cloud-code-workshop.md
[^12]: /Users/johnney-fivemiller/CascadeProjects/windsurf-project/meeting_summaries/leveraging-claude-code-ai-development.md
