# wifi_snr_rssi_noise.py
#
# MacOS only RSSI, Noise, and SNR on en0, Currently loops to show  values.
#
# TODO: Create Wifi locator using Yagi-Udo Antenna using RSSI, Noise, and SNR
# 1) Hook Yagi-Udo to Alfa external antenna
# 2) Use this to locate a Raspberry Pi Pico 2 W that has a 2.4GHz Wifi.
# 3) Output RSSI, Noise, and SNR (RSSI - Noise), to find Pico 2 W
#
# usage:
#   python3 wifi_snr_rssi_noise.py
#
# Install prerequisites:
#    pip install pyobjc
#    pip install pyobjc-framework-CoreWLAN
#
# ----------------
# RSSI, higher is better
#  * 4 bars is excellent: > -50 dBm
#  * 3 bars is good: -50 to -60 dBm
#  * 2 bars is ok: -60 to -70 dBm
#  * 1 bar is fair: < -70 dBm
#
# Noise, lower is better
#  * -90 to -100 dBm: Extremely low noise levels, ideal for WiFi
#  * -80 to -90 dBm: Low noise, still conducive to good  WiFi
#  * -70 to -80 dBm: Moderate noise starts to effect WiFi in crowed environments
#  * -60 to -70 dBm: High noise, causes noticeable degradation
#  * Above -60 dBm: Very high noise, often disconnects, slow speeds, & more errors
#
# SNR (rssi - noise), higher is better
#  * Above  30 is very good
#  * 14 to 25 is good
#  * Below 14 is bad
#
# Sample Outputs
# --------------
# RSSI:  -28 dBm
# Noise: -94 dBm
# SNR:    66 dB
#
# office environent
# RSSI:  -45 dBm, 4 bars
# Noise: -100 dBm, very low
# SNR:    55 dB, very good

import objc
from Foundation import NSObject

# Load CoreWLAN framework
objc.loadBundle(
    "CoreWLAN",
    globals(),
    bundle_path="/System/Library/Frameworks/CoreWLAN.framework"
)

CWInterface = objc.lookUpClass("CWInterface")


def query_wifi():
    """
    MacOS query rssi and noise form Wifi.
    Typical execution time is ~20msec, update rate ~50 Hz.

    :return: tuple
        noise: noise (int): Noise level in dBm.
        rssi:  rssi  (int): RSSI level in dBm.
    """
    wifi = CWInterface.interface()
    rssi = wifi.rssiValue()
    noise = wifi.noiseMeasurement()
    return rssi, noise


def print_summary(noise, rssi):
    """
    Prints a summary of RSSI, noise and SNR.
    While SNR is ratio, bedause of log scales this is a subtraction.

    :param noise: noise (int): Noise level in dBm.
    :param rssi:  rssi  (int): RSSI level in dBm.
    :return:
    """
    snr = rssi - noise
    print(f"RSSI:  {rssi:>4} dBm")
    print(f"Noise: {noise:>4} dBm")
    print(f"SNR:   {rssi - noise:>4} dB\n")


def print_with_string(noise, rssi):
    """
    Prints RSSI, noise and SNR with textual interpretation
    While SNR is ratio, bedause of log scales this is a subtraction.

    :param noise: noise (int): Noise level in dBm.
    :param rssi:  rssi  (int): RSSI level in dBm.
    :return:
    """
    snr = rssi - noise

    # RSSI quality, higher is better
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

    # Noise level, lower is better
    if noise < -90:
        noise_string = "very low"
    elif noise > -80:
        noise_string = "low"
    elif noise > -70:
        noise_string = "moderate"
    elif noise > -60:
        noise_string = "high"
    else:
        noise_string = "very high"

    # SNR quality, higher is better
    if snr > 30:
        snr_string = "very good"
    elif snr > 25:
        snr_string = "good"
    elif snr > 14:
        snr_string = "ok"
    else:
        snr_string = "poor"

    print(f"RSSI:  {rssi:>4} dBm, {rssi_string}")
    print(f"Noise: {noise:>4} dBm, {noise_string}")
    print(f"SNR:   {snr:>4} dB, {snr_string}\n")


def main():

    # get Wi-Fi interface (usually "en0")
    while True:
        rssi, noise = query_wifi()
        # print_summary(noise, rssi)
        print_with_string(noise, rssi)


if __name__ == "__main__":
    main()
