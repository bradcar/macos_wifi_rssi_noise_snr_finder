# curses_output.py
#
# Simple terinal output using curses to overwrite results to show continuous updates
# of RSSI, noise, SNR with update duration in msec, frequency and current datetime.
# Also prints out the name of the en0 Wifi network it is monitoring.
# However, Python must be enabled in System Settings > Privacy & Security> Location Services.
#
# Usage:
#   in termainal, python3 curses_output.py
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
import curses
import time
from datetime import datetime

from wifi_snr_rssi_noise import query_wifi, enable_ssid_name


def main_window(stdscr):
    enable_ssid_name()
    curses.curs_set(0)  # hide cursor
    stdscr.nodelay(True)

    while True:
        start_time = time.time()
        rssi, noise, ssid = query_wifi()
        snr = rssi - noise
        duration = time.time() - start_time

        stdscr.clear()
        stdscr.addstr(1, 1, f"WiFi Signal Monitor: {ssid}")
        stdscr.addstr(3, 4, f"RSSI:  {rssi:>4} dBm")
        stdscr.addstr(4, 4, f"Noise: {noise:>4} dBm")
        stdscr.addstr(5, 4, f"SNR:   {snr:>4} dB")

        stdscr.addstr(7, 4, f"Updates:  {duration * 1000:.1f} msec, {1.0 / duration:.0f} Hz")
        stdscr.addstr(8, 4, f"Clock: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        stdscr.refresh()
        time.sleep(0.1)


if __name__ == "__main__":
    curses.wrapper(main_window)
