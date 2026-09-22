from app.system_schema import (
    SystemModel,
    Component,
    Port,
    Connection,
    State,
    Transition,
    Assumption,
)


def test_l1_two_tank_model():

    tank1 = Component(
        name="TK-101",
        type="Tank",
        ports=[
            Port(name="inlet", type="fluid"),
            Port(name="outlet", type="fluid"),
        ],
        attributes={
            "area": 1.2,
            "height": 1.0,
            "initial_level": 0.05,
        },
    )

    tank2 = Component(
        name="TK-102",
        type="Tank",
        ports=[
            Port(name="inlet", type="fluid"),
            Port(name="outlet", type="fluid"),
        ],
        attributes={
            "area": 1.4,
            "height": 1.0,
            "initial_level": 0.05,
        },
    )

    valve1 = Component(
        name="XV-101",
        type="OnOffValve",
        attributes={
            "nominal_flow": 0.006,
            "fail_position": "Closed",
        },
    )

    valve2 = Component(
        name="XV-102",
        type="OnOffValve",
        attributes={
            "nominal_flow": 0.0045,
            "fail_position": "Closed",
        },
    )

    valve3 = Component(
        name="XV-103",
        type="OnOffValve",
        attributes={
            "nominal_flow": 0.005,
            "fail_position": "Closed",
        },
    )

    fill_state = State(
        name="FILL_T1",
        description="Fill Tank 1",
    )

    transfer_state = State(
        name="TRANSFER_T1_T2",
        description="Transfer liquid from Tank 1 to Tank 2",
    )

    drain_state = State(
        name="DRAIN_T2",
        description="Drain Tank 2",
    )

    transition = Transition(
        source="FILL_T1",
        target="TRANSFER_T1_T2",
        trigger="Tank 1 high level reached",
        action="Close XV-101",
    )

    system = SystemModel(
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
            fill_state,
            transfer_state,
            drain_state,
        ],
        transitions=[
            transition,
        ],
        assumptions=[
            Assumption(
                description="CR-004 values are treated as the current approved parameters.",
                reason="They supersede the older URS Rev A values.",
            )
        ],
    )

    assert system.name == "L1_TwoTankController"
    assert len(system.components) == 5
    assert len(system.connections) == 4
    assert len(system.states) == 3
    assert len(system.transitions) == 1
    assert len(system.assumptions) == 1

    assert system.components[0].name == "TK-101"
    assert system.components[0].attributes["area"] == 1.2

    assert system.transitions[0].source == "FILL_T1"
    assert system.transitions[0].target == "TRANSFER_T1_T2"


from app.agents.requirement_agent import RequirementExtractionAgent


def test_requirement_agent_reads_specification():

    agent = RequirementExtractionAgent(
        "data/l1_two_tank/input/specification.txt"
    )

    specification = agent.load_specification()

    assert len(specification) > 0
    assert "SPECALIVE L1" in specification
    assert "TK-101" in specification
    assert "TK-102" in specification
    assert "CR-004" in specification