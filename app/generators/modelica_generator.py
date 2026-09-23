from app.system_schema import SystemModel


def _safe_name(name: str) -> str:
    """Convert engineering names into valid Modelica identifiers."""
    return name.replace("-", "_").replace(" ", "_")


def generate_modelica(system: SystemModel) -> str:
    """
    Generate a Modelica representation from the SystemModel.

    The SystemModel remains the single source of truth.
    """

    model_name = _safe_name(system.name)

    lines = []

    lines.append(f"model {model_name}")
    lines.append("")

    # ========================================
    # Parameters
    # ========================================

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

    lines.append("  parameter Real waitAfterFill = 10.0;")
    lines.append("  parameter Real waitAfterTransfer = 12.0;")
    lines.append("  parameter Real waitAfterDrain = 8.0;")

    lines.append("")

    # ========================================
    # Tank levels
    # ========================================

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

    # ========================================
    # Controller command inputs
    # ========================================

    lines.append("  // ========================================")
    lines.append("  // Controller command inputs")
    lines.append("  // ========================================")

    lines.append("  input Boolean START(start=false);")
    lines.append("  input Boolean STOP(start=false);")
    lines.append("  input Boolean SHUT(start=false);")

    lines.append("")

    # ========================================
    # Valve commands
    # ========================================

    lines.append("  // ========================================")
    lines.append("  // Valve commands")
    lines.append("  // ========================================")

    lines.append("  Boolean v1Open;")
    lines.append("  Boolean v2Open;")
    lines.append("  Boolean v3Open;")

    lines.append("")

    # ========================================
    # Controller state
    # ========================================

    lines.append("  // ========================================")
    lines.append("  // Controller state")
    lines.append("  // ========================================")

    lines.append("  discrete Integer state(start=0, fixed=true);")

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

    # ========================================
    # Continuous equations
    # ========================================

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

    # ========================================
    # State machine
    # ========================================

    lines.append("algorithm")
    lines.append("")

    lines.append("  // Command priority: SHUT > STOP > START")

    lines.append("  when initial() then")
    lines.append("    state := 0;")
    lines.append("  end when;")

    # Check controller conditions periodically.
    lines.append("  when sample(0, 0.1) then")

    lines.append("")

    # SHUT has highest priority.
    lines.append("    if SHUT then")
    lines.append("      state := 8;")

    # STOP has second priority.
    lines.append(
        "    elseif STOP and state <> 0 and state <> 8 then"
    )
    lines.append("      state := 7;")

    # START from IDLE.
    lines.append(
        "    elseif START and state == 0 then"
    )
    lines.append("      state := 1;")

    # Normal sequence.
    lines.append(
        "    elseif state == 1 and tank1Level >= tank1HighLevel then"
    )
    lines.append("      state := 2;")

    lines.append(
        "    elseif state == 2 then"
    )
    lines.append(
        "      state := 3;"
    )

    lines.append(
        "    elseif state == 3 and tank1Level <= tank1LowLevel then"
    )
    lines.append("      state := 4;")

    lines.append(
        "    elseif state == 4 then"
    )
    lines.append("      state := 5;")

    lines.append(
        "    elseif state == 5 and tank2Level <= tank2LowLevel then"
    )
    lines.append("      state := 6;")

    lines.append(
        "    elseif state == 6 then"
    )
    lines.append("      state := 1;")

    lines.append("    end if;")
    lines.append("")

    lines.append("  end when;")
    lines.append("")

    lines.append(f"end {model_name};")

    return "\n".join(lines)