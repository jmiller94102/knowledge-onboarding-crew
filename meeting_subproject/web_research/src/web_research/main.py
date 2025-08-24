#!/usr/bin/env python
import sys
import warnings
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

from datetime import datetime

from web_research.crew import LearningContentEnrichmentCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Load .env so Serper/Exa keys are available to tools
load_dotenv(find_dotenv())

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def _default_inputs() -> dict:
    """Build default inputs pointing at the generated onboarding modules."""
    # meeting_subproject/onboarding_plan/src/outputs/modules
    here = Path(__file__).resolve()
    onboarding_outputs = here.parents[3] / "onboarding_plan" / "src" / "outputs" / "modules"
    return {
        'folder_path': str(onboarding_outputs),
        'topics': ''
    }


def run():
    """
    Run the crew.
    """
    inputs = _default_inputs()
    LearningContentEnrichmentCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = _default_inputs()
    try:
        LearningContentEnrichmentCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LearningContentEnrichmentCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = _default_inputs()
    try:
        LearningContentEnrichmentCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
