# Cart Proximity Warning - Robot Beacon
#
# Runs on the Raspberry Pi Pico W mounted on the AMR / AGV.
# Broadcasts a Bluetooth Low Energy advertisement so nearby cart gadgets
# know the robot is on its way to pick up a cart.
#
# Hardware: Raspberry Pi Pico W (MicroPython firmware).
# No wiring required beyond USB or battery power.

import time

import bluetooth
from machine import Pin

ROBOT_NAME = "CART-AMR-01"   # Must match ROBOT_NAME in cart_gadget/config.py
ADV_INTERVAL_US = 100_000    # Advertise every 100 ms


def adv_payload(name):
    """Build a BLE advertising payload: flags field + complete local name."""
    raw = name.encode()
    flags = bytes((2, 0x01, 0x06))                 # General discoverable, BR/EDR not supported
    name_field = bytes((len(raw) + 1, 0x09)) + raw  # 0x09 = Complete Local Name
    return flags + name_field


def main():
    ble = bluetooth.BLE()
    ble.active(True)
    led = Pin("LED", Pin.OUT)

    ble.gap_advertise(ADV_INTERVAL_US, adv_data=adv_payload(ROBOT_NAME))
    print("Cart beacon broadcasting as", ROBOT_NAME)

    while True:
        # Slow blink = beacon is alive.
        led.toggle()
        time.sleep(1)


main()
