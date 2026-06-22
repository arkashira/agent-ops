from agent_ops import AgentOps, ScalingPolicy

def test_define_scaling_policy():
    agent_ops = AgentOps()
    policy_id = "test_policy"
    policy = ScalingPolicy(min_agents=1, max_agents=10, cpu_threshold=0.5)
    agent_ops.define_scaling_policy(policy_id, policy)
    assert agent_ops.scaling_policies[policy_id] == policy

def test_update_load_tags():
    agent_ops = AgentOps()
    load_tags = {"tag1": 10, "tag2": 20}
    agent_ops.update_load_tags(load_tags)
    assert agent_ops.load_tags == load_tags

def test_spawn_agents():
    agent_ops = AgentOps()
    policy_id = "test_policy"
    policy = ScalingPolicy(min_agents=1, max_agents=10, cpu_threshold=0.5)
    agent_ops.define_scaling_policy(policy_id, policy)
    new_agents = agent_ops.spawn_agents(policy_id)
    assert new_agents == 1

def test_terminate_agents():
    agent_ops = AgentOps()
    policy_id = "test_policy"
    policy = ScalingPolicy(min_agents=1, max_agents=10, cpu_threshold=0.5)
    agent_ops.define_scaling_policy(policy_id, policy)
    agent_ops.agents[policy_id] = 5
    new_agents = agent_ops.terminate_agents(policy_id)
    assert new_agents == 4

def test_get_agents():
    agent_ops = AgentOps()
    policy_id = "test_policy"
    policy = ScalingPolicy(min_agents=1, max_agents=10, cpu_threshold=0.5)
    agent_ops.define_scaling_policy(policy_id, policy)
    agent_ops.agents[policy_id] = 5
    assert agent_ops.get_agents(policy_id) == 5

def test_log_scaling_action():
    agent_ops = AgentOps()
    policy_id = "test_policy"
    action = "spawn"
    agent_ops.log_scaling_action(policy_id, action)
    # No assertion, just checking that it runs without error

def test_respect_resource_limits():
    agent_ops = AgentOps()
    policy_id = "test_policy"
    policy = ScalingPolicy(min_agents=1, max_agents=10, cpu_threshold=0.5)
    agent_ops.define_scaling_policy(policy_id, policy)
    agent_ops.agents[policy_id] = 15
    new_agents = agent_ops.respect_resource_limits(policy_id)
    assert new_agents == 10
