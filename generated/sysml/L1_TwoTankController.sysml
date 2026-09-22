package L1_TwoTankController {

    part def Tank {
        doc /* Tank 1 */;
        attribute area = 1.2;
        attribute height = 1.0;
        attribute initial_level = 0.05;
        attribute high_level = 0.8;
        attribute low_level = 0.05;
    }

    part def OnOffValve {
        doc /* Feed valve */;
        attribute nominal_flow = 0.006;
        attribute fail_position = "Closed";
    }

    // Component instances
    part TK_101 : Tank;
    part TK_102 : Tank;
    part XV_101 : OnOffValve;
    part XV_102 : OnOffValve;
    part XV_103 : OnOffValve;

    // System connections

    connection connect_XV_101.outlet_to_TK_101.inlet {
        // XV-101.outlet -> TK-101.inlet
    }

    connection connect_TK_101.outlet_to_XV_102.inlet {
        // TK-101.outlet -> XV-102.inlet
    }

    connection connect_XV_102.outlet_to_TK_102.inlet {
        // XV-102.outlet -> TK-102.inlet
    }

    connection connect_TK_102.outlet_to_XV_103.inlet {
        // TK-102.outlet -> XV-103.inlet
    }

    state def ControllerStateMachine {

        state IDLE;
        state FILL_T1;
        state WAIT_AFTER_FILL;
        state TRANSFER_T1_T2;
        state WAIT_AFTER_TRANSFER;
        state DRAIN_T2;
        state WAIT_AFTER_DRAIN;
        state PAUSED;
        state SHUTDOWN;

        // IDLE -> FILL_T1
        // Trigger: START

        // FILL_T1 -> WAIT_AFTER_FILL
        // Condition: Tank 1 level >= 0.80 m
        // Action: Close XV-101

        // WAIT_AFTER_FILL -> TRANSFER_T1_T2
        // Condition: 10 s wait completed
        // Action: Open XV-102

        // TRANSFER_T1_T2 -> WAIT_AFTER_TRANSFER
        // Condition: Tank 1 level <= 0.05 m
        // Action: Close XV-102

        // WAIT_AFTER_TRANSFER -> DRAIN_T2
        // Condition: 12 s wait completed
        // Action: Open XV-103

        // DRAIN_T2 -> WAIT_AFTER_DRAIN
        // Condition: Tank 2 level <= 0.05 m
        // Action: Close XV-103

        // WAIT_AFTER_DRAIN -> FILL_T1
        // Condition: 8 s wait completed
        // Action: Open XV-101

        // SHUTDOWN -> IDLE
        // Condition: Both tanks <= low-level setpoints
        // Action: Close XV-102 and XV-103

    }

    // Engineering assumptions

    // Assumption: CR-004 values are the current approved values.
    // Reason: They supersede the older URS Rev A values.

}