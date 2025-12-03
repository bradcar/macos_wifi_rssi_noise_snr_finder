# MacOS Wifi - RSSI, Noise, SNR 
## Accesses MacOS Wifi Paramters

MacOS-only Wifi Mointoring of RSSI, Noise, and SNR on en0. Currently it just loops to shows ouput values.

TODO: Create Wifi locator using Yagi-Udo Antenna using RSSI, Noise, and SNR
1) Hook Yagi-Udo to Alfa external antenna
2) Use this to locate a Raspberry Pi Pico 2 W that has a 2.4GHz Wifi.
3) Output RSSI, Noise, and SNR (RSSI - Noise), to find Pico 2 W

### usage:
    python3 wifi_snr_rssi_noise.py

or Terminal Curses output:

    python3 curses_output.py

## Wifi Definitions

RSSI, higher is better
* 4 bars is excellent: > -50 dBm
* 3 bars is good: -50 to -60 dBm
* 2 bars is ok: -60 to -70 dBm
* 1 bar is fair: < -70 dBm

Noise, lower is better
* -90 to -100 dBm: Extremely low noise levels, ideal for WiFi
* -80 to -90 dBm: Low noise, still conducive to good  WiFi
* -70 to -80 dBm: Moderate noise starts to effect WiFi in crowed environments
* -60 to -70 dBm: High noise, causes noticeable degradation
* Above -60 dBm: Very high noise, often disconnects, slow speeds, & more errors

SNR (rssi - noise), higher is better
* Above  30 is very good
* 14 to 25 is good
* Below 14 is bad

## Sample Outputs

Home (desk on top of wifi)
* RSSI:  -30 dBm, 4 bars
* Noise: -94 dBm, very low
* SNR:    64 dB, very good

office environent
* RSSI:   -45 dBm, 4 bars
* Noise: -100 dBm, very low
* SNR:     55 dB, very good

## Install prerequisites:

    pip install pyobjc
    pip install pyobjc-framework-CoreWLAN