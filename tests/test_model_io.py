from app.agents.requirement_agent import RequirementExtractionAgent
from app.model_io import save_system_model, load_system_model


def test_system_model_json_round_trip(tmp_path):

    agent = RequirementExtractionAgent(
        "data/l1_two_tank/input/specification.txt"
    )

    original = agent.mock_extract()

    output_file = tmp_path / "l1_system_model.json"

    save_system_model(original, str(output_file))

    loaded = load_system_model(str(output_file))

    assert loaded.name == original.name
    assert len(loaded.components) == len(original.components)
    assert len(loaded.connections) == len(original.connections)
    assert len(loaded.states) == len(original.states)
    assert len(loaded.transitions) == len(original.transitions)

    assert loaded.components[0].name == "TK-101"
    assert loaded.components[0].attributes["high_level"] == 0.80