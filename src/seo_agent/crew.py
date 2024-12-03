from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from dotenv import load_dotenv
from seo_agent.tools.custom_tool import SemrushTool, StoreInDatabaseTool, FetchFromDatabaseTool, ShopifyPostTool		
from crewai_tools import ScrapeWebsiteTool	
import os


load_dotenv()

# Set up environment variables
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY_HERE"

@CrewBase
class SeoAgent():
	"""SeoAgent crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@before_kickoff # Optional hook to be executed before the crew starts
	def pull_data_example(self, inputs):
		# Example of pulling data from an external API, dynamically changing the inputs
		inputs['extra_data'] = "This is extra data"
		return inputs

	@after_kickoff # Optional hook to be executed after the crew has finished
	def log_results(self, output):
		# Example of logging results, dynamically changing the output
		print(f"Results: {output}")
		return output

	@agent
	def seo_director(self) -> Agent:
		return Agent(
			config=self.agents_config['seo_director'],
			tools=[ShopifyPostTool()],
			verbose=True,
			
		)

	@agent
	def backlink_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['backlink_agent'],
			tools=[SemrushTool()],
			verbose=True,
			
		)
	
	@agent
	def content_agents(self) -> Agent:
		return Agent(
			config=self.agents_config['content_agents'],
			tools=[SemrushTool(), ScrapeWebsiteTool(), StoreInDatabaseTool()],
			verbose=True,
		)

	@agent
	def content_brief_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['content_brief_manager'],
			tools=[FetchFromDatabaseTool()],
			verbose=True,
			
		)

	@task
	def backlink_task(self) -> Task:
		return Task(
			config=self.tasks_config['backlink_task'],
		)

	@task
	def content_creation_tasks(self) -> Task:	
		return Task(
			config=self.tasks_config['content_creation_tasks'],
		)
	
	@task
	def content_brief_manager_task(self) -> Task:
		return Task(
			config=self.tasks_config['content_brief_manager_task'],
		)
	
	@task
	def seo_director_task(self) -> Task:
		return Task(
			config=self.tasks_config['seo_director_task'],
		)
	
	
	@crew
	def crew(self) -> Crew:
		"""Creates the SeoAgent crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
