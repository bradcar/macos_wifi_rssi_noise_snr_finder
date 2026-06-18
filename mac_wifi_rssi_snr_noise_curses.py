# mac_wifi_rssi_snr_noise_curses.py
#
# Simple terminal output using curses to overwrite results to show continuous updates
# of RSSI, noise, SNR with update duration in msec, frequency and current datetime.
# Also prints out the name of the en0 Wifi network it is monitoring.
# However, Python must be enabled in System Settings > Privacy & Security> Location Services.
#
# Usage:
#   in terminal, python3 mac_wifi_rssi_snr_noise_curses.py
#
# Sample output:
#  WiFi Signal Monitor: XYZ
#
#     RSSI:  -23 dBm
#     Noise: -94 dBm
#     SNR:    71 dB
#
#     Updates:  15.4 msec, 65 Hz
#     Clock: 2025-12-04 19:44:38
#
# Install prerequisites:
#    pip install pyobjc
#    pip install pyobjc-framework-CoreWLAN
#    Python must be enabled in: System Settings > Privacy & Security > Location Services
#
import curses
import time
from datetime import datetime

from mac_wifi_rssi_snr_noise import get_ssid, query_wifi, rssi_snr_noise_to_string


def main_window(stdscr):
    curses.curs_set(0)  # hide cursor
    stdscr.nodelay(True)

    ssid = get_ssid()
    while True:
        start_time = time.time()
        rssi, noise = query_wifi()
        snr = rssi - noise
        duration = time.time() - start_time

        rssi_string, snr_string, noise_string = rssi_snr_noise_to_string(rssi, snr, noise)

        stdscr.clear()
        stdscr.addstr(1, 1, f"WiFi Signal Monitor (macOS): {ssid}")
        stdscr.addstr(3, 4, f"RSSI: {rssi:>4} dBm  {rssi_string}")
        stdscr.addstr(4, 4, f"Noise:{noise:>4} dBm  {noise_string}")
        stdscr.addstr(5, 4, f"SNR:  {snr:>4} dB   {snr_string}")

        stdscr.addstr(7, 4, f"Updates:  {duration * 1000:.1f} msec, {1.0 / duration:.0f} Hz")
        stdscr.addstr(8, 4, f"Clock: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        stdscr.refresh()
        time.sleep(0.1)


if __name__ == "__main__":
    curses.wrapper(main_window)
