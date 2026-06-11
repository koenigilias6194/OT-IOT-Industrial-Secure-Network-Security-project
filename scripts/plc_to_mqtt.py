import time
from pymodbus.client import ModbusTcpClient
import paho.mqtt.client as mqtt

# Connection settings
PLC_IP = "10.10.10.10"
MQTT_BROKER = "10.10.20.10"

# Connect to MQTT broker
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, 1883)

# Connect to PLC
plc = ModbusTcpClient(PLC_IP, port=502)
plc.connect()

print("Connected! Reading PLC data and publishing to MQTT...")

while True:
    try:
        # Read holding registers (Temperature, Pressure, FlowRate)
        registers = plc.read_holding_registers(1024, count=3)
        if not registers.isError():
            mqtt_client.publish("factory/temperature", registers.registers[0])
            mqtt_client.publish("factory/pressure", registers.registers[1])
            mqtt_client.publish("factory/flowrate", registers.registers[2])

        # Read coils (Motor, Pump, Alarm)
        coils = plc.read_coils(0, count=3)
        if not coils.isError():
            mqtt_client.publish("factory/motor", str(coils.bits[0]))
            mqtt_client.publish("factory/pump", str(coils.bits[1]))
            mqtt_client.publish("factory/alarm", str(coils.bits[2]))

        print(f"Temp:{registers.registers[0]} Pressure:{registers.registers[1]} Flow:{registers.registers[2]}")
        time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(2)
