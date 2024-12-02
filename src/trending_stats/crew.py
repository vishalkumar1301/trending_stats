from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from pydantic import BaseModel, Field


class Statistic(BaseModel):
    value: str = Field(..., description="Value of the statistic.")
    text: str = Field(..., description="Text of the statistic.")
    description: str = Field(..., description="Description of the statistic.")
    entities: list[str] = Field(..., description="Entities mentioned in the statistic.")


class ListOfStatistics(BaseModel):
    statistics: list[Statistic] = Field(..., description="List of statistics.")


@CrewBase
class TrendingStats():
	"""TrendingStats crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def stats_extractor(self) -> Agent:
		return Agent(
			config=self.agents_config['stats_extractor'],
		)

	@task
	def stats_extraction_task(self) -> Task:
		return Task(
			config=self.tasks_config['stats_extraction_task'],
			output_json=ListOfStatistics,
			output_file='stats_report.json'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TrendingStats crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)
