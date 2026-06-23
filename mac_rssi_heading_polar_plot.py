# mac_rssi_heading_polar_plot.py
"""
Polar plot of RSSI strength at 360° headings. Radar-style plot for analysis
of measured RSSI from directional antenna Yagi-Uda data.
Peak RSSI is detected and its value and heading are printed in the title.
Magnetic North is 0° degrees, East is 90° degrees.

Features:
- Detects peak RSSI, or mid of plateau of peaks
- Autoscales so the peak is 85% of the polar plot limit.
- Indicates peak with red line from plot boundary to peak, outside of boundary peaks RSSI printed.

Dependencies:
    pandas, matplotlib, numpy

Expected CSV Input Format:
    The input file must include headers matching 'degree' and 'rssi'.
    Example:
        degree,rssi
        0,-45
        10,-48.5
        ...

Note:
    Magnetic North 0° is at Top/Up. Clockwise rotation with East 90° at right.

Usage:
    python mac_rssi_heading_polar_plot.py <path_to_rssi_data.csv>

"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
from datetime import datetime
from lib.plot_rssi_polar_utils import  plot_rssi_polar
from pathlib import Path

# dBm bounds for clamping values and gridlines
RSSI_MAX_PLOT_CONSTANT = -20
RSSI_MIN_PLOT_CONSTANT = -99
Y_TICK_MAX = -10
Y_TICK_MIN = -90

LCD_PIXELS = 240
LCD_DPI = 100
LCD_SIZE_INCHES = LCD_PIXELS / LCD_DPI


def read_theata_rssi_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    theta = np.deg2rad(df['degree'])
    rssi = df['rssi']
    return df, rssi, theta


def main():
    print("Polar plot of RSSI strength at 360 degrees\n")
    print("Magnetic North is 0° degrees")
    if len(sys.argv) > 1:
        csv_name = sys.argv[1]
        df, rssi, theta = read_theata_rssi_from_csv(csv_name)

        # create directory & file for plots
        dir = "polar_plots"
        plot_dir = Path(dir)
        plot_dir.mkdir(exist_ok=True)
        base_name = Path(csv_name).stem
        file_path = plot_dir / f"{base_name}-{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.jpg"

        start_time = time.time()
        lcd_jpg_generate = False
        plot_rssi_polar(df, rssi, theta, csv_name, lcd_jpg_generate, file_path)
        print(f"plot time = {(time.time() - start_time):.2f} secs")
    else:
        print("Please enter a csv file")


if __name__ == "__main__":
    main()
