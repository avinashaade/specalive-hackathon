from app.system_schema import SystemModel, Component, Port


def test_system_model():
    tank = Component(
        name="Tank1",
        type="Tank",
        ports=[
            Port(
                name="inlet",
                type="fluid"
            ),
            Port(
                name="outlet",
                type="fluid"
            )
        ]
    )

    system = SystemModel(
        name="TwoTankSystem",
        description="Simple two tank control system",
        components=[tank]
    )

    assert system.name == "TwoTankSystem"
    assert len(system.components) == 1
    assert system.components[0].name == "Tank1"