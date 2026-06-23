# plot_rssi_polar_utils.py
"""
Polar plot of RSSI strength at 360° headings. Radar-style plot for analysis
of measured RSSI from directional antenna Yagi-Uda data.
Peak RSSI is detected and its value and heading are printed in the title.
Magnetic North is 0° degrees, East is 90° degrees.

Features:
- Runs on MacOS or Pi Zero 2 W
- lcd_jpg_generate flag - if True creates small 240px x 240px jpg for direct display on small color LCD
- Dark Mode created for testing and possible use for lcd jpg's.
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

# dBm bounds for clamping values and gridlines
RSSI_MAX_PLOT_CONSTANT = -20
RSSI_MIN_PLOT_CONSTANT = -99
Y_TICK_MAX = -10
Y_TICK_MIN = -90

LCD_PIXELS = 240
LCD_DPI = 100
LCD_SIZE_INCHES = LCD_PIXELS / LCD_DPI


def plot_rssi_polar(df, rssi, theta, subtitle, lcd_jpg_generate, file_name="plot.jpg"):
    # Detect all values at peak RSSI
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
        # Short arc crosses  if >180 then crosses 0°
        if diff > 180:
            arc_degrees = np.linspace(last_deg, first_deg + 360, num=100) % 360
        else:
            arc_degrees = np.linspace(first_deg, last_deg, num=100)

        arc_radians = np.deg2rad(arc_degrees)
        arc_radii = np.full_like(arc_radians, peak_rssi)

    print(f"Peak detected: {peak_rssi:.0f} dBm @ {peak_degree:.0f}° degrees")

    # Now that Peak(s) are known, set up the plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    dark_mode = False
    if not lcd_jpg_generate:
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    else:
        dark_mode = True
        fig, ax = plt.subplots(
            figsize=(LCD_SIZE_INCHES, LCD_SIZE_INCHES),
            dpi=LCD_DPI,
            subplot_kw={'projection': 'polar'}
        )

    if dark_mode:
        bg_color = '#000000'  # True black to block the backlight
        panel_color = '#121212'  # Dark charcoal for the active radar circle
        text_color = '#FFFFFF'  # White text labels
        y_label_color = 'cyan'
        grid_color = '#555555'  # Muted gray gridlines
    else:
        bg_color = '#FFFFFF'
        panel_color = '#FFFFFF'
        text_color = '#000000'
        y_label_color = 'blue'
        grid_color = '#CCCCCC'

    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(panel_color)

    # Orientate the angular direction of the plot
    ax.set_theta_direction(-1)
    # Shift the 0° degrees off EAST
    # ax.set_theta_zero_location("N")  # only 8 directions possible
    custom_offset_degrees = 135
    ax.set_theta_offset(np.deg2rad(custom_offset_degrees))

    # Circular x-axis (angular degree) labels every 15°, with bold for 45° intervals
    thetaticks = np.arange(0, 360, 15)
    ax.set_thetagrids(thetaticks, labels=[f"{x}°" for x in thetaticks])

    if not lcd_jpg_generate:
        font_adjust = 0
        label_pad = 7  # default
    else:
        font_adjust = 2
        ax.tick_params(axis='x', colors=text_color, pad=2)

    for tick, label in zip(thetaticks, ax.get_xticklabels()):
        if tick % 45 == 0:
            label.set_weight('bold')
            label.set_fontsize(11 - font_adjust)
        else:
            # label.set_style('italic')
            label.set_fontsize(9 - font_adjust)

    # Radial y-axis RSSI strength labels
    yticks = np.arange(Y_TICK_MIN, Y_TICK_MAX, 10)
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{y}" for y in yticks])
    if not lcd_jpg_generate:
        ax.tick_params(axis='y', labelsize=10, labelcolor='blue')
    else:
        ax.tick_params(axis='y', labelsize=9, labelcolor=y_label_color)

    rssi_max_plot = RSSI_MAX_PLOT_CONSTANT
    rssi_min_plot = RSSI_MIN_PLOT_CONSTANT

    # Autoscale radial y-axis peak is 80% of the polar plot limit
    if peak_rssi != -99:
        rssi_max_plot = rssi_min_plot + (peak_rssi - rssi_min_plot) * 1.2
        print(f"Plot boundaries: {rssi_max_plot:.0f} to {rssi_min_plot:.0f} dBm")

    ax.set_ylim(rssi_min_plot, rssi_max_plot)

    # Plot RSSI strength values for 360°
    if not lcd_jpg_generate:
        ax.plot(theta, rssi, color='green', linewidth=2.0)
    else:
        ax.plot(theta, rssi, color='green', linewidth=0.7)
    ax.fill(theta, rssi, color='green', alpha=0.7)

    # Title with peak RSSI info in red font, csv file name at bottom
    title_text = "RSSI Strength"
    red_peak_text = f"(Peak: {peak_rssi:.0f}dBm @ {peak_degree:.0f}°)"
    file_text = f"{subtitle}"
    if not lcd_jpg_generate:
        fig.text(0.32, 0.95, title_text, ha='center', fontsize=12, fontweight='bold')
        fig.text(0.45, 0.95, red_peak_text, ha='left', fontsize=12, fontweight='bold', color='red')
        fig.text(0.05, 0.03, file_text, ha='left', fontsize=8)
    else:
        # fig.text(0.01, 0.95, f"(Peak {peak_rssi:.0f} dBm)", ha='left', fontsize=9, fontweight='bold', color='red')
        # fig.text(0.63, 0.95, f"(Peak: {peak_degree:.0f}°)", ha='left', fontsize=9, fontweight='bold', color='red')
        fig.text(0.16, 0.95, f"(Peak {peak_rssi:.0f} dBm @ {peak_degree:.0f}°)", ha='left', fontsize=9,
                 fontweight='bold', color='red')
        fig.text(0.82, 0.02, f"RSSI", ha='left', color=text_color, fontsize=11, fontweight='bold')

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
    if not lcd_jpg_generate:
        peak_string = f"{peak_rssi:.0f} dBm"
        peak_offset = 20
    else:
        peak_string = f"{peak_rssi:.0f}"
        peak_offset = 5

    ax.annotate(peak_string,
                xy=(peak_rad, rssi_max_plot),
                xytext=(np.sin(peak_rad) * peak_offset, np.cos(peak_rad) * peak_offset),
                textcoords="offset points",
                color='red',
                ha='center',
                va='center',
                fontweight='bold',
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='red', alpha=0.8))

    plt.grid(True, linestyle='--', color=grid_color, alpha=0.6)

    if not lcd_jpg_generate:
        plt.show()
        plt.savefig(file_name, format='jpg', dpi=300, bbox_inches='tight')
    else:
        # reposition polar plot for LCD display, default [0.125, 0.1, 0.775, 0.8]
        ax.set_position([0.14, 0.1, 0.72, 0.75])
        plt.show()
        plt.savefig(file_name, format='jpg', dpi=LCD_DPI)
