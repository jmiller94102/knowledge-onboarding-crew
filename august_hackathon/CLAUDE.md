# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a crewAI-based multi-agent AI system called AugustHackathon. The project uses Python with crewAI framework to coordinate multiple AI agents that collaborate on research and reporting tasks. The system includes a YouTube transcription utility that uses Google's Gemini API.

## Common Commands

### Running the System
```bash
# Main command to run the crew
crewai run

# Alternative using Python module
python -m august_hackathon.main

# Install dependencies (requires uv)
crewai install
```

### Available Scripts (via pyproject.toml)
```bash
# Run the crew
august_hackathon

# Train the crew (requires iterations and filename)
python -c "from august_hackathon.main import train; train()" <iterations> <filename>

# Replay crew execution from specific task
python -c "from august_hackathon.main import replay; replay()" <task_id>

# Test crew execution
python -c "from august_hackathon.main import test; test()" <iterations> <eval_llm>
```

### YouTube Transcription
```bash
# Requires GOOGLE_API_KEY environment variable
export GOOGLE_API_KEY=your_key_here
python -m august_hackathon.youtube_transcribe --url "https://www.youtube.com/watch?v=VIDEO_ID"

# Save to file
python -m august_hackathon.youtube_transcribe --url "URL" --out transcript.txt
```

## Architecture

### Core Structure
- **src/august_hackathon/**: Main package directory
  - **main.py**: Entry point with run/train/replay/test functions
  - **crew.py**: CrewAI crew definition with agents and tasks
  - **config/**: YAML configuration files for agents and tasks
  - **tools/**: Custom tool implementations

### Agent System
The system uses two main agents defined in `config/agents.yaml`:
1. **Researcher**: Senior data researcher focused on finding cutting-edge developments
2. **Reporting Analyst**: Creates detailed reports from research findings

### Task Flow
Sequential process defined in `config/tasks.yaml`:
1. **Research Task**: Conducts thorough research on specified topic
2. **Reporting Task**: Expands research into full markdown report (saved as `report.md`)

### Configuration
- Agent configurations are parameterized with `{topic}` placeholders
- Tasks use `{topic}` and `{current_year}` variables
- Default topic is "AI LLMs" when run locally
- Output is generated as `report.md` in the root directory

## Environment Setup

### Requirements
- Python >=3.10 <3.13
- UV package manager
- OpenAI API key in `.env` file
- Google API key for YouTube transcription (optional)

### Dependencies
Main dependency is `crewai[tools]>=0.121.1,<1.0.0` managed through pyproject.toml.

## Custom Tools

The project includes a template for custom tools in `tools/custom_tool.py` using crewAI's BaseTool class. Tools should inherit from BaseTool and implement the `_run` method with proper Pydantic schema validation.