from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

from crewai_tools import (FileReadTool)
import os



@CrewBase
class MeetingTranscriptFormatterCrew:
    """MeetingTranscriptFormatter crew"""

    
    @agent
    def meeting_transcript_analyst(self) -> Agent:
        
        return Agent(
            config=self.agents_config["meeting_transcript_analyst"],
            tools=[
				FileReadTool()
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
                temperature=float(os.getenv("MODEL_TEMPERATURE", "0.7")),
            ),
        )
    

    
    @task
    def process_meeting_transcript(self) -> Task:
        return Task(
            config=self.tasks_config["process_meeting_transcript"],
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the MeetingTranscriptFormatter crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
