"""
Virtual Modbus TCP server for the CODESYS tank control project.

Input Registers:
    Address 0: Tank level, scaled by 10
    Address 1: Temperature, scaled by 10

Holding Registers:
    Address 0: Pump command
    Address 1: Valve command
"""

from time import sleep

from pyModbusTCP.server import DataBank, ModbusServer


HOST = "127.0.0.1"
PORT = 502

SIMULATION_CYCLE = 0.5
LEVEL_STEP_RAW = 20

data_bank = DataBank()

# Initial process values
tank_level_raw = 500       # 50.0%
temperature_raw = 240      # 24.0°C

# Initialize virtual sensor registers
data_bank.set_input_registers(
    0,
    [tank_level_raw, temperature_raw]
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
    print("Waiting for commands from CODESYS.")
    print("Press Ctrl+C to stop the simulation.\n")

    while True:
        # Read commands written by CODESYS to the Holding Registers
        commands = data_bank.get_holding_registers(0, 2)

        pump_command = commands[0] == 1
        valve_command = commands[1] == 1

        # Simulate basic physical tank behavior
        if pump_command and not valve_command:
            tank_level_raw += LEVEL_STEP_RAW

        elif valve_command and not pump_command:
            tank_level_raw -= LEVEL_STEP_RAW

        # Limit the virtual tank level to the physical range of 0% to 100%
        tank_level_raw = max(0, min(1000, tank_level_raw))

        # Update the Input Registers with the simulated sensor values
        data_bank.set_input_registers(
            0,
            [tank_level_raw, temperature_raw]
        )

        print(
            f"\rTank: {tank_level_raw / 10:5.1f}% | "
            f"Temperature: {temperature_raw / 10:4.1f} C | "
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