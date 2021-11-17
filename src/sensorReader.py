import serial
import time


ARDUINO_TIMEOUT = 5  # Wait for serial from Arduino n cycle until time out
ARDUINO_WAIT_TIME = 0.25  # Wait time for serial from Arduino in each cycle


def getArduinoSerial():
    arduinoSerial = serial.Serial("/dev/ttyUSB0", 9600)

    # Check if serial available
    for i in range(ARDUINO_TIMEOUT):
        if arduinoSerial.in_waiting():  # There is a serial incomming
            print("[ OK ] Serial found.")
            break
        time.sleep(ARDUINO_WAIT_TIME)  # Wait for serial from Arduino
    else:
        print(f"[ ERROR ] Arduino serial timeout. Waiting... ({i}/{ARDUINO_TIMEOUT})")
        return None

    # Check for incomplete serial
    for i in range(ARDUINO_TIMEOUT):
        serialData = arduinoSerial.readline().decode("utf-8").split()
        if len(serialData) == 5:
            print("[ OK ] Serial data is complete.")
            return serialData
        print(
            f"[ ERROR ] Serial is incomplete. Getting new one... ({i}/{ARDUINO_TIMEOUT})"
        )
        time.sleep(ARDUINO_WAIT_TIME)  # Wait for new serial from Arduino
    else:
        print("[ ERROR ] Arduino serial timeout. Cannot get complete serial data.")
        return None


def readSensor():
    serialData = getArduinoSerial()
    if serialData is None:
        print("[ ERROR ] Cannot get serial data from Arduino.")

    print(f"Serial data :\n{serialData}")

    keys = [
        "insideHumidity",
        "insideTemperature",
        "Moisure",
        "outsideHumidity",
        "outsideTemperature",
    ]

    data = {keys[i]: int(serialData[i]) for i in range(5)}
    data["light"] = 1  # placeholder

    return data
