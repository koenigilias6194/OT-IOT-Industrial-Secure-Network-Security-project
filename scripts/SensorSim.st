PROGRAM SensorSim
VAR
Temperature AT %MW0 : INT := 25;
Pressure AT %MW1 : INT := 10;
Motor AT %QX0.0 : BOOL := TRUE;
END_VAR
IF Temperature < 100 THEN
Temperature := Temperature + 1;
ELSE
Temperature := 0;
END_IF;
IF Pressure < 50 THEN
Pressure := Pressure + 1;
ELSE
Pressure := 0;
END_IF;
END_PROGRAM
CONFIGURATION Config0
RESOURCE Res0 ON PLC
TASK TaskMain(INTERVAL := T#20ms,PRIORITY := 0);
PROGRAM Inst0 WITH TaskMain: SensorSim;
END_RESOURCE
END_CONFIGURATION
