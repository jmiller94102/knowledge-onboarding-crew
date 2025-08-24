from crewai import Agent, Crew, Process, Task, LLM
import os
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

from crewai_tools import (
	FileReadTool,
	SerperDevTool,
	EXASearchTool
)



@CrewBase
class LearningContentEnrichmentCrew:
    """LearningContentEnrichment crew"""

    
    @agent
    def learning_content_analyzer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["learning_content_analyzer"],
            tools=[
				FileReadTool()
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    
    @agent
    def research_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["research_specialist"],
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    
    @agent
    def advanced_search_researcher(self) -> Agent:
        
        return Agent(
            config=self.agents_config["advanced_search_researcher"],
            tools=[
				EXASearchTool(api_key=os.environ.get("EXA_API_KEY"))
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    
    @agent
    def content_enrichment_writer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["content_enrichment_writer"],
            tools=[

            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    

    
    @task
    def analyze_learning_modules(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_learning_modules"],
        )
    
    @task
    def conduct_general_research(self) -> Task:
        return Task(
            config=self.tasks_config["conduct_general_research"],
        )
    
    @task
    def perform_advanced_research(self) -> Task:
        return Task(
            config=self.tasks_config["perform_advanced_research"],
        )
    
    @task
    def create_enriched_learning_content(self) -> Task:
        return Task(
            config=self.tasks_config["create_enriched_learning_content"],
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the LearningContentEnrichment crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
