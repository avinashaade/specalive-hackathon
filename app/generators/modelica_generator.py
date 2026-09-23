from app.system_schema import SystemModel


def generate_modelica(system: SystemModel) -> str:
    lines = []

    lines.append(f"model {system.name}")
    lines.append("")

    # ---------------------------------------------------------
    # Parameters
    # ---------------------------------------------------------
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

    lines.append("  parameter Real scanTime = 0.1;")

    lines.append("")

    # ---------------------------------------------------------
    # Tank levels
    # ---------------------------------------------------------
    lines.append(
        "  Real tank1Level(start = tank1InitialLevel, fixed = true);"
    )
    lines.append(
        "  Real tank2Level(start = tank2InitialLevel, fixed = true);"
    )

    lines.append("")

    # ---------------------------------------------------------
    # External commands
    # ---------------------------------------------------------
    lines.append("  input Boolean START(start = false);")
    lines.append("  input Boolean STOP(start = false);")
    lines.append("  input Boolean SHUT(start = false);")

    lines.append("")

    # ---------------------------------------------------------
    # Controller state
    #
    # 0 = IDLE
    # 1 = FILL_T1
    # 2 = WAIT_AFTER_FILL
    # 3 = TRANSFER_T1_T2
    # 4 = WAIT_AFTER_TRANSFER
    # 5 = DRAIN_T2
    # 6 = WAIT_AFTER_DRAIN
    # 7 = PAUSED
    # 8 = SHUTDOWN
    # ---------------------------------------------------------
    lines.append("  discrete Integer state(start = 0, fixed = true);")
    lines.append("  discrete Integer pausedState(start = 0, fixed = true);")

    # Remaining time when STOP interrupts a WAIT state.
    lines.append(
        "  discrete Real pausedRemainingWait(start = 0.0, fixed = true);"
    )

    # Time at which the current WAIT state was entered/resumed.
    lines.append(
        "  discrete Real waitStartTime(start = 0.0, fixed = true);"
    )

    lines.append("")

    # ---------------------------------------------------------
    # Tank physics
    #
    # State directly determines the active flow path.
    # ---------------------------------------------------------
    lines.append("equation")

    lines.append(
        "  der(tank1Level) = "
        "(if state == 1 then flowV1 else 0.0) "
        "- (if state == 3 or state == 8 then flowV2 else 0.0);"
    )

    lines.append(
        "  der(tank2Level) = "
        "(if state == 3 or state == 8 then flowV2 else 0.0) "
        "- (if state == 5 or state == 8 then flowV3 else 0.0);"
    )

    lines.append("")

    # ---------------------------------------------------------
    # Controller state machine
    # ---------------------------------------------------------
    lines.append("algorithm")
    lines.append("  when sample(0.0, scanTime) then")

    # ---------------------------------------------------------
    # SHUT has highest priority
    # ---------------------------------------------------------
    lines.append("    if SHUT then")
    lines.append("      state := 8;")
    lines.append("      waitStartTime := time;")
    lines.append("      pausedRemainingWait := 0.0;")

    # ---------------------------------------------------------
    # STOP has second priority
    #
    # If STOP interrupts a WAIT state, preserve the remaining
    # wait time so START can resume from the same point.
    # ---------------------------------------------------------
    lines.append(
        "    elseif STOP and state <> 0 and state <> 7 and state <> 8 then"
    )
    lines.append("      pausedState := state;")

    lines.append(
        "      if state == 2 then"
    )
    lines.append(
        "        pausedRemainingWait := max(0.0, "
        "waitAfterFill - (time - waitStartTime));"
    )
    lines.append(
        "      elseif state == 4 then"
    )
    lines.append(
        "        pausedRemainingWait := max(0.0, "
        "waitAfterTransfer - (time - waitStartTime));"
    )
    lines.append(
        "      elseif state == 6 then"
    )
    lines.append(
        "        pausedRemainingWait := max(0.0, "
        "waitAfterDrain - (time - waitStartTime));"
    )
    lines.append(
        "      else"
    )
    lines.append(
        "        pausedRemainingWait := 0.0;"
    )
    lines.append(
        "      end if;"
    )

    lines.append("      state := 7;")

    # ---------------------------------------------------------
    # START
    #
    # If paused, resume the state that was active before STOP.
    # For WAIT states, reconstruct waitStartTime so that only
    # the remaining wait duration is required.
    # Otherwise START from IDLE begins the normal sequence.
    # ---------------------------------------------------------
    lines.append(
        "    elseif START and state == 7 then"
    )
    lines.append("      state := pausedState;")

    lines.append(
        "      if pausedState == 2 then"
    )
    lines.append(
        "        waitStartTime := time + pausedRemainingWait - waitAfterFill;"
    )
    lines.append(
        "      elseif pausedState == 4 then"
    )
    lines.append(
        "        waitStartTime := time + pausedRemainingWait - waitAfterTransfer;"
    )
    lines.append(
        "      elseif pausedState == 6 then"
    )
    lines.append(
        "        waitStartTime := time + pausedRemainingWait - waitAfterDrain;"
    )
    lines.append(
        "      else"
    )
    lines.append(
        "        waitStartTime := time;"
    )
    lines.append(
        "      end if;"
    )

    lines.append(
        "    elseif START and state == 0 then"
    )
    lines.append("      state := 1;")

    # ---------------------------------------------------------
    # FILL_T1
    # ---------------------------------------------------------
    lines.append(
        "    elseif state == 1 and tank1Level >= tank1HighLevel then"
    )
    lines.append("      state := 2;")
    lines.append("      waitStartTime := time;")

    # ---------------------------------------------------------
    # WAIT_AFTER_FILL
    # ---------------------------------------------------------
    lines.append(
        "    elseif state == 2 and "
        "(time - waitStartTime) >= waitAfterFill then"
    )
    lines.append("      state := 3;")
    lines.append("      pausedRemainingWait := 0.0;")

    # ---------------------------------------------------------
    # TRANSFER_T1_T2
    # ---------------------------------------------------------
    lines.append(
        "    elseif state == 3 and tank1Level <= tank1LowLevel then"
    )
    lines.append("      state := 4;")
    lines.append("      waitStartTime := time;")

    # ---------------------------------------------------------
    # WAIT_AFTER_TRANSFER
    # ---------------------------------------------------------
    lines.append(
        "    elseif state == 4 and "
        "(time - waitStartTime) >= waitAfterTransfer then"
    )
    lines.append("      state := 5;")
    lines.append("      pausedRemainingWait := 0.0;")

    # ---------------------------------------------------------
    # DRAIN_T2
    # ---------------------------------------------------------
    lines.append(
        "    elseif state == 5 and tank2Level <= tank2LowLevel then"
    )
    lines.append("      state := 6;")
    lines.append("      waitStartTime := time;")

    # ---------------------------------------------------------
    # WAIT_AFTER_DRAIN
    # ---------------------------------------------------------
    lines.append(
        "    elseif state == 6 and "
        "(time - waitStartTime) >= waitAfterDrain then"
    )
    lines.append("      state := 1;")
    lines.append("      pausedRemainingWait := 0.0;")

    lines.append("    end if;")
    lines.append("  end when;")

    lines.append("")
    lines.append(f"end {system.name};")

    return "\n".join(lines)