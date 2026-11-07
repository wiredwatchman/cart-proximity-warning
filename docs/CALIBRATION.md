# Calibration

Bluetooth signal strength changes with metal racks, walls, people, and the robot's mounting position. Tune the system where it will actually run.

## 1. Measure the signal

1. Flash `robot_beacon/main.py` to the robot's Pico W and power it.
2. Install a BLE scanner app on a phone (for example, nRF Connect).
3. Find `CART-AMR-01` in the scan list and note the RSSI at several distances: 10 ft, 6 ft, 4 ft, and 2 ft.
4. Repeat with the robot in the positions it will approach the cart from, with a realistic load on the cart.

## 2. Set the threshold

In `cart_gadget/config.py`, set `RSSI_THRESHOLD` to a value between the RSSI you see at your target distance and the RSSI you see farther away. Start at -70 dBm and adjust.

- Threshold too weak (for example, -90): the warning triggers when the robot is far away.
- Threshold too strong (for example, -50): the warning triggers only when the robot is nearly touching the cart.

## 3. Tune the person sensor

- Adjust the mmWave sensor's range and sensitivity using its own configuration tool or adjustment pins, per its datasheet.
- Set `PERSON_HOLD_MS` so the warning does not drop out between sensor readings.

## 4. Test the full system

1. Power the robot beacon and one cart gadget.
2. Walk toward the cart with the robot stationary nearby. Confirm the warning activates only when both conditions are true.
3. Hold the robot still and step away. Confirm the warning stops after `PERSON_HOLD_MS`.
4. Hold a person still in front of the sensor with the robot out of range. Confirm no warning.
5. Run the robot's approach route several times and log the results.

## 5. Check audio and light

- Set `VOLUME` so the sound is clearly audible over the loading area's background noise.
- Confirm the LED is visible in daylight and in the dimmest part of the shop.

## Troubleshooting

| Symptom | Likely cause |
|---------|--------------|
| Robot never detected | Name mismatch between files; beacon not powered; RSSI below threshold |
| Warning flickers | Increase `PERSON_HOLD_MS` or `RSSI_SAMPLES` |
| No sound | DFPlayer TX/RX swapped; no `0001.mp3` on the SD card; SD card not FAT32 |
| Warning on with no robot | Threshold too weak; raise `RSSI_THRESHOLD` |
