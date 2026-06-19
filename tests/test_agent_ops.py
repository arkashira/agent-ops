import json
from src.agent_ops import Agent, AgentOps

def test_deploy_agent():
    agent_ops = AgentOps()
    agent = Agent("test_agent", "dev")
    result = agent_ops.deploy_agent(agent)
    assert result == "Agent test_agent deployed to dev"
    assert len(agent_ops.get_deployed_agents()) == 1

def test_get_deployed_agents():
    agent_ops = AgentOps()
    agent1 = Agent("test_agent1", "dev")
    agent2 = Agent("test_agent2", "prod")
    agent_ops.deploy_agent(agent1)
    agent_ops.deploy_agent(agent2)
    assert len(agent_ops.get_deployed_agents("dev")) == 1
    assert len(agent_ops.get_deployed_agents("prod")) == 1
    assert len(agent_ops.get_deployed_agents()) == 2

def test_save_to_json():
    agent_ops = AgentOps()
    agent1 = Agent("test_agent1", "dev")
    agent2 = Agent("test_agent2", "prod")
    agent_ops.deploy_agent(agent1)
    agent_ops.deploy_agent(agent2)
    agent_ops.save_to_json("agents.json")
    with open("agents.json", "r") as f:
        data = json.load(f)
    assert len(data) == 2
    assert data[0]["name"] == "test_agent1"
    assert data[1]["name"] == "test_agent2"

def test_load_from_json():
    agent_ops = AgentOps()
    agent1 = Agent("test_agent1", "dev")
    agent2 = Agent("test_agent2", "prod")
    agent_ops.deploy_agent(agent1)
    agent_ops.deploy_agent(agent2)
    agent_ops.save_to_json("agents.json")
    agent_ops = AgentOps()
    agent_ops.load_from_json("agents.json")
    assert len(agent_ops.get_deployed_agents()) == 2
    assert agent_ops.get_deployed_agents()[0].name == "test_agent1"
    assert agent_ops.get_deployed_agents()[1].name == "test_agent2"
