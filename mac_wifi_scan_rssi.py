# mac_wifi_scan_rssi.py
"""
runs on Macbook Pro in MacOS
2.4, 5, & 6 GHz Wifi - RSSI ONLY
Scans repeatedly, sorted by strongest RSSI first.
CANNOT get noise & SNR on unconnected networks. For connected network use: mac_wifi_rssi_snr_noise.py

NOTES:
  1) Python MUST be enabled in System Settings > Privacy & Security> Location Services.

Usage:
  in terminal, python3 mac_wifi_scan_rssi.py
  can also run in pycharm
"""
import time
from datetime import datetime

from CoreWLAN import CWWiFiClient

BLOCK_LESS_THAN_ONE_BAR = True
BLOCK_NON_2_4_G = True


def init_wifi():
    """Initialize CoreWLAN client and returns the active Wi-Fi"""
    client = CWWiFiClient.sharedWiFiClient()
    return client.interface()


def map_band_to_string(net) -> str:
    """Map bands using CoreWLAN's band integers"""
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


def scan_and_print(interface):
    """network scan using the interface, print sorted RSSI, current row counts header, dash row, and network count"""
    if not interface:
        print("Error: Wi-Fi interface not found or initialized.")
        return False, 1

    # Scan for networks, include (None) and hidden networks (True)
    networks, error = interface.scanForNetworksWithSSID_includeHidden_error_(None, True, None)

    if error:
        # Code 16 "Resource busy" (EBUSY), return for retry
        if error.code() == 16:
            return False, 1

        print(f"Scan error: {error}")
        return False, 1

    if not networks:
        print("No networks found. Ensure Terminal/IDE has Location Services permissions.")
        return False, 1

    # Sort networks by their RSSI value in descending order (strongest first)
    sorted_networks = sorted(networks, key=lambda net: net.rssiValue(), reverse=True)

    current_row = 0

    print(f"{'SSID':<23} {'Band':<7} {'BSSID':<17} {'RSSI':<9} {'Bars'}")
    current_row += 1
    print("-" * 66)
    current_row += 1

    for net in sorted_networks:
        ssid = net.ssid() or "<hidden>"
        bssid = net.bssid() or "Unknown"
        rssi = net.rssiValue()

        band = map_band_to_string(net)
        rssi_string = rssi_bar_string(rssi)

        if not (BLOCK_LESS_THAN_ONE_BAR and rssi <= -80) and not (BLOCK_NON_2_4_G and band != "2.4 GHz"):
            print(f"{ssid:<23} {band:<7} {bssid} {rssi:>4} dBm  {rssi_string}")
            current_row += 1

    return True, current_row


def main():
    last_update = time.time()
    wifi_interface = init_wifi()
    print("Continuous Wi-Fi scan:")

    try:
        while True:
            success, current_row = scan_and_print(wifi_interface)
            if success:
                duration = time.time() - last_update
                last_update = time.time()
                print(f"  Clock: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, Update every {duration:.2f} secs")
                print(
                    f"  Blocked <1-bar and non 2.4GHz" if BLOCK_LESS_THAN_ONE_BAR and BLOCK_NON_2_4_G else f"Blocked <1-bar" if BLOCK_LESS_THAN_ONE_BAR else f"Blocked non 2.4GHz" if BLOCK_NON_2_4_G else "")
                print()
                # MacOS ONLY retry in 6 sec (MacOS slow)
                time.sleep(6)
            else:
                # If the hardware was busy, retry in 1 second
                time.sleep(1)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
    print("\nExiting.")
