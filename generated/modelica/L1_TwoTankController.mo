model L1_TwoTankController

  // ========================================
  // Two-Tank System Parameters
  // ========================================
  parameter Real tank1Area = 1.2;
  parameter Real tank2Area = 1.4;
  parameter Real tank1InitialLevel = 0.05;
  parameter Real tank2InitialLevel = 0.05;
  parameter Real tank1HighLevel = 0.80;
  parameter Real tank1LowLevel = 0.05;
  parameter Real tank2LowLevel = 0.05;
  parameter Real flowV1 = 0.006;
  parameter Real flowV2 = 0.0045;
  parameter Real flowV3 = 0.005;

  // ========================================
  // Tank levels
  // ========================================
  Real tank1Level(start=tank1InitialLevel, fixed=true);
  Real tank2Level(start=tank2InitialLevel, fixed=true);

  // ========================================
  // Valve commands
  // ========================================
  Boolean v1Open;
  Boolean v2Open;
  Boolean v3Open;

  // ========================================
  // Controller state
  // ========================================
  discrete Integer state(start=0, fixed=true);

  // State mapping:
  // 0 = IDLE
  // 1 = FILL_T1
  // 2 = WAIT_AFTER_FILL
  // 3 = TRANSFER_T1_T2
  // 4 = WAIT_AFTER_TRANSFER
  // 5 = DRAIN_T2
  // 6 = WAIT_AFTER_DRAIN
  // 7 = PAUSED
  // 8 = SHUTDOWN

equation

  // ========================================
  // Valve control
  // ========================================
  v1Open = state == 1;
  v2Open = state == 3 or state == 8;
  v3Open = state == 5 or state == 8;

  // ========================================
  // Tank dynamics
  // ========================================
  der(tank1Level) = (if v1Open then flowV1 else 0.0) - (if v2Open then flowV2 else 0.0);
  der(tank2Level) = (if v2Open then flowV2 else 0.0) - (if v3Open then flowV3 else 0.0);

  // ========================================
  // State transitions
  // ========================================
algorithm
  when initial() then
    state := 1;
  end when;

  when state == 1 and tank1Level >= tank1HighLevel then
    state := 2;
  end when;

  when state == 2 then
    state := 3;
  end when;

  when state == 3 and tank1Level <= tank1LowLevel then
    state := 4;
  end when;

  when state == 4 then
    state := 5;
  end when;

  when state == 5 and tank2Level <= tank2LowLevel then
    state := 6;
  end when;

  when state == 6 then
    state := 1;
  end when;

end L1_TwoTankController;