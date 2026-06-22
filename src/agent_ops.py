import json
from dataclasses import dataclass
from typing import List

@dataclass
class ScalingPolicy:
    min_agents: int
    max_agents: int
    cpu_threshold: float

class AgentOps:
    def __init__(self):
        self.scaling_policies = {}
        self.load_tags = {}
        self.agents = {}

    def define_scaling_policy(self, policy_id: str, policy: ScalingPolicy):
        self.scaling_policies[policy_id] = policy

    def update_load_tags(self, load_tags: dict):
        self.load_tags = load_tags

    def spawn_agents(self, policy_id: str):
        policy = self.scaling_policies.get(policy_id)
        if policy:
            current_agents = self.agents.get(policy_id, 0)
            if current_agents < policy.max_agents:
                new_agents = min(policy.max_agents, current_agents + 1)
                self.agents[policy_id] = new_agents
                return new_agents
        return 0

    def terminate_agents(self, policy_id: str):
        policy = self.scaling_policies.get(policy_id)
        if policy:
            current_agents = self.agents.get(policy_id, 0)
            if current_agents > policy.min_agents:
                new_agents = max(policy.min_agents, current_agents - 1)
                self.agents[policy_id] = new_agents
                return new_agents
        return 0

    def get_agents(self, policy_id: str):
        return self.agents.get(policy_id, 0)

    def log_scaling_action(self, policy_id: str, action: str):
        print(f"Scaling action: {action} for policy {policy_id}")

    def respect_resource_limits(self, policy_id: str):
        policy = self.scaling_policies.get(policy_id)
        if policy:
            current_agents = self.agents.get(policy_id, 0)
            if current_agents > policy.max_agents:
                self.agents[policy_id] = policy.max_agents
                return policy.max_agents
        return 0
