# Cart Proximity Warning

A low-cost awareness system that tells people to clear out of the way when an autonomous mobile robot (AMR) or automated guided vehicle (AGV) is coming to pick up a cart.

A cart is loaded by hand. When the robot approaches, a Pico W on the robot broadcasts a Bluetooth signal. A Pico W gadget on the cart sees that signal and combines it with a mmWave presence sensor. Only when **the robot is nearby and a person is at the cart** does the gadget flash a warning LED and play a spoken or tone warning through a speaker.

Commercial presence and proximity systems for industrial vehicles often cost thousands of dollars per unit. This build targets roughly $20–40 in parts per cart.

> **Important:** This is an awareness device. It is not a certified safety system and must not replace the robot's safety scanners, physical guarding, or your site's lockout and traffic procedures. Follow your facility's safety program and applicable standards for AGVs and AMRs (for example, ANSI/ITSDF B56.5 in the US or ISO 3691-4 internationally).

## How it works

```
  ROBOT (Pico W)                          CART GADGET (Pico W)
  ───────────────                         ─────────────────────────────
  BLE advertisement   ── signal ──▶      Scans for robot, averages RSSI
  "CART-AMR-01"                           │
                                          ├─ Robot near?      ┐
  mmWave presence     ── GP16 ──▶        │                   ├─▶ WARNING
                                          └─ Person present?  ┘   LED + audio
```

- **Robot beacon:** advertises a name over Bluetooth Low Energy every 100 ms.
- **Cart gadget:** averages recent signal strength from the robot and checks the mmWave sensor. The alarm needs both.
- **Hold times and thresholds** are set in one file, so you can tune the system without changing the logic.

## Parts

See [docs/WIRING.md](docs/WIRING.md) for the full parts list, pin map, and wiring notes.

| Part | Qty per cart | Notes |
|------|--------------|-------|
| Raspberry Pi Pico W | 1 (+1 on the robot) | |
| mmWave presence sensor | 1 | Digital output module |
| DFPlayer Mini + microSD | 1 | Warning track as `0001.mp3` |
| Speaker, 3 W | 1 | |
| LED + 220 Ω resistor | 1 | |

## Quick start

1. **Install MicroPython** on each Pico W from [micropython.org](https://micropython.org/download/RPI_PICO_W/).
2. **Flash the robot beacon.** Copy `robot_beacon/main.py` to the robot's Pico W as `main.py`.
3. **Flash each cart gadget.** Copy `cart_gadget/main.py` and `cart_gadget/config.py` to the gadget's Pico W. Keep the names exactly `main.py` and `config.py`.
4. **Wire the gadget** using [docs/WIRING.md](docs/WIRING.md).
5. **Load the audio.** Put one warning sound on the microSD card as `0001.mp3` (FAT32).
6. **Calibrate** using [docs/CALIBRATION.md](docs/CALIBRATION.md).

Use [Thonny](https://thonny.org/) to copy files to the Pico W.

## Configuration

All settings live in `cart_gadget/config.py`:

| Setting | Default | Purpose |
|---------|---------|---------|
| `ROBOT_NAME` | `CART-AMR-01` | Must match the robot beacon |
| `RSSI_THRESHOLD` | `-70` | Signal strength (dBm) that counts as "robot near" |
| `RSSI_SAMPLES` | `5` | Readings averaged to smooth the signal |
| `ROBOT_TIMEOUT_MS` | `4000` | Robot counts as gone after this long |
| `PERSON_HOLD_MS` | `3000` | How long "person present" lasts after the sensor clears |
| `WARNING_TRACK` | `1` | Track number on the SD card |
| `VOLUME` | `20` | DFPlayer volume, 0–30 |
| `REPLAY_MS` | `8000` | How often the warning track restarts while active |

To use more than one robot, give each robot its own name and set each gadget's `ROBOT_NAME` to match.

## Project layout

```
cart-proximity-warning/
├── robot_beacon/
│   └── main.py          # Runs on the robot's Pico W
├── cart_gadget/
│   ├── main.py          # Runs on each cart's Pico W
│   └── config.py        # Settings for the cart gadget
├── docs/
│   ├── WIRING.md        # Parts, pin map, wiring
│   └── CALIBRATION.md   # Field tuning and troubleshooting
├── LICENSE
└── README.md
```

## Status and roadmap

- [x] Bluetooth robot beacon
- [x] Cart gadget with Bluetooth + mmWave AND logic
- [x] DFPlayer audio and warning LED
- [x] Single-file configuration
- [ ] Wi-Fi access point and web page for adjusting settings in the field
- [ ] Multiple warning levels by distance (for example, a yellow LED at 10 ft and red at 4 ft)
- [ ] Small display for warning text or countdown
- [ ] Battery monitoring on the beacon and gadget

## Limitations

- Bluetooth signal strength is affected by metal racks, walls, and people. Calibrate on site.
- The mmWave sensor detects presence, not intent. It may trigger for people who are not loading the cart.
- The system needs power on the robot and every cart. Check batteries before each shift.

## Contributing

Issues and pull requests are welcome. Please test changes on hardware before submitting, and note the robot and sensor models you used.

## License

Released under the MIT License. See [LICENSE](LICENSE).
