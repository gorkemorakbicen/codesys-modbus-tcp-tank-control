**CODESYS Modbus TCP Tank Control**

This project demonstrates Modbus TCP communication between a CODESYS PLC application and a Python-based virtual tank simulator.

CODESYS operates as the Modbus TCP client. It reads the simulated tank level and temperature, executes the control logic, and sends pump and valve commands.

Python operates as the Modbus TCP server. It simulates the tank process according to the commands received from the PLC.

**Main Features**

- Modbus TCP communication between CODESYS and Python
- IEC 61131-3 Structured Text programming
- State-machine-based control
- Automatic and manual operating modes
- Hysteresis-based tank-level control
- Temporary communication-loss detection
- Safe pump and valve outputs
- Recovery from communication failures
- Persistent tank level in the Python simulation
- CODESYS Visualization for operation and fault monitoring

**System Behavior**

In automatic mode, the PLC controls the tank between two level limits:

- Lower limit: 30 percent
- Upper limit: 70 percent

During `FILLING`, the pump remains active until the upper limit is reached.

During `DRAINING`, the valve remains active until the lower limit is reached.

The difference between the two limits creates hysteresis and prevents rapid switching between the pump and valve.

In manual mode, the operator can request the pump or valve directly.

If both manual commands are requested simultaneously, the system enters `MANUAL_CONFLICT`. Both outputs remain disabled in this condition.

**Communication Fault Behavior**

The PLC continuously checks the Modbus TCP connection.

When communication is lost:

- The pump and valve outputs are disabled immediately.
- The state changes to `COMM_LOSS`.
- The last valid tank level and temperature remain visible on the HMI.

If communication returns before seven seconds, the PLC resumes automatic operation through the `INIT` state.

If communication remains unavailable for seven seconds:

- A communication fault is latched.
- The state changes to `COMM_FAULT`.
- Restoring the connection alone does not clear the fault.
- The operator must press the fault-reset button after communication is restored.

This prevents the process from restarting automatically after a persistent communication failure.

**Recovery Behavior**

The PLC stores the last active automatic direction in `eLastAutoState`.

After a temporary communication loss or a fault reset:

- If the tank level is at or above the upper limit, the system selects `DRAINING`.
- If the tank level is at or below the lower limit, the system selects `FILLING`.
- If the level is between the limits, the system resumes the previous automatic direction.

This avoids always restarting with filling and preserves the hysteresis behavior after a communication interruption.

**Python Process Simulation**

The Python server simulates the physical tank behavior:

- The tank level increases while the pump is active.
- The tank level decreases while the valve is active.
- The level is limited between 0 and 100 percent.
- Temperature is currently fixed at 24 degrees Celsius.
- The simulation cycle is 0.5 seconds.

The last tank level is stored in a local `tank_state.txt` file.

When the Python server is restarted, it restores the last saved level instead of returning to the default 50 percent value.

The runtime state file is excluded from Git with `.gitignore`.

**Modbus Register Map**

- Input Register 0: Tank level, scaled by 10
- Input Register 1: Temperature, scaled by 10
- Holding Register 0: Pump command
- Holding Register 1: Valve command

For example, a tank-level register value of 620 represents 62.0 percent.

**Technologies**

- CODESYS Development System
- CODESYS Control Win V3 x64
- IEC 61131-3 Structured Text
- Python 3
- pyModbusTCP 0.3.0
- Modbus TCP

**Operating States**

`INIT` is a short transition state and is therefore not included in the screenshots.

**FILLING**

The pump fills the tank until the upper level limit is reached.

![Filling](docs/filling.png)

**DRAINING**

The valve drains the tank until the lower level limit is reached.

![Draining](docs/draining.png)

**MANUAL_IDLE**

Manual mode is active, but no manual command is requested.

![Manual Idle](docs/manual_idle.png)

**MANUAL_FILLING**

The pump is controlled manually.

![Manual Filling](docs/manual_filling.png)

**MANUAL_DRAINING**

The valve is controlled manually.

![Manual Draining](docs/manual_draining.png)

**MANUAL_CONFLICT**

Both manual commands are active, so both outputs remain disabled.

![Manual Conflict](docs/manual_conflict.png)

**COMM_LOSS**

Communication has been interrupted, but the seven-second fault delay has not yet expired.

![Communication Loss](docs/comm_loss.png)

**COMM_FAULT**

The communication loss has exceeded seven seconds and the fault has been latched.

![Communication Fault](docs/comm_fault.png)

**Repository Contents**

- `codesys/codesys-modbus-tcp-tank-control.projectarchive`: Complete CODESYS project
- `codesys/source/E_TankState.st`: State enumeration
- `codesys/source/PLC_PRG.st`: Main Structured Text program
- `python-server/virtual_slave.py`: Modbus TCP server and tank simulation
- `requirements.txt`: Required Python dependency
- `docs/`: HMI screenshots for the operating states

**Running the Project**

1. Restore the CODESYS project archive.
2. Start CODESYS Control Win.
3. Install the Python dependency with `python -m pip install -r requirements.txt`.
4. Start the Python server with `python python-server/virtual_slave.py`.
5. Log in to the CODESYS runtime.
6. Start the PLC application.

Connection settings:

- IP address: `127.0.0.1`
- Port: `502`
