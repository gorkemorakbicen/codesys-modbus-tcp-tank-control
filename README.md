**CODESYS Modbus TCP Tank Control**

A virtual tank-control project demonstrating Modbus TCP communication between a CODESYS PLC application and a Python-based process simulator.

CODESYS operates as the Modbus TCP client and controls the simulated tank through pump and valve commands. Python operates as the Modbus TCP server and updates the virtual tank level according to these commands.

**Main Features**

- Modbus TCP communication between CODESYS and Python
- Structured Text programming
- State-machine-based automatic control
- Automatic and manual operating modes
- Communication-loss detection
- Latched fault handling and manual reset
- Safe pump and valve outputs
- Virtual tank-level simulation

**Control Logic**

The PLC uses four states:

- INIT
- FILLING
- DRAINING
- COMM_FAULT

In automatic mode, the pump fills the tank until the level reaches 68 percent. The valve then drains the tank until the level falls to 32 percent.

In manual mode, the pump and valve can be controlled independently. If both commands are requested simultaneously, both outputs remain disabled.

If the Modbus connection remains unavailable for seven seconds, the PLC enters COMM_FAULT and disables the outputs. The fault can be cleared only after communication is restored and the operator sends a reset request.

**Modbus Data**

- Input Register 0: Tank level
- Input Register 1: Temperature
- Holding Register 0: Pump command
- Holding Register 1: Valve command

Tank level and temperature values are scaled by 10.

**Technologies**

- CODESYS Control Win V3 x64
- IEC 61131-3 Structured Text
- Python 3
- pyModbusTCP 0.3.0
- Modbus TCP

**Repository Contents**

- CODESYS project archive
- Readable Structured Text source files
- Python virtual Modbus server
- Python dependency file
- Project screenshots and documentation

**Running the Project**

1. Restore the CODESYS project archive.
2. Start CODESYS Control Win.
3. Start the Python server.
4. Log in to the PLC runtime and run the application.

Connection settings:

- IP address: 127.0.0.1
- Port: 502

This repository is an educational software simulation and is not intended for direct use in a real industrial process.