from pathlib import Path

from app.agents.requirement_agent import RequirementExtractionAgent
from app.generators.file_writer import save_text
from app.generators.sysml_generator import generate_sysml


def generate_l1_sysml(output_path: str) -> Path:
    """
    Generate the L1 Two-Tank SysML file.

    Flow:
    specification.txt
        ↓
    RequirementExtractionAgent
        ↓
    SystemModel
        ↓
    SysML Generator
        ↓
    .sysml file
    """

    agent = RequirementExtractionAgent(
        "data/l1_two_tank/input/specification.txt"
    )

    system = agent.mock_extract()

    sysml_content = generate_sysml(system)

    save_text(
        sysml_content,
        output_path,
    )

    return Path(output_path)