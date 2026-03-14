import json
from utils.agent_decorator import agent


@agent("Aggregator Agent")
def aggregator_agent(state):

    validated = state["validated_output"]

    with open("validated_locators.json", "w") as f:
        json.dump(validated, f, indent=2)

    return state