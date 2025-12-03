# curses_output.py
#
# Simple terinal output using curses to overwrite results to show continuous updates
# of RSSI, noise, SNR with update duration in msec, frequency and current datetime.
#
# Usage:
#   in termainal, python3 curses_output.py
#
import curses
import time
from datetime import datetime

from wifi_snr_rssi_noise import query_wifi


def main_window(stdscr):
    curses.curs_set(0)  # hide cursor
    stdscr.nodelay(True)

    while True:
        start_time = time.time()
        rssi, noise = query_wifi()
        snr = rssi - noise
        duration = time.time() - start_time

        stdscr.clear()
        stdscr.addstr(1, 1, "WiFi Signal Monitor")
        stdscr.addstr(3, 4, f"RSSI:  {rssi:>4} dBm")
        stdscr.addstr(4, 4, f"Noise: {noise:>4} dBm")
        stdscr.addstr(5, 4, f"SNR:   {snr:>4} dB")

        stdscr.addstr(7, 4, f"Updates:  {duration * 1000:.1f} msec, {1.0/duration:.0f} Hz")
        stdscr.addstr(8, 4, f"Clock: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        stdscr.refresh()
        time.sleep(0.1)


if __name__ == "__main__":
    curses.wrapper(main_window)
