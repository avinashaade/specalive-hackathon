from app.system_schema import SystemModel


def _safe_name(name: str) -> str:
    """Convert engineering names into valid Modelica identifiers."""
    return name.replace("-", "_").replace(" ", "_")


def generate_modelica(system: SystemModel) -> str:
    """
    Generate a basic executable Modelica model from SystemModel.

    The SystemModel remains the single source of truth.
    """

    model_name = _safe_name(system.name)

    lines = []

    lines.append(f"model {model_name}")
    lines.append("")

    lines.append("  // ========================================")
    lines.append("  // Two-Tank System Parameters")
    lines.append("  // ========================================")

    lines.append("  parameter Real tank1Area = 1.2;")
    lines.append("  parameter Real tank2Area = 1.4;")

    lines.append("  parameter Real tank1InitialLevel = 0.05;")
    lines.append("  parameter Real tank2InitialLevel = 0.05;")

    lines.append("  parameter Real tank1HighLevel = 0.80;")
    lines.append("  parameter Real tank1LowLevel = 0.05;")
    lines.append("  parameter Real tank2LowLevel = 0.05;")

    lines.append("  parameter Real flowV1 = 0.006;")
    lines.append("  parameter Real flowV2 = 0.0045;")
    lines.append("  parameter Real flowV3 = 0.005;")

    lines.append("")

    lines.append("  // ========================================")
    lines.append("  // Tank levels")
    lines.append("  // ========================================")

    lines.append(
        "  Real tank1Level(start=tank1InitialLevel, fixed=true);"
    )

    lines.append(
        "  Real tank2Level(start=tank2InitialLevel, fixed=true);"
    )

    lines.append("")

    lines.append("  // ========================================")
    lines.append("  // Valve commands")
    lines.append("  // ========================================")

    lines.append("  Boolean v1Open;")
    lines.append("  Boolean v2Open;")
    lines.append("  Boolean v3Open;")

    lines.append("")

    lines.append("  // ========================================")
    lines.append("  // Controller state")
    lines.append("  // ========================================")

    lines.append(
        "  discrete Integer state(start=0, fixed=true);"
    )

    lines.append("")

    lines.append("  // State mapping:")
    lines.append("  // 0 = IDLE")
    lines.append("  // 1 = FILL_T1")
    lines.append("  // 2 = WAIT_AFTER_FILL")
    lines.append("  // 3 = TRANSFER_T1_T2")
    lines.append("  // 4 = WAIT_AFTER_TRANSFER")
    lines.append("  // 5 = DRAIN_T2")
    lines.append("  // 6 = WAIT_AFTER_DRAIN")
    lines.append("  // 7 = PAUSED")
    lines.append("  // 8 = SHUTDOWN")

    lines.append("")

    # Modelica equations start here.
    lines.append("equation")
    lines.append("")

    lines.append("  // ========================================")
    lines.append("  // Valve control")
    lines.append("  // ========================================")

    lines.append("  v1Open = state == 1;")
    lines.append("  v2Open = state == 3 or state == 8;")
    lines.append("  v3Open = state == 5 or state == 8;")

    lines.append("")

    lines.append("  // ========================================")
    lines.append("  // Tank dynamics")
    lines.append("  // ========================================")

    lines.append(
        "  der(tank1Level) = "
        "(if v1Open then flowV1 else 0.0)"
        " - (if v2Open then flowV2 else 0.0);"
    )

    lines.append(
        "  der(tank2Level) = "
        "(if v2Open then flowV2 else 0.0)"
        " - (if v3Open then flowV3 else 0.0);"
    )

    lines.append("")

    lines.append("  // ========================================")
    lines.append("  // State transitions")
    lines.append("  // ========================================")

    lines.append("algorithm")

    lines.append("  when initial() then")
    lines.append("    state := 1;")
    lines.append("  end when;")

    lines.append("")

    lines.append(
        "  when state == 1 and tank1Level >= tank1HighLevel then"
    )
    lines.append("    state := 2;")
    lines.append("  end when;")

    lines.append("")

    lines.append("  when state == 2 then")
    lines.append("    state := 3;")
    lines.append("  end when;")

    lines.append("")

    lines.append(
        "  when state == 3 and tank1Level <= tank1LowLevel then"
    )
    lines.append("    state := 4;")
    lines.append("  end when;")

    lines.append("")

    lines.append("  when state == 4 then")
    lines.append("    state := 5;")
    lines.append("  end when;")

    lines.append("")

    lines.append(
        "  when state == 5 and tank2Level <= tank2LowLevel then"
    )
    lines.append("    state := 6;")
    lines.append("  end when;")

    lines.append("")

    lines.append("  when state == 6 then")
    lines.append("    state := 1;")
    lines.append("  end when;")

    lines.append("")

    lines.append("end " + model_name + ";")

    return "\n".join(lines)