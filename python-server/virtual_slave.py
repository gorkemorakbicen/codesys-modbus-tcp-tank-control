from time import sleep

from pyModbusTCP.server import DataBank, ModbusServer


HOST = "127.0.0.1"
PORT = 502

SIMULATION_CYCLE = 0.5
LEVEL_STEP_RAW = 20

data_bank = DataBank()

# Başlangıç proses değerleri
tank_level_raw = 500      # 50.0 %
temperature_raw = 240      # 24.0 °C

# Sanal sensör register'ları
data_bank.set_input_registers(
    0,
    [tank_level_raw, temperature_raw]
)

# CODESYS'in yazacağı komut register'ları
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

    print(f"Modbus TCP Slave çalışıyor: {HOST}:{PORT}")
    print("CODESYS komutları bekleniyor.")
    print("Durdurmak için Ctrl+C kullan.\n")

    while True:
        # CODESYS'in Holding Register'lara yazdığı komutlar
        commands = data_bank.get_holding_registers(0, 2)

        pump_command = commands[0] == 1
        valve_command = commands[1] == 1

        # Fiziksel tank davranışının basit simülasyonu
        if pump_command and not valve_command:
            tank_level_raw += LEVEL_STEP_RAW

        elif valve_command and not pump_command:
            tank_level_raw -= LEVEL_STEP_RAW

        # Sanal tankın fiziksel sınırları: %0 ile %100
        tank_level_raw = max(0, min(1000, tank_level_raw))

        # Yeni sensör ölçümlerini Input Register'lara aktar
        data_bank.set_input_registers(
            0,
            [tank_level_raw, temperature_raw]
        )

        print(
            f"\rTank: {tank_level_raw / 10:5.1f}% | "
            f"Sıcaklık: {temperature_raw / 10:4.1f} C | "
            f"Pompa: {int(pump_command)} | "
            f"Vana: {int(valve_command)}",
            end="",
            flush=True
        )

        sleep(SIMULATION_CYCLE)

except KeyboardInterrupt:
    print("\nProgram kullanıcı tarafından durduruldu.")

finally:
    server.stop()
    print("Modbus TCP Slave kapatıldı.")


    """python -m pip install pyModbusTCP==0.3"""
