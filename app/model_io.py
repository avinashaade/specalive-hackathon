import json

from app.system_schema import SystemModel


def save_system_model(system: SystemModel, output_path: str) -> None:
    """Save a SystemModel as a formatted JSON file."""

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            system.model_dump(),
            file,
            indent=2,
        )


def load_system_model(input_path: str) -> SystemModel:
    """Load a SystemModel from a JSON file."""

    with open(input_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return SystemModel.model_validate(data)