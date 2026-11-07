# Wiring

This guide covers one cart gadget. The robot beacon needs only a Pico W and power.

## Parts (approximate)

| Part | Notes | Approx. cost |
|------|-------|--------------|
| Raspberry Pi Pico W | Runs both the beacon and the gadget | ~$6 |
| mmWave presence sensor module | Digital output (HIGH when presence detected) | ~$5–15 |
| DFPlayer Mini MP3 module | With a microSD card holding `0001.mp3` | ~$3–5 |
| Small speaker (3 W, 4–8 Ω) | Connects to the DFPlayer SPK pins | ~$2–5 |
| Warning LED + 220 Ω resistor | Any bright LED works | ~$1 |
| Enclosure, power bank, wire | Weatherproof enclosure recommended for shop floors | Varies |

## Pin map (cart gadget)

| Pico W pin | Connects to | Notes |
|-----------|-------------|-------|
| GP16 | mmWave sensor OUT | Digital output; HIGH = presence |
| GP15 | Warning LED anode, through 220 Ω | LED cathode to GND |
| GP4 (UART1 TX) | DFPlayer RX | Use a 1 kΩ series resistor on this line for safety |
| GP5 (UART1 RX) | DFPlayer TX | |
| 3V3 (pin 36) | mmWave VCC, DFPlayer VCC | Check your sensor's voltage rating; some modules need 5 V |
| GND | Every module's GND | Share one ground |

Connect the speaker to the DFPlayer's SPK+ and SPK− pins.

## Beacon (robot)

- Power the Pico W from the robot's 5 V supply or a USB power bank.
- No other connections are needed.

## Before powering up

- Confirm the mmWave module's supply voltage. Do not feed 5 V into a 3.3 V-only module.
- Confirm GND is common across all modules.
- Format the microSD card as FAT32 and copy the warning sound as `0001.mp3`.
