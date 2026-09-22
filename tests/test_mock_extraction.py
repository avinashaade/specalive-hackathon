from app.agents.requirement_agent import RequirementExtractionAgent


def test_mock_requirement_extraction():

    agent = RequirementExtractionAgent(
        "data/l1_two_tank/input/specification.txt"
    )

    system = agent.mock_extract()

    assert system.name == "L1_TwoTankController"

    assert len(system.components) == 5
    assert len(system.connections) == 4
    assert len(system.states) == 9
    assert len(system.transitions) == 8

    assert system.components[0].name == "TK-101"
    assert system.components[1].name == "TK-102"

    assert system.components[0].attributes["high_level"] == 0.80

    assert system.components[2].name == "XV-101"
    assert system.components[3].name == "XV-102"
    assert system.components[4].name == "XV-103"

    assert system.states[0].name == "IDLE"
    assert system.states[1].name == "FILL_T1"
    assert system.states[-1].name == "SHUTDOWN"

    assert system.assumptions[0].description == (
        "CR-004 values are the current approved values."
    )