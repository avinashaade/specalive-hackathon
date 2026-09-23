model L1_TwoTankController

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
  parameter Real waitAfterFill = 10.0;
  parameter Real waitAfterTransfer = 12.0;
  parameter Real waitAfterDrain = 8.0;
  parameter Real scanTime = 0.1;

  Real tank1Level(start = tank1InitialLevel, fixed = true);
  Real tank2Level(start = tank2InitialLevel, fixed = true);

  input Boolean START(start = false);
  input Boolean STOP(start = false);
  input Boolean SHUT(start = false);

  discrete Integer state(start = 0, fixed = true);
  discrete Real waitStartTime(start = 0.0, fixed = true);

equation
  der(tank1Level) = (if state == 1 then flowV1 else 0.0) - (if state == 3 or state == 8 then flowV2 else 0.0);
  der(tank2Level) = (if state == 3 or state == 8 then flowV2 else 0.0) - (if state == 5 or state == 8 then flowV3 else 0.0);

algorithm
  when sample(0.0, scanTime) then
    if SHUT then
      state := 8;
      waitStartTime := time;
    elseif STOP and state <> 0 and state <> 7 and state <> 8 then
      state := 7;
    elseif START and state == 0 then
      state := 1;
    elseif state == 1 and tank1Level >= tank1HighLevel then
      state := 2;
      waitStartTime := time;
    elseif state == 2 and (time - waitStartTime) >= waitAfterFill then
      state := 3;
    elseif state == 3 and tank1Level <= tank1LowLevel then
      state := 4;
      waitStartTime := time;
    elseif state == 4 and (time - waitStartTime) >= waitAfterTransfer then
      state := 5;
    elseif state == 5 and tank2Level <= tank2LowLevel then
      state := 6;
      waitStartTime := time;
    elseif state == 6 and (time - waitStartTime) >= waitAfterDrain then
      state := 1;
    end if;
  end when;

end L1_TwoTankController;