from app.agents.requirement_agent import RequirementExtractionAgent
from app.generators.sysml_generator import generate_sysml


def test_sysml_generation():

    agent = RequirementExtractionAgent(
        "data/l1_two_tank/input/specification.txt"
    )

    system = agent.mock_extract()

    sysml = generate_sysml(system)

    assert "package L1_TwoTankController" in sysml

    # Part definitions
    assert "part def Tank" in sysml
    assert "part def OnOffValve" in sysml

    # Component instances
    assert "part TK_101 : Tank;" in sysml
    assert "part TK_102 : Tank;" in sysml

    assert "part XV_101 : OnOffValve;" in sysml
    assert "part XV_102 : OnOffValve;" in sysml
    assert "part XV_103 : OnOffValve;" in sysml

    # Controller states
    assert "IDLE" in sysml
    assert "FILL_T1" in sysml
    assert "TRANSFER_T1_T2" in sysml
    assert "DRAIN_T2" in sysml
    assert "PAUSED" in sysml
    assert "SHUTDOWN" in sysml

    # State transition information
    assert "Tank 1 level >= 0.80 m" in sysml
    assert "Tank 1 level <= 0.05 m" in sysml
    assert "Tank 2 level <= 0.05 m" in sysml

    # Engineering assumption
    assert "CR-004 values are the current approved values." in sysml