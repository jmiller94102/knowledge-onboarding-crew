from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

from crewai_tools import CrewaiEnterpriseTools


@CrewBase
class IntelligentRequestProcessingSystemCrew:
    """IntelligentRequestProcessingSystem crew"""

    
    @agent
    def request_intake_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["request_intake_specialist"],
            tools=[

            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    
    @agent
    def requirements_clarification_analyst(self) -> Agent:
        
        return Agent(
            config=self.agents_config["requirements_clarification_analyst"],
            tools=[

            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    
    @agent
    def request_board_manager(self) -> Agent:
        enterprise_actions_tool = CrewaiEnterpriseTools(
            actions_list=[
                
                "google_sheets_create_row",
                
            ],
        )
        
        return Agent(
            config=self.agents_config["request_board_manager"],
            tools=[
				*enterprise_actions_tool
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o",
                temperature=0.7,
            ),
        )
    

    
    @task
    def analyze_initial_request(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_initial_request"],
        )
    
    @task
    def generate_clarifying_questions(self) -> Task:
        return Task(
            config=self.tasks_config["generate_clarifying_questions"],
        )
    
    @task
    def structure_request_for_board(self) -> Task:
        return Task(
            config=self.tasks_config["structure_request_for_board"],
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the IntelligentRequestProcessingSystem crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
