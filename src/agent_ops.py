import json
from dataclasses import dataclass
from typing import List

@dataclass
class Agent:
    name: str
    environment: str

class AgentOps:
    def __init__(self):
        self.agents = []

    def deploy_agent(self, agent: Agent):
        self.agents.append(agent)
        return f"Agent {agent.name} deployed to {agent.environment}"

    def get_deployed_agents(self, environment: str = None):
        if environment:
            return [agent for agent in self.agents if agent.environment == environment]
        return self.agents

    def save_to_json(self, filename: str):
        data = [{"name": agent.name, "environment": agent.environment} for agent in self.agents]
        with open(filename, "w") as f:
            json.dump(data, f)

    def load_from_json(self, filename: str):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.agents = [Agent(agent["name"], agent["environment"]) for agent in data]
        except FileNotFoundError:
            pass
