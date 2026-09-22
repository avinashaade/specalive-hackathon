import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.system_schema import (
    SystemModel,
    Component,
    Connection,
    State,
    Transition,
    Assumption,
)


class RequirementExtractionAgent:
    """
    Converts an engineering specification into a structured
    SystemModel representation.
    """

    def __init__(self, specification_path: str):
        self.specification_path = Path(specification_path)

        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is not configured.")

        self.client = OpenAI(api_key=api_key)

    def load_specification(self) -> str:
        """Read the engineering specification."""

        if not self.specification_path.exists():
            raise FileNotFoundError(
                f"Specification not found: {self.specification_path}"
            )

        return self.specification_path.read_text(encoding="utf-8")

    def ask_ai(self, specification: str) -> str:
        """Send the specification to the OpenAI API."""

        response = self.client.responses.create(
            model="gpt-5.6-luna",
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are an engineering requirements extraction assistant. "
                        "Read the provided engineering specification and identify "
                        "components, connections, states, transitions, attributes, "
                        "assumptions, and missing information. "
                        "Do not invent engineering details."
                    ),
                },
                {
                    "role": "user",
                    "content": specification,
                },
            ],
        )

        return response.output_text

    def mock_extract(self) -> SystemModel:
        """
        Temporary offline extractor used while API access is unavailable.

        This simulates the structured result that an AI requirement
        extraction agent will eventually produce.
        """

        specification = self.load_specification()

        if "SPECALIVE L1" not in specification:
            raise ValueError("Unexpected specification format.")

        tank1 = Component(
            name="TK-101",
            type="Tank",
            description="Tank 1",
            attributes={
                "area": 1.2,
                "height": 1.0,
                "initial_level": 0.05,
                "high_level": 0.80,
                "low_level": 0.05,
            },
        )

        tank2 = Component(
            name="TK-102",
            type="Tank",
            description="Tank 2",
            attributes={
                "area": 1.4,
                "height": 1.0,
                "initial_level": 0.05,
                "low_level": 0.05,
            },
        )

        valve1 = Component(
            name="XV-101",
            type="OnOffValve",
            description="Feed valve",
            attributes={
                "nominal_flow": 0.006,
                "fail_position": "Closed",
            },
        )

        valve2 = Component(
            name="XV-102",
            type="OnOffValve",
            description="Transfer valve",
            attributes={
                "nominal_flow": 0.0045,
                "fail_position": "Closed",
            },
        )

        valve3 = Component(
            name="XV-103",
            type="OnOffValve",
            description="Drain valve",
            attributes={
                "nominal_flow": 0.005,
                "fail_position": "Closed",
            },
        )

        return SystemModel(
            name="L1_TwoTankController",
            description="Two-tank sequence control system",
            components=[
                tank1,
                tank2,
                valve1,
                valve2,
                valve3,
            ],
            connections=[
                Connection(
                    source="XV-101.outlet",
                    target="TK-101.inlet",
                ),
                Connection(
                    source="TK-101.outlet",
                    target="XV-102.inlet",
                ),
                Connection(
                    source="XV-102.outlet",
                    target="TK-102.inlet",
                ),
                Connection(
                    source="TK-102.outlet",
                    target="XV-103.inlet",
                ),
            ],
            states=[
                State(name="IDLE"),
                State(name="FILL_T1"),
                State(name="WAIT_AFTER_FILL"),
                State(name="TRANSFER_T1_T2"),
                State(name="WAIT_AFTER_TRANSFER"),
                State(name="DRAIN_T2"),
                State(name="WAIT_AFTER_DRAIN"),
                State(name="PAUSED"),
                State(name="SHUTDOWN"),
            ],
            transitions=[
                Transition(
                    source="IDLE",
                    target="FILL_T1",
                    trigger="START",
                ),
                Transition(
                    source="FILL_T1",
                    target="WAIT_AFTER_FILL",
                    condition="Tank 1 level >= 0.80 m",
                    action="Close XV-101",
                ),
                Transition(
                    source="WAIT_AFTER_FILL",
                    target="TRANSFER_T1_T2",
                    condition="10 s wait completed",
                    action="Open XV-102",
                ),
                Transition(
                    source="TRANSFER_T1_T2",
                    target="WAIT_AFTER_TRANSFER",
                    condition="Tank 1 level <= 0.05 m",
                    action="Close XV-102",
                ),
                Transition(
                    source="WAIT_AFTER_TRANSFER",
                    target="DRAIN_T2",
                    condition="12 s wait completed",
                    action="Open XV-103",
                ),
                Transition(
                    source="DRAIN_T2",
                    target="WAIT_AFTER_DRAIN",
                    condition="Tank 2 level <= 0.05 m",
                    action="Close XV-103",
                ),
                Transition(
                    source="WAIT_AFTER_DRAIN",
                    target="FILL_T1",
                    condition="8 s wait completed",
                    action="Open XV-101",
                ),
                Transition(
                    source="SHUTDOWN",
                    target="IDLE",
                    condition="Both tanks <= low-level setpoints",
                    action="Close XV-102 and XV-103",
                ),
            ],
            assumptions=[
                Assumption(
                    description="CR-004 values are the current approved values.",
                    reason="They supersede the older URS Rev A values.",
                )
            ],
        )

    def extract(self) -> SystemModel:
        """
        Extract a SystemModel from the engineering specification.

        Real AI parsing will be implemented later.
        """

        specification = self.load_specification()

        ai_response = self.ask_ai(specification)

        print("\nAI RESPONSE:\n")
        print(ai_response)

        raise NotImplementedError(
            "Structured SystemModel parsing is not implemented yet."
        )