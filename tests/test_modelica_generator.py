from app.agents.requirement_agent import RequirementExtractionAgent
from app.generators.modelica_generator import generate_modelica


def test_modelica_generation():

    agent = RequirementExtractionAgent(
        "data/l1_two_tank/input/specification.txt"
    )

    system = agent.mock_extract()

    modelica = generate_modelica(system)

    # Model declaration
    assert "model L1_TwoTankController" in modelica

    # Tank variables
    assert "tank1Level" in modelica
    assert "tank2Level" in modelica

    # Valve commands
    assert "v1Open" in modelica
    assert "v2Open" in modelica
    assert "v3Open" in modelica

    # State controller
    assert "state" in modelica
    assert "FILL_T1" in modelica
    assert "TRANSFER_T1_T2" in modelica
    assert "DRAIN_T2" in modelica

    # Tank dynamics
    assert "der(tank1Level)" in modelica
    assert "der(tank2Level)" in modelica

    # State transitions
    assert "tank1Level >= tank1HighLevel" in modelica
    assert "tank1Level <= tank1LowLevel" in modelica
    assert "tank2Level <= tank2LowLevel" in modelica

    # Modelica model must close correctly
    assert "end L1_TwoTankController;" in modelica