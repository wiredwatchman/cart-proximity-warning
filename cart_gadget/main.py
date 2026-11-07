# Cart Proximity Warning - Cart Gadget
#
# Runs on a Raspberry Pi Pico W at each cart.
# The warning activates only when BOTH are true:
#   1. A person is detected by the mmWave sensor, AND
#   2. The AMR / AGV beacon is nearby (Bluetooth signal strength).
# When both are true: the warning LED flashes and the DFPlayer plays the warning track.

import time

import bluetooth
from machine import Pin, UART

import config as cfg

# ---------------------------------------------------------------- hardware ---
mmwave = Pin(cfg.MMWAVE_PIN, Pin.IN, Pin.PULL_DOWN)
warn_led = Pin(cfg.WARNING_LED_PIN, Pin.OUT)
status_led = Pin("LED", Pin.OUT)
df = UART(cfg.DF_UART_ID, baudrate=9600, tx=Pin(cfg.DF_TX_PIN), rx=Pin(cfg.DF_RX_PIN))

# ------------------------------------------------------------- DFPlayer Mini --
def df_cmd(cmd, p1=0, p2=0):
    """Send one 10-byte DFPlayer Mini command frame."""
    buf = bytearray([0x7E, 0xFF, 0x06, cmd, 0x00, p1, p2, 0, 0, 0xEF])
    checksum = (0 - sum(buf[1:7])) & 0xFFFF
    buf[7] = checksum >> 8
    buf[8] = checksum & 0xFF
    df.write(buf)


def play_warning():
    df_cmd(0x03, 0, cfg.WARNING_TRACK)   # Play track by number


def stop_warning():
    df_cmd(0x16)                          # Stop playback


# ------------------------------------------------------------ BLE scanning ---
_IRQ_SCAN_RESULT = 5
_TARGET = cfg.ROBOT_NAME.encode()

ble = bluetooth.BLE()
ble.active(True)

robot_rssi = []        # Recent RSSI readings from the robot
last_robot_seen = None # ticks_ms of last matching advertisement


def _local_name(adv):
    """Return the complete or shortened local name from advertising data, or None."""
    i = 0
    while i < len(adv) - 1:
        length = adv[i]
        if length == 0:
            break
        kind = adv[i + 1]
        if kind in (0x08, 0x09):
            return bytes(adv[i + 2:i + 1 + length])
        i += length + 1
    return None


def _on_ble_event(event, data):
    global last_robot_seen
    if event == _IRQ_SCAN_RESULT:
        _addr_type, _addr, _adv_type, rssi, adv_data = data
        if _local_name(adv_data) == _TARGET:
            robot_rssi.append(rssi)
            if len(robot_rssi) > cfg.RSSI_SAMPLES:
                robot_rssi.pop(0)
            last_robot_seen = time.ticks_ms()


def robot_near():
    if last_robot_seen is None or not robot_rssi:
        return False
    if time.ticks_diff(time.ticks_ms(), last_robot_seen) > cfg.ROBOT_TIMEOUT_MS:
        return False
    average = sum(robot_rssi) / len(robot_rssi)
    return average > cfg.RSSI_THRESHOLD


# ------------------------------------------------------- person detection ----
last_person_seen = None


def person_present():
    global last_person_seen
    if mmwave.value() == 1:
        last_person_seen = time.ticks_ms()
    if last_person_seen is None:
        return False
    return time.ticks_diff(time.ticks_ms(), last_person_seen) < cfg.PERSON_HOLD_MS


# ------------------------------------------------------------------ main -----
def main():
    ble.irq(_on_ble_event)
    ble.gap_scan(0, 30000, 30000, True)   # 0 = scan continuously

    df_cmd(0x06, 0, cfg.VOLUME)           # Set volume
    time.sleep_ms(200)
    print("Cart gadget ready. Looking for", cfg.ROBOT_NAME)

    alarm = False
    last_play = 0

    while True:
        warn = robot_near() and person_present()

        if warn and not alarm:
            alarm = True
            play_warning()
            last_play = time.ticks_ms()
            print("WARNING ON: robot near and person present")
        elif alarm and not warn:
            alarm = False
            stop_warning()
            warn_led.off()
            print("WARNING OFF")

        if alarm:
            warn_led.toggle()
            if time.ticks_diff(time.ticks_ms(), last_play) > cfg.REPLAY_MS:
                play_warning()
                last_play = time.ticks_ms()

        status_led.toggle()
        time.sleep_ms(250)


main()
