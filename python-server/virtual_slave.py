"""
Virtual Modbus TCP server for the CODESYS tank control project.

Input Registers:
    Address 0: Tank level, scaled by 10
    Address 1: Temperature, scaled by 10

Holding Registers:
    Address 0: Pump command
    Address 1: Valve command
"""

from pathlib import Path
from time import sleep

from pyModbusTCP.server import DataBank, ModbusServer


HOST = "127.0.0.1"
PORT = 502

SIMULATION_CYCLE = 0.5
LEVEL_STEP_RAW = 20

DEFAULT_TANK_LEVEL_RAW = 500      # 50.0%
TEMPERATURE_RAW = 240             # 24.0°C

STATE_FILE = Path(__file__).with_name("tank_state.txt")


data_bank = DataBank()

# Restore the last saved tank level or start at the default value
try:
    tank_level_raw = int(
        STATE_FILE.read_text(encoding="utf-8").strip()
    )
except (FileNotFoundError, ValueError, OSError):
    tank_level_raw = DEFAULT_TANK_LEVEL_RAW

# Ensure that the restored value is within the physical range
tank_level_raw = max(0, min(1000, tank_level_raw))

# Store the initial value to avoid unnecessary file writes
last_saved_tank_level_raw = tank_level_raw


# Initialize virtual sensor registers
data_bank.set_input_registers(
    0,
    [tank_level_raw, TEMPERATURE_RAW]
)

# Initialize command registers written by CODESYS
data_bank.set_holding_registers(
    0,
    [0, 0]
)


server = ModbusServer(
    host=HOST,
    port=PORT,
    no_block=True,
    data_bank=data_bank
)


try:
    server.start()

    print(f"Modbus TCP server running at {HOST}:{PORT}")
    print(f"Restored tank level: {tank_level_raw / 10:.1f}%")
    print("Waiting for commands from CODESYS.")
    print("Press Ctrl+C to stop the simulation.\n")

    while True:
        # Read commands written by CODESYS to the Holding Registers
        commands = data_bank.get_holding_registers(0, 2) or [0, 0]

        pump_command = commands[0] == 1
        valve_command = commands[1] == 1

        # Simulate basic physical tank behavior
        if pump_command and not valve_command:
            tank_level_raw += LEVEL_STEP_RAW

        elif valve_command and not pump_command:
            tank_level_raw -= LEVEL_STEP_RAW

        # Limit the simulated tank level to the range of 0% to 100%
        tank_level_raw = max(0, min(1000, tank_level_raw))

        # Save the tank level only when it changes
        if tank_level_raw != last_saved_tank_level_raw:
            STATE_FILE.write_text(
                str(tank_level_raw),
                encoding="utf-8"
            )
            last_saved_tank_level_raw = tank_level_raw

        # Update the Input Registers with the simulated sensor values
        data_bank.set_input_registers(
            0,
            [tank_level_raw, TEMPERATURE_RAW]
        )

        print(
            f"\rTank: {tank_level_raw / 10:5.1f}% | "
            f"Temperature: {TEMPERATURE_RAW / 10:4.1f} C | "
            f"Pump: {int(pump_command)} | "
            f"Valve: {int(valve_command)}",
            end="",
            flush=True
        )

        sleep(SIMULATION_CYCLE)

except KeyboardInterrupt:
    print("\nSimulation stopped by the user.")

finally:
    server.stop()
    print("Modbus TCP server stopped.")