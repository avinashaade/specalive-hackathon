from app.system_schema import SystemModel


def _safe_name(name: str) -> str:
    """
    Convert an engineering identifier into a valid textual identifier.

    Example:
        TK-101 -> TK_101
        XV-101 -> XV_101
    """
    return name.replace("-", "_").replace(" ", "_")


def generate_sysml(system: SystemModel) -> str:
    """
    Generate a structured SysML v2 textual representation
    from the SystemModel.

    SystemModel remains the single source of truth.
    """

    lines = []

    lines.append(f"package {system.name} {{")
    lines.append("")

    # ---------------------------------------------------------
    # 1. Part definitions
    # ---------------------------------------------------------

    # Create only one definition for each component type.
    component_types = {}

    for component in system.components:
        if component.type not in component_types:
            component_types[component.type] = component

    for component_type, component in component_types.items():

        lines.append(f"    part def {component_type} {{")

        if component.description:
            lines.append(
                f"        doc /* {component.description} */;"
            )

        for name, value in component.attributes.items():

            attribute_name = _safe_name(name)

            if isinstance(value, str):
                lines.append(
                    f'        attribute {attribute_name} = "{value}";'
                )
            else:
                lines.append(
                    f"        attribute {attribute_name} = {value};"
                )

        lines.append("    }")
        lines.append("")

    # ---------------------------------------------------------
    # 2. Component instances
    # ---------------------------------------------------------

    lines.append("    // Component instances")

    for component in system.components:

        instance_name = _safe_name(component.name)

        lines.append(
            f"    part {instance_name} : {component.type};"
        )

    lines.append("")

    # ---------------------------------------------------------
    # 3. Connections
    # ---------------------------------------------------------

    if system.connections:

        lines.append("    // System connections")
        lines.append("")

        for connection in system.connections:

            source = _safe_name(connection.source)
            target = _safe_name(connection.target)

            lines.append(
                f"    connection connect_{source}_to_{target}"
                f" {{"
            )

            lines.append(
                f"        // {connection.source} -> {connection.target}"
            )

            if connection.description:
                lines.append(
                    f"        doc /* {connection.description} */;"
                )

            lines.append("    }")
            lines.append("")

    # ---------------------------------------------------------
    # 4. State machine
    # ---------------------------------------------------------

    if system.states:

        lines.append("    state def ControllerStateMachine {")
        lines.append("")

        for state in system.states:

            state_name = _safe_name(state.name)

            lines.append(
                f"        state {state_name};"
            )

        lines.append("")

        # State transitions
        for transition in system.transitions:

            source = _safe_name(transition.source)
            target = _safe_name(transition.target)

            lines.append(
                f"        // {transition.source} -> "
                f"{transition.target}"
            )

            if transition.trigger:
                lines.append(
                    f"        // Trigger: {transition.trigger}"
                )

            if transition.condition:
                lines.append(
                    f"        // Condition: {transition.condition}"
                )

            if transition.action:
                lines.append(
                    f"        // Action: {transition.action}"
                )

            lines.append("")

        lines.append("    }")
        lines.append("")

    # ---------------------------------------------------------
    # 5. Engineering assumptions
    # ---------------------------------------------------------

    if system.assumptions:

        lines.append("    // Engineering assumptions")
        lines.append("")

        for assumption in system.assumptions:

            lines.append(
                f"    // Assumption: {assumption.description}"
            )

            if assumption.reason:
                lines.append(
                    f"    // Reason: {assumption.reason}"
                )

        lines.append("")

    lines.append("}")

    return "\n".join(lines)