from app.agents.requirement_agent import RequirementExtractionAgent


def test_ai_connection():

    agent = RequirementExtractionAgent(
        "data/l1_two_tank/input/specification.txt"
    )

    specification = agent.load_specification()

    response = agent.ask_ai(specification)

    assert response is not None
    assert len(response) > 0

    print("\nAI RESPONSE:\n")
    print(response)