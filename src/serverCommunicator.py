import paho.mqtt.client as mqtt
import json
import time

VERSION = "1.0.0"


def statHandler():
    pass  # TODO


def editHandler():
    pass  # TODO


def invalidHandler():
    pass  # TODO


commandList = {"stat": statHandler, "edit": editHandler}


def onMessage(client, obj, msg):
    cmd = msg.payload.decode("utf-8").lower()
    print(f"Got a payload : {cmd}")

    # Check if user input is valid
    if cmd not in commandList:
        invalidHandler()
    else:
        commandList[cmd]


def main():
    print("Pocket Farm V")
    print("LINE COMMUNICATION MODULE")
    print(f"VERSION : {VERSION}")
    print("_________________________")

    print("Initialising... ", end="")
    mqttc = mqtt.Client()
    mqttc.on_message = onMessage
    mqttc.username_pw_set("brsiutlc", "Rw4rcSFm_gCL")
    mqttc.connect("m15.cloudmqtt.com", 17711)
    mqttc.subscribe("/test1", 0)
    print("Done")

    print("\nWaiting for Line payload... \n")
    mqttc.loop_forever()


if __name__ == "__main__":
    main()
