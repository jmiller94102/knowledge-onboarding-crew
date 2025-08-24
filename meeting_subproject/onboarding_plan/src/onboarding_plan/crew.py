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
class DocumentationLearningPlanGeneratorCrew:
    """DocumentationLearningPlanGenerator crew"""

    def __init__(self):
        # Allow overriding per-subproject, then fall back to global defaults
        self._model_name = os.environ.get("ONBOARDING_MODEL_NAME", os.environ.get("MODEL_NAME", "gpt-4o"))
        try:
            self._temperature = float(os.environ.get("ONBOARDING_MODEL_TEMPERATURE", os.environ.get("MODEL_TEMPERATURE", "0.7")))
        except Exception:
            self._temperature = 0.7
    
    @agent
    def documentation_reader_and_cataloger(self) -> Agent:
        
        return Agent(
            config=self.agents_config["documentation_reader_and_cataloger"],
            tools=[
				FileReadTool()
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model=self._model_name,
                temperature=self._temperature,
            ),
        )
    
    @agent
    def content_analyzer_and_knowledge_mapper(self) -> Agent:
        
        return Agent(
            config=self.agents_config["content_analyzer_and_knowledge_mapper"],
            tools=[

            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model=self._model_name,
                temperature=self._temperature,
            ),
        )
    
    @agent
    def learning_plan_designer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["learning_plan_designer"],
            tools=[

            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model=self._model_name,
                temperature=self._temperature,
            ),
        )
    

    
    @task
    def catalog_documentation_files(self) -> Task:
        return Task(
            config=self.tasks_config["catalog_documentation_files"],
        )
    
    @task
    def analyze_learning_content_and_map_knowledge(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_learning_content_and_map_knowledge"],
        )
    
    @task
    def design_structured_learning_onboarding_plan(self) -> Task:
        return Task(
            config=self.tasks_config["design_structured_learning_onboarding_plan"],
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the DocumentationLearningPlanGenerator crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
