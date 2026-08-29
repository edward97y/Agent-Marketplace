class AgentFactory:

    @staticmethod
    def get_agent(
        agents: dict,
        agent_type: str,
    ):
        agent = agents.get(agent_type)

        if agent is None:
            raise ValueError(
                f"Agent type '{agent_type}' not found"
            )

        return agent