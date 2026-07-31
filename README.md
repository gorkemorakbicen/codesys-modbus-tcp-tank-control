# \# CODESYS Modbus TCP Tank Control

# 

# A virtual industrial control project demonstrating Modbus TCP communication between a CODESYS PLC application and a Python-based process simulator.

# 

# The CODESYS application operates as a Modbus TCP client and controls a simulated tank through pump and valve commands. The Python application operates as a virtual Modbus TCP server and simulates tank-level changes based on the commands received from the PLC.

# 

# \## Project Overview

# 

# The project demonstrates:

# 

# \- Modbus TCP client-server communication

# \- Input Register and Holding Register access

# \- Structured Text programming according to IEC 61131-3

# \- State-machine-based automatic control

# \- Manual and automatic operating modes

# \- Communication-loss detection

# \- Latched fault handling and manual reset

# \- Safe output initialization during every PLC cycle

# \- Basic physical process simulation in Python

# 

# \## System Architecture

# 

# ```text

# ┌───────────────────────────────┐

# │ CODESYS Control Win V3 x64    │

# │                               │

# │ Modbus TCP Client             │

# │ PLC state machine             │

# │ Pump and valve control        │

# │ Communication fault handling  │

# └───────────────┬───────────────┘

# &#x20;               │

# &#x20;               │ Modbus TCP

# &#x20;               │ 127.0.0.1:502

# &#x20;               │

# ┌───────────────▼───────────────┐

# │ Python Virtual Server         │

# │                               │

# │ Simulated tank level          │

# │ Simulated temperature         │

# │ Pump and valve commands       │

# └───────────────────────────────┘

# ```

# 

# \## Modbus Register Map

# 

# | Register type | Address | Data | Scaling |

# |---|---:|---|---|

# | Input Register | 0 | Tank level | Raw value ÷ 10 = % |

# | Input Register | 1 | Temperature | Raw value ÷ 10 = °C |

# | Holding Register | 0 | Pump command | `0 = OFF`, `1 = ON` |

# | Holding Register | 1 | Valve command | `0 = OFF`, `1 = ON` |

# 

# Example:

# 

# ```text

# Tank level raw value: 500

# Engineering value: 500 / 10 = 50.0%

# ```

# 

# \## PLC Control Logic

# 

# The PLC application uses the following states:

# 

# | State | Description |

# |---|---|

# | `INIT` | Determines whether filling or draining should begin |

# | `FILLING` | Activates the pump until the upper level limit is reached |

# | `DRAINING` | Activates the valve until the lower level limit is reached |

# | `COMM\_FAULT` | Forces the outputs into a safe state after communication failure |

# 

# The automatic level-control limits are:

# 

# ```text

# Lower level limit: 32.0%

# Upper level limit: 68.0%

# ```

# 

# The difference between the switching limits prevents rapid switching between the pump and valve.

# 

# \## Communication Fault Handling

# 

# The PLC continuously checks whether a Modbus TCP server is connected.

# 

# If communication remains unavailable for seven seconds:

# 

# 1\. A communication fault is latched.

# 2\. The state machine enters `COMM\_FAULT`.

# 3\. Pump and valve commands remain disabled.

# 4\. Restoring the connection alone does not clear the fault.

# 5\. The operator must issue a reset request after communication is restored.

# 6\. The PLC then performs a controlled restart from the `INIT` state.

# 

# \## Operating Modes

# 

# \### Automatic mode

# 

# The PLC automatically switches between filling and draining according to the tank level.

# 

# \### Manual mode

# 

# The operator can request the pump or valve manually.

# 

# A conflict condition is generated when both manual commands are requested simultaneously. In that case, neither output is activated.

# 

# \## Python Process Simulation

# 

# The Python server:

# 

# \- Initializes the tank level at 50.0%

# \- Initializes the temperature at 24.0°C

# \- Reads pump and valve commands from Holding Registers

# \- Increases the tank level while the pump is active

# \- Decreases the tank level while the valve is active

# \- Restricts the simulated tank level to the range of 0–100%

# \- Updates the Input Registers every 0.5 seconds

# 

# \## Repository Structure

# 

# ```text

# codesys-modbus-tcp-tank-control/

# ├── codesys/

# │   ├── codesys-modbus-tcp-tank-control.projectarchive

# │   └── source/

# │       ├── E\_TankState.st

# │       └── PLC\_PRG.st

# ├── python-server/

# │   └── virtual\_slave.py

# ├── docs/

# ├── requirements.txt

# └── README.md

# ```

# 

# \## Requirements

# 

# \- CODESYS Development System

# \- CODESYS Control Win V3 x64

# \- Python 3

# \- `pyModbusTCP==0.3.0`

# 

# Install the Python dependency with:

# 

# ```bash

# python -m pip install -r requirements.txt

# ```

# 

# \## Running the Project

# 

# 1\. Restore the CODESYS project archive.

# 2\. Start CODESYS Control Win.

# 3\. Verify that the Modbus TCP client is configured for:

# 

# ```text

# IP address: 127.0.0.1

# Port: 502

# ```

# 

# 4\. Start the Python virtual server:

# 

# ```bash

# python python-server/virtual\_slave.py

# ```

# 

# 5\. Log in to the CODESYS runtime.

# 6\. Start the PLC application.

# 7\. Observe the tank level, pump command, valve command and communication status.

# 

# \## Safety Design

# 

# The pump and valve commands are reset to `FALSE` at the beginning of every PLC cycle.

# 

# They are activated only when the current operating state explicitly permits them. This prevents an output from unintentionally remaining active after a state transition or communication failure.

# 

# > This repository is an educational simulation project. It is not intended for direct use in a real industrial process without additional hardware safety, validation and risk assessment.

# 

# \## Possible Future Improvements

# 

# \- HMI screenshots and operating instructions

# \- Automated test cases

# \- Adjustable simulation speed

# \- Dynamic temperature simulation

# \- Alarm history

# \- Data logging

# \- Additional sensor-failure scenarios

# \- Docker-based Python server deployment

