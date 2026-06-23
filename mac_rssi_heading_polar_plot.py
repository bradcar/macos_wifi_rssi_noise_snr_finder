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
from pathlib import Path

# dBm bounds for clamping values and gridlines
RSSI_MAX_PLOT_CONSTANT = -20
RSSI_MIN_PLOT_CONSTANT = -99
Y_TICK_MAX = -10
Y_TICK_MIN = -90

PIXELS = 240
DPI = 100
SIZE_INCHES = PIXELS / DPI


def read_theata_rssi_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    theta = np.deg2rad(df['degree'])
    rssi = df['rssi']
    return df, rssi, theta


def plot_rssi_polar(df, rssi, theta, subtitle, file_name="plot.jpg"):
    # Detect peak RSSI, or mid of plateau of peaks (issue? maybe 0 to 359° wrap)
    valid_data = df[df['rssi'] > -98]
    if valid_data.empty:
        peak_rssi = -99.0
        peak_degree = 0
    else:
        max_rssi = valid_data['rssi'].max()
        peak_cluster = valid_data[valid_data['rssi'] == max_rssi]
        peak_rssi = float(max_rssi)

        # Get first and last target degrees in the peak sequence
        first_deg = float(peak_cluster['degree'].iloc[0])
        last_deg = float(peak_cluster['degree'].iloc[-1])
        peak_degree = float(peak_cluster['degree'].mean())  # middle angle of disparate values of same peak value

        # calc shortest path arc connecting, accounting for 360° wrap
        diff = (last_deg - first_deg) % 360
        if diff > 180:
            # Shortest arc crosses the 0° boundary
            arc_degrees = np.linspace(last_deg, first_deg + 360, num=100) % 360
        else:
            # Shortest arc is continuous
            arc_degrees = np.linspace(first_deg, last_deg, num=100)

        arc_radians = np.deg2rad(arc_degrees)
        arc_radii = np.full_like(arc_radians, peak_rssi)

    print(f"Peak detected: {peak_rssi:.0f} dBm @ {peak_degree:.0f}° degrees")

    # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    fig, ax = plt.subplots(
        figsize=(SIZE_INCHES, SIZE_INCHES),
        dpi=DPI,
        subplot_kw={'projection': 'polar'}
    )

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    custom_offset_degrees = 27
    ax.set_theta_offset(np.deg2rad(custom_offset_degrees))

    # Circular x-axis (angular degree) labels every 15°, with bold for 45° intervals
    thetaticks = np.arange(0, 360, 15)
    ax.set_thetagrids(thetaticks, labels=[f"{x}°" for x in thetaticks])

    for tick, label in zip(thetaticks, ax.get_xticklabels()):
        if tick % 45 == 0:
            label.set_weight('bold')
            label.set_fontsize(11)
        else:
            # label.set_style('italic')
            label.set_fontsize(9)

    # Radial y-axis (RSSI strength) labels
    yticks = np.arange(Y_TICK_MIN, Y_TICK_MAX, 10)
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{y}" for y in yticks])

    rssi_max_plot = RSSI_MAX_PLOT_CONSTANT
    rssi_min_plot = RSSI_MIN_PLOT_CONSTANT

    # Autoscale radial y-axis peak is 80% of the polar plot limit
    if peak_rssi != -99:
        rssi_max_plot = rssi_min_plot + (peak_rssi - rssi_min_plot) * 1.2
        print(f"Plot boundaries: {rssi_max_plot:.0f} to {rssi_min_plot:.0f} dBm")

    ax.set_ylim(rssi_min_plot, rssi_max_plot)

    # Plot RSSI strength values for 360°
    ax.plot(theta, rssi, color='green', linewidth=0.7)
    ax.fill(theta, rssi, color='green', alpha=0.3)

    # Title with peak RSSI info in red font, csv file name at bottom
    title_text = "RSSI Strength"
    red_peak_text = f"(Peak: {peak_rssi:.0f}dBm @ {peak_degree:.1f}°)"
    file_text = f"{subtitle}"
    fig.text(0.32, 0.95, title_text, ha='center', fontsize=12, fontweight='bold')
    fig.text(0.45, 0.95, red_peak_text, ha='left', fontsize=12, fontweight='bold', color='red')
    fig.text(0.05, 0.03, file_text, ha='left', fontsize=8)

    # Draw peak indicator with red dashed line
    peak_rad = np.deg2rad(peak_degree)
    if peak_rssi < rssi_max_plot:
        # draw solid line from plot edge halfway to peak, then dashed line to peak
        halfway_peak = (peak_rssi - rssi_max_plot) / 2
        ax.plot([peak_rad, peak_rad], [peak_rssi, peak_rssi - halfway_peak], color='red', linestyle='--', linewidth=2)
        ax.plot([peak_rad, peak_rad], [peak_rssi - halfway_peak, rssi_max_plot], color='red', linestyle='-',
                linewidth=4)
    else:
        # default draw red line from center to plot edge
        ax.plot([peak_rad, peak_rad], [rssi_min_plot, peak_rssi], color='red', linestyle='--', linewidth=1)

    # Draw the red peak arc overlay at the peak radius line
    if len(peak_cluster) > 1:
        ax.plot(arc_radians, arc_radii, color='red', linewidth=1, linestyle='-')

    # Print peak RSSI outside plot edge, xytext has 20px outward offset
    ax.annotate(f"{peak_rssi:.0f} dBm",
                xy=(peak_rad, rssi_max_plot),
                xytext=(np.sin(peak_rad) * 20, np.cos(peak_rad) * 20),
                textcoords="offset points",
                color='red',
                ha='center',
                va='center',
                fontweight='bold',
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='red', alpha=0.8))

    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
    #plt.savefig(file_name, format='jpg', dpi=300, bbox_inches='tight')
    plt.savefig(file_name, format='jpg', dpi=DPI)


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
        plot_rssi_polar(df, rssi, theta, csv_name, file_path)
        print(f"plot time = {(time.time() - start_time):.2f} secs")
    else:
        print("Please enter a csv file")


if __name__ == "__main__":
    main()
