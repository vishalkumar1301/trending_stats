from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from trending_stats.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class TrendingStats():
	"""TrendingStats crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def stats_extractor(self) -> Agent:
		return Agent(
			config=self.agents_config['stats_extractor'],
			llm=LLM(model="ollama/phi3.5", base_url='http://localhost:11434'),
			verbose=True
		)

	@task
	def stats_extraction_task(self) -> Task:
		return Task(
			config=self.tasks_config['stats_extraction_task'],
			verbose=True,
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
