from time import sleep

import machine
import network

ssid = "iiNet1EE995 2.4gz"
password = "S0m3Th1nG"


def wait_wlan(wlan):
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("waiting for connection...")
        sleep(1)

    if wlan.status() != 3:
        print("Failed setting up wifi, will restart in 30 seconds")
        sleep(30)
        machine.reset()


def connect_wlan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.disconnect()

    wlan.active(True)
    wlan.connect(ssid, password)

    wait_wlan(wlan)

    print("connected to wifi with ip = ", wlan.ifconfig()[0])
    return wlan
