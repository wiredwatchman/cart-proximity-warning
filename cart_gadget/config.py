# Cart Proximity Warning - Cart Gadget Settings
#
# Edit these values for your build, then re-upload config.py to the Pico W.
# See docs/CALIBRATION.md for how to tune them in the field.

# --- Robot identity ---------------------------------------------------------
ROBOT_NAME = "CART-AMR-01"     # Must match ROBOT_NAME in robot_beacon/main.py

# --- Bluetooth proximity (robot is "near") ----------------------------------
RSSI_THRESHOLD = -70           # dBm. Robot counts as near when the averaged signal is stronger than this
RSSI_SAMPLES = 5               # Number of readings averaged to smooth out signal jumps
ROBOT_TIMEOUT_MS = 4000        # Robot counts as gone after this long with no advertisement

# --- Person detection (mmWave sensor) ---------------------------------------
PERSON_HOLD_MS = 3000          # Keep "person present" this long after the sensor clears

# --- Pins -------------------------------------------------------------------
MMWAVE_PIN = 16                # mmWave sensor digital output (HIGH = presence)
WARNING_LED_PIN = 15           # Warning LED (use a current-limiting resistor)
DF_UART_ID = 1                 # UART 1 on the Pico W
DF_TX_PIN = 4                  # Pico TX  -> DFPlayer RX
DF_RX_PIN = 5                  # Pico RX  <- DFPlayer TX

# --- Audio ------------------------------------------------------------------
WARNING_TRACK = 1              # Track number on the DFPlayer SD card (file 0001.mp3)
VOLUME = 20                    # 0-30
REPLAY_MS = 8000               # Re-start the warning track this often while the alarm is active
