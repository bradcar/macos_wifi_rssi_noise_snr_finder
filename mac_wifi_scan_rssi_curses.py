# mac_wifi_scan_rssi.py
"""
runs on Macbook Pro in MacOS
2.4, 5, & 6 GHz Wifi - RSSI ONLY
Scans repeatedly, sorted by strongest RSSI first.
CANNOT get noise & SNR on unconnected networks. For connected network use: wifi_rssi_snr_noise.py

NOTES:
  1) Python MUST be enabled in System Settings > Privacy & Security> Location Services.

Usage:
  Curses requires running in terminal:
  python3 mac_wifi_scan_rssi_curses.py
"""
import curses
import time
from datetime import datetime

from CoreWLAN import CWWiFiClient


def init_wifi():
    """Initialize CoreWLAN client and returns the active Wi-Fi"""
    client = CWWiFiClient.sharedWiFiClient()
    return client.interface()


def map_band_to_string(net) -> str:
    # Map bands using CoreWLAN's band integers
    channel_obj = net.wlanChannel()
    band = "Unknown"
    if channel_obj:
        c_band = channel_obj.channelBand()
        if c_band == 1:  # 2.4 GHz
            band = "2.4 GHz"
        elif c_band == 2:  # 5 GHz
            band = "5 GHz"
        elif c_band == 3:  # 6 GHz
            band = "6 GHz"
    return band


def rssi_bar_string(rssi) -> str:
    """RSSI quality, higher is better"""
    if rssi > -50:
        rssi_string = "4 bars"
    elif rssi > -60:
        rssi_string = "3 bars"
    elif rssi > -70:
        rssi_string = "2 bars"
    elif rssi > -80:
        rssi_string = "1 bar"
    else:
        rssi_string = "0 bar"
    return rssi_string


def scan_and_print(interface, stdscr):
    """network scan using the interface, print sorted RSSI"""
    if not interface:
        stdscr.addstr(0, 0, "Error: Wi-Fi interface not found or initialized.")
        stdscr.refresh()
        return False

    # Scan for networks, include (None) and hidden networks (True)
    networks, error = interface.scanForNetworksWithSSID_includeHidden_error_(None, True, None)

    if error:
        # Code 16 "Resource busy" (EBUSY), return for retry
        if error.code() == 16:
            return False, 1

        stdscr.addstr(0, 0, f"Scan error: {error}")
        stdscr.refresh()
        return False, 1

    if not networks:
        stdscr.addstr(0, 0, "No networks found. Ensure Terminal/IDE has Location Services permissions.")
        stdscr.refresh()
        return False, 1

    # Sort networks by their RSSI value in descending order (strongest first)
    sorted_networks = sorted(networks, key=lambda net: net.rssiValue(), reverse=True)

    stdscr.clear()

    # Track the terminal boundaries to avoid writing past the screen limits
    max_y, max_x = stdscr.getmaxyx()
    current_row = 0

    stdscr.addstr(current_row, 0, f"{'SSID':<23} {'Band':<7} {'BSSID':<17} {'RSSI':<9} {'Bars'}")
    current_row += 1
    stdscr.addstr(current_row, 0, "-" * 66)
    current_row += 1

    for net in sorted_networks:
        if current_row >= max_y - 1:
            break  # Stop printing if we run out of screen space

        ssid = net.ssid() or "<hidden>"
        bssid = net.bssid() or "Unknown"
        rssi = net.rssiValue()

        band = map_band_to_string(net)
        rssi_string = rssi_bar_string(rssi)

        stdscr.addstr(current_row, 0, f"{ssid:<23} {band:<7} {bssid} {rssi:>4} dBm  {rssi_string}")
        current_row += 1

    stdscr.refresh()
    return True, current_row




def main(stdscr):
    # Hide the blinking cursor for curses
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    last_update = time.time()
    wifi_interface = init_wifi()
    stdscr.addstr(0, 0, "Continuous Wi-Fi scan:")
    stdscr.refresh()

    try:
        while True:
            success, current_row = scan_and_print(wifi_interface, stdscr)
            if success:
                duration = time.time() - last_update
                last_update = time.time()
                stdscr.addstr(current_row, 2,
                              f"Clock: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Update every {duration:.2f} secs")
                stdscr.refresh()
                # retry in 6 sec (MacOS slow)
                time.sleep(6)
            else:
                # If the hardware was busy, retry in 1 second
                time.sleep(1)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    curses.wrapper(main)
    print("\nExiting.")
