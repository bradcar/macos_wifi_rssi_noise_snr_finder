# MacOS Wifi - RSSI, Noise, SNR 
## Accesses MacOS Wifi Paramters

MacOS-only Wifi Monitoring of RSSI, Noise, and SNR on en0. Currently it just loops to shows ouput values.

TODO: Create Wifi locator using Yagi-Uda Antenna using RSSI, Noise, and SNR
1) Hook Yagi-Uda directional antenna to Alfa external antenna
2) Use the Output RSSI, Noise, and SNR (RSSI - Noise), to find Pico 2 W (2.4GHz Wifi).
3) By moving Yagi-Uda Antenna shoud be able to use direction of antenna to locate a Raspberry Pi Pico 2 W.

### Usage:
    python3 wifi_snr_rssi_noise.py

Or use program in Terminal Curses output:

    python3 curses_output.py

## Wifi Definitions

RSSI, higher is better:
* 4 bars is excellent: > -50 dBm
* 3 bars is good: -50 to -60 dBm
* 2 bars is ok: -60 to -70 dBm
* 1 bar is fair: < -70 dBm

Noise, lower is better:
* -90 to -100 dBm: Extremely low noise levels, ideal for WiFi
* -80 to -90 dBm: Low noise, still conducive to good  WiFi
* -70 to -80 dBm: Moderate noise starts to effect WiFi in crowed environments
* -60 to -70 dBm: High noise, causes noticeable degradation
* Above -60 dBm: Very high noise, often disconnects, slow speeds, & more errors

SNR (rssi - noise), higher is better:
* Above 30: Very good
* 14 to 25: Food
* Below 14: Bad

## Sample Outputs

Home (desk on top of wifi):
* RSSI:  -30 dBm, 4 bars
* Noise: -94 dBm, very low
* SNR:    64 dB, very good

office environment:
* RSSI:   -45 dBm, 4 bars
* Noise: -100 dBm, very low
* SNR:     55 dB, very good

## Install Prerequisites:

    pip install pyobjc
    pip install pyobjc-framework-CoreWLAN

## References

Very Practical Yagi-Uda design from Ham radio long-timer
* https://www.youtube.com/watch?v=SKumu3twopc

Yagi-Uda principles
* https://en.wikipedia.org/wiki/Yagi%E2%80%93Uda_antenna

Connecting to Mac USB to external antenna with MacOS support (I hope!?!)
* https://www.amazon.com/dp/B08BJS8FXD

My focus is 2.4GHz Wifi (Raspbery Pi Picc 2 W). The latest Wifi are at higher frequencies and I have not explored their use.

2.4 GHz Wifi Yagi-Uda 2.4 GHz directional Antenna that I will test, (will update this README.md on success!):
* https://www.amazon.com/dp/B00OCJYPCY

A 2.4 GHz half-wavelength antenna is approximately 62.5 mm (about 2.46 inches) long.
This is calculated by finding the full wavelength of a 2.4 GHz signal, which is about 125 mm, and then dividing it by two.
The antenna's total length is split into two elements, each approximately 31.25 mm long, but need to tune.
* Practical the quarter dipole is shorter (WTF): https://www.youtube.com/watch?v=8iBoRNyrrPM
* 29.7mm bare copper wire
* 28.2mm insulation before bare wire
* 2.4 to 2.5 frequency hopping = 29.07mm 5% = 27.6mm
