model L1_StateTest

  discrete Integer state(start=0, fixed=true);

algorithm

  when initial() then
    state := 0;
  end when;

  when sample(0, 0.1) then

    if state == 0 then
      state := 1;

    elseif state == 1 then
      state := 2;

    elseif state == 2 then
      state := 3;

    elseif state == 3 then
      state := 4;

    elseif state == 4 then
      state := 5;

    elseif state == 5 then
      state := 6;

    elseif state == 6 then
      state := 1;
    end if;

  end when;

end L1_StateTest;
