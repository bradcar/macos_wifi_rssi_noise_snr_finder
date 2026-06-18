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

# dBm bounds for clamping values and gridlines
RSSI_MAX_PLOT_CONSTANT = -20
RSSI_MIN_PLOT_CONSTANT = -99
Y_TICK_MAX = -10
Y_TICK_MIN = -90


def plot_rssi_polar(csv_file):
    df = pd.read_csv(csv_file)
    theta = np.deg2rad(df['degree'])
    rssi = df['rssi']

    # Detect peak RSSI, or mid of plateau of peaks (issue? maybe 0 to 359° wrap)
    valid_data = df[df['rssi'] > -98]
    if valid_data.empty:
        peak_rssi = -99.0
        peak_degree = 0
    else:
        max_rssi = valid_data['rssi'].max()
        peak_cluster = valid_data[valid_data['rssi'] == max_rssi]
        peak_rssi = float(max_rssi)
        peak_degree = float(peak_cluster['degree'].mean())
    print(f"Peak detected: {peak_rssi:.0f} dBm @ {peak_degree:.0f}° degrees")

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    # Circular grid layout
    yticks = np.arange(Y_TICK_MIN, Y_TICK_MAX, 10)
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{y}" for y in yticks])

    rssi_max_plot = RSSI_MAX_PLOT_CONSTANT
    rssi_min_plot = RSSI_MIN_PLOT_CONSTANT

    # Autoscale, peak is 80% of the polar plot limit
    if peak_rssi != -99:
        rssi_max_plot = rssi_min_plot + (peak_rssi - rssi_min_plot) * 1.2
        print(f"Plot boundaries: {rssi_max_plot:.0f} to {rssi_min_plot:.0f} dBm")

    ax.set_ylim(rssi_min_plot, rssi_max_plot)

    # Plot RSSI values for 360°
    ax.plot(theta, rssi, color='blue', linewidth=0.7)
    ax.fill(theta, rssi, color='blue', alpha=0.3)

    # Title with peak RSSI info in red font, csv file name at bottom
    title_text = "RSSI Strength"
    red_peak_text = f"(Peak: {peak_rssi:.0f}dBm @ {peak_degree}°)"
    file_text = f"{csv_file}"
    fig.text(0.32, 0.95, title_text, ha='center', fontsize=12, fontweight='bold')
    fig.text(0.45, 0.95, red_peak_text, ha='left', fontsize=12, fontweight='bold', color='red')
    fig.text(0.60, 0.03, file_text, ha='left', fontsize=8)

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


def main():
    print("Polar plot of RSSI strength at 360 degrees\n")
    print("Magnetic North is 0° degrees")
    if len(sys.argv) > 1:
        plot_rssi_polar(sys.argv[1])
    else:
        print("Please enter a csv file")


if __name__ == "__main__":
    main()
