PROGRAM PLC_PRG
VAR
    // Modbus'tan okunan ham değerler
    wTankLevelRaw : WORD;
    wTemperatureRaw : WORD;

    // CODESYS'te ölçeklendirilmiş değerler
    rTankLevelPercent : REAL;
    rTemperatureC : REAL;

    // PLC'nin ürettiği kontrol komutları
    xPumpCommand : BOOL;
    xValveCommand : BOOL;

    // Modbus'a yazılacak 16-bit register değerleri
    wPumpCommandRaw : WORD;
    wValveCommandRaw : WORD;
	
	eTankState : E_TankState := E_TankState.INIT;

    rLowLevelLimit : REAL := 32.0;
    rHighLevelLimit : REAL := 68.0;
	
	// Çalışma modu
	xAutoMode : BOOL := TRUE;

	// Manuel mod istekleri
	xManualPumpRequest : BOOL;
	xManualValveRequest : BOOL;
	
	// Manuel komut çakışma bilgisi
	xManualConflict : BOOL;
	
	xModbusConnected : BOOL;
	xCommunicationFault : BOOL;
	xFaultResetRequest : BOOL;
	
	fbCommLossDelay : TON;
	fbFaultResetEdge : R_TRIG;

END_VAR