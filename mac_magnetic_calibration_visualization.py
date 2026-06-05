"""
Quick visualizer for Magnetometer LIS3MDL sensor Calibration Output on Rasberry Pi Zero 2 W
"""
import re
import matplotlib.pyplot as plt
from typing import List, Tuple

# Paste your console output from calibrate_lis3mdl_test.py into this LOG_DATA
LOG_DATA = """
59.6s remain, Raw: ( -37.8,  +12.4,  -88.1) -> Mapped: (-0.62, +0.26, -0.42)
59.2s remain, Raw: ( -40.9,   +9.9,  -85.8) -> Mapped: (+0.12, -0.07, -0.42)
58.8s remain, Raw: ( -21.5,  +12.1,  -99.4) -> Mapped: (+1.00, +0.48, -1.00)
58.3s remain, Raw: (  +5.9,  +13.2, -101.2) -> Mapped: (+1.00, +0.74, -0.98)
57.9s remain, Raw: ( +42.2,  +22.4,  -59.2) -> Mapped: (+1.00, +0.35, +1.00)
57.5s remain, Raw: ( +24.5,   -1.3,  -16.7) -> Mapped: (+0.58, -0.87, +1.00)
57.1s remain, Raw: ( -14.5,  +36.6,  -10.5) -> Mapped: (-0.30, +1.00, +0.88)
56.7s remain, Raw: ( -40.9,  +49.8,  -54.1) -> Mapped: (-0.89, +0.78, -0.02)
56.3s remain, Raw: ( -31.1,  +26.8,  -92.7) -> Mapped: (-0.67, +0.01, -0.82)
55.8s remain, Raw: ( -28.4,  -25.7,  -71.5) -> Mapped: (-0.61, -1.00, -0.38)
55.4s remain, Raw: ( -37.6,  -22.7,  -39.1) -> Mapped: (-0.81, -0.86, +0.29)
55.0s remain, Raw: ( -40.7,   -4.7,  -21.2) -> Mapped: (-0.88, -0.44, +0.65)
54.6s remain, Raw: ( -29.0,  -28.6,  -38.6) -> Mapped: (-0.62, -1.00, +0.30)
54.2s remain, Raw: ( -17.0,   +2.7,  -98.8) -> Mapped: (-0.35, -0.21, -0.95)
53.8s remain, Raw: ( -15.6,  +62.4,  -59.4) -> Mapped: (-0.32, +1.00, -0.13)
53.4s remain, Raw: ( -25.7,   +5.5,   -5.8) -> Mapped: (-0.55, -0.20, +0.97)
52.9s remain, Raw: ( -17.2,  -29.4,  -27.7) -> Mapped: (-0.36, -0.94, +0.52)
52.5s remain, Raw: ( +20.8,  -28.3,  -42.4) -> Mapped: (+0.50, -0.87, +0.22)
52.1s remain, Raw: ( +37.1,  -10.9,  -61.8) -> Mapped: (+0.86, -0.51, -0.18)
51.7s remain, Raw: ( +43.1,  +10.7,  -60.1) -> Mapped: (+1.00, -0.07, -0.15)
51.3s remain, Raw: ( +42.3,  +22.9,  -48.1) -> Mapped: (+0.98, +0.19, +0.10)
50.9s remain, Raw: ( +41.5,  +24.0,  -54.3) -> Mapped: (+0.96, +0.21, -0.03)
50.4s remain, Raw: ( +42.0,  +13.0,  -63.8) -> Mapped: (+0.97, -0.02, -0.22)
50.0s remain, Raw: ( +40.6,   -1.5,  -40.6) -> Mapped: (+0.94, -0.32, +0.25)
49.6s remain, Raw: ( +43.9,  +16.7,  -50.6) -> Mapped: (+1.00, +0.06, +0.05)
49.2s remain, Raw: ( +37.3,   +5.6,  -74.5) -> Mapped: (+0.85, -0.17, -0.44)
48.8s remain, Raw: ( +38.0,   -9.6,  -59.8) -> Mapped: (+0.87, -0.49, -0.14)
48.4s remain, Raw: ( +40.8,   +7.8,  -68.4) -> Mapped: (+0.93, -0.13, -0.32)
48.0s remain, Raw: ( +40.9,  +26.7,  -48.5) -> Mapped: (+0.93, +0.26, +0.09)
47.5s remain, Raw: ( +37.0,  +35.6,  -47.4) -> Mapped: (+0.85, +0.45, +0.11)
47.1s remain, Raw: ( -10.3,  +62.2,  -42.8) -> Mapped: (-0.21, +1.00, +0.21)
46.7s remain, Raw: ( -56.6,  +23.7,  -35.4) -> Mapped: (-1.00, +0.20, +0.36)
46.3s remain, Raw: ( -46.3,  -14.0,  -29.0) -> Mapped: (-0.77, -0.57, +0.49)
45.9s remain, Raw: ( -30.8,  -34.5,  -49.2) -> Mapped: (-0.46, -1.00, +0.08)
45.5s remain, Raw: (  -6.8,  -38.7,  -61.2) -> Mapped: (+0.01, -1.00, -0.17)
45.1s remain, Raw: ( +19.5,  -32.8,  -60.8) -> Mapped: (+0.52, -0.88, -0.16)
44.6s remain, Raw: ( +38.7,  -11.0,  -40.6) -> Mapped: (+0.90, -0.45, +0.26)
44.2s remain, Raw: ( +44.7,  +10.3,  -48.3) -> Mapped: (+0.99, -0.03, +0.10)
43.8s remain, Raw: ( +36.0,  +38.4,  -58.4) -> Mapped: (+0.83, +0.53, -0.11)
43.4s remain, Raw: ( -17.1,  +62.7,  -58.9) -> Mapped: (-0.20, +0.99, -0.12)
43.0s remain, Raw: ( -54.6,  +35.6,  -52.9) -> Mapped: (-0.93, +0.46, +0.00)
42.6s remain, Raw: ( -52.9,   -8.1,  -60.5) -> Mapped: (-0.89, -0.40, -0.16)
42.2s remain, Raw: ( -36.1,  -28.6,  -56.7) -> Mapped: (-0.56, -0.80, -0.08)
41.7s remain, Raw: (  -4.8,  -37.0,  -59.5) -> Mapped: (+0.04, -0.96, -0.13)
41.3s remain, Raw: ( +30.1,  -21.2,  -62.4) -> Mapped: (+0.71, -0.66, -0.19)
40.9s remain, Raw: ( +42.1,   +2.4,  -61.6) -> Mapped: (+0.95, -0.19, -0.18)
40.5s remain, Raw: ( +42.2,  +13.8,  -62.4) -> Mapped: (+0.95, +0.03, -0.20)
40.1s remain, Raw: ( +25.2,  -24.1,  -66.3) -> Mapped: (+0.62, -0.71, -0.28)
39.7s remain, Raw: (  -4.2,  -34.1,  -66.5) -> Mapped: (+0.05, -0.91, -0.28)
39.3s remain, Raw: ( -37.3,  -21.4,  -65.5) -> Mapped: (-0.59, -0.66, -0.26)
38.8s remain, Raw: ( -56.0,  +11.6,  -64.5) -> Mapped: (-0.95, -0.01, -0.24)
38.4s remain, Raw: ( -44.6,   +4.4,  -82.5) -> Mapped: (-0.73, -0.16, -0.61)
38.0s remain, Raw: (  -1.7,  -12.1,  -94.2) -> Mapped: (+0.10, -0.48, -0.85)
37.6s remain, Raw: ( +13.8,   +5.3,  -96.6) -> Mapped: (+0.40, -0.14, -0.90)
37.2s remain, Raw: (  +6.4,  +18.4,  -98.2) -> Mapped: (+0.26, +0.12, -0.93)
36.8s remain, Raw: ( +14.1,  +33.2,  -92.3) -> Mapped: (+0.40, +0.41, -0.81)
36.3s remain, Raw: ( -20.6,  +58.7,  -72.9) -> Mapped: (-0.26, +0.91, -0.41)
35.9s remain, Raw: ( -53.0,  +36.3,  -57.9) -> Mapped: (-0.89, +0.47, -0.10)
35.5s remain, Raw: ( -26.3,  +60.9,  -62.7) -> Mapped: (-0.37, +0.95, -0.20)
35.1s remain, Raw: ( +33.4,  +41.0,  -65.0) -> Mapped: (+0.78, +0.56, -0.25)
34.7s remain, Raw: ( +41.9,   +1.8,  -63.5) -> Mapped: (+0.94, -0.21, -0.22)
34.3s remain, Raw: ( +35.0,  -17.1,  -59.8) -> Mapped: (+0.81, -0.58, -0.14)
33.9s remain, Raw: (  -6.8,  -35.2,  -65.0) -> Mapped: (+0.00, -0.93, -0.25)
33.4s remain, Raw: ( -49.3,   -6.2,  -67.2) -> Mapped: (-0.82, -0.36, -0.29)
33.0s remain, Raw: ( -55.3,  +14.6,  -64.1) -> Mapped: (-0.93, +0.05, -0.23)
32.6s remain, Raw: ( -53.7,  +33.1,  -61.2) -> Mapped: (-0.90, +0.41, -0.17)
32.2s remain, Raw: ( -11.5,  +62.4,  -62.5) -> Mapped: (-0.09, +0.98, -0.20)
31.8s remain, Raw: ( +18.6,  +56.4,  -55.3) -> Mapped: (+0.49, +0.86, -0.05)
31.4s remain, Raw: ( +29.0,  +46.5,  -44.1) -> Mapped: (+0.69, +0.67, +0.18)
31.0s remain, Raw: ( +36.9,  +20.9,  -29.6) -> Mapped: (+0.84, +0.17, +0.48)
30.5s remain, Raw: ( +28.2,   -2.3,  -20.5) -> Mapped: (+0.68, -0.28, +0.67)
30.1s remain, Raw: ( +11.7,  -19.7,  -18.8) -> Mapped: (+0.36, -0.63, +0.70)
29.7s remain, Raw: (  -5.8,  -21.6,  -16.3) -> Mapped: (+0.02, -0.66, +0.76)
29.3s remain, Raw: ( -10.4,  -20.1,  -15.1) -> Mapped: (-0.07, -0.63, +0.78)
28.9s remain, Raw: ( -33.9,   -5.8,  -16.1) -> Mapped: (-0.52, -0.35, +0.76)
28.5s remain, Raw: ( -38.9,  +23.3,  -15.7) -> Mapped: (-0.62, +0.22, +0.77)
28.1s remain, Raw: ( -25.0,  +44.4,  -17.0) -> Mapped: (-0.35, +0.63, +0.74)
27.6s remain, Raw: ( -46.2,  +20.7,  -22.7) -> Mapped: (-0.76, +0.16, +0.62)
27.2s remain, Raw: ( -33.8,   -7.0,  -17.9) -> Mapped: (-0.52, -0.38, +0.72)
26.8s remain, Raw: ( -22.2,  -21.3,  -20.6) -> Mapped: (-0.30, -0.66, +0.67)
26.4s remain, Raw: (  -9.8,  -25.4,  -20.3) -> Mapped: (-0.06, -0.74, +0.67)
26.0s remain, Raw: (  +3.0,  -25.3,  -20.0) -> Mapped: (+0.19, -0.74, +0.68)
25.6s remain, Raw: ( +23.9,   +1.5,  -13.8) -> Mapped: (+0.59, -0.21, +0.81)
25.2s remain, Raw: (  +5.2,  +43.8,  -14.2) -> Mapped: (+0.23, +0.62, +0.80)
24.7s remain, Raw: ( -26.0,  +57.2,  -32.4) -> Mapped: (-0.37, +0.88, +0.42)
24.3s remain, Raw: ( -45.7,  +25.7,  -86.1) -> Mapped: (-0.75, +0.26, -0.68)
23.9s remain, Raw: ( -17.0,   -1.9, -100.1) -> Mapped: (-0.20, -0.28, -0.97)
23.5s remain, Raw: ( +12.8,  -18.2,  -85.0) -> Mapped: (+0.38, -0.60, -0.66)
23.1s remain, Raw: ( +24.9,  -13.9,  -77.8) -> Mapped: (+0.61, -0.51, -0.51)
22.7s remain, Raw: ( +38.3,   -7.1,  -45.0) -> Mapped: (+0.87, -0.38, +0.16)
22.2s remain, Raw: ( +40.2,   -2.1,  -63.8) -> Mapped: (+0.91, -0.28, -0.22)
21.8s remain, Raw: ( +24.0,  -27.0,  -64.3) -> Mapped: (+0.60, -0.77, -0.23)
21.4s remain, Raw: ( +10.8,  -34.2,  -50.5) -> Mapped: (+0.34, -0.91, +0.05)
21.0s remain, Raw: ( -11.4,  -25.8,  -82.5) -> Mapped: (-0.09, -0.75, -0.61)
20.6s remain, Raw: ( -24.6,  +55.7,  -70.7) -> Mapped: (-0.34, +0.85, -0.37)
20.2s remain, Raw: ( -28.0,  +34.1,  -14.5) -> Mapped: (-0.41, +0.43, +0.79)
19.8s remain, Raw: ( -11.8,  -34.8,  -61.1) -> Mapped: (-0.09, -0.92, -0.17)
19.3s remain, Raw: (  -4.1,  -21.9,  -87.0) -> Mapped: (+0.05, -0.67, -0.70)
18.9s remain, Raw: (  +1.2,  +21.4, -101.7) -> Mapped: (+0.16, +0.18, -1.00)
18.5s remain, Raw: ( -44.9,  -16.8,  -60.7) -> Mapped: (-0.73, -0.57, -0.15)
18.1s remain, Raw: ( -39.3,  -20.2,  -38.5) -> Mapped: (-0.63, -0.64, +0.30)
17.7s remain, Raw: ( -28.3,   -0.2,  -12.4) -> Mapped: (-0.41, -0.25, +0.84)
17.3s remain, Raw: (  -9.0,  +36.6,  -11.0) -> Mapped: (-0.04, +0.48, +0.87)
16.9s remain, Raw: ( +13.1,  +53.1,  -72.6) -> Mapped: (+0.39, +0.80, -0.39)
16.4s remain, Raw: ( +42.1,   +4.0,  -64.5) -> Mapped: (+0.95, -0.16, -0.23)
16.0s remain, Raw: ( +23.0,  -25.8,  -49.9) -> Mapped: (+0.58, -0.75, +0.07)
15.6s remain, Raw: ( +10.0,  -22.8,  -25.6) -> Mapped: (+0.33, -0.69, +0.57)
15.2s remain, Raw: (  -2.5,   +7.2,   -6.8) -> Mapped: (+0.09, -0.10, +0.95)
14.8s remain, Raw: (  -7.9,  -23.7,  -19.6) -> Mapped: (-0.02, -0.71, +0.69)
14.4s remain, Raw: (  +3.3,  -34.4,  -68.1) -> Mapped: (+0.20, -0.91, -0.30)
14.0s remain, Raw: (  +4.3,   -4.8,  -98.0) -> Mapped: (+0.22, -0.34, -0.91)
13.5s remain, Raw: (  -8.2,  +27.4, -100.1) -> Mapped: (-0.03, +0.30, -0.95)
13.1s remain, Raw: ( -49.9,  +33.7,  -71.0) -> Mapped: (-0.83, +0.42, -0.36)
12.7s remain, Raw: ( -53.6,   -7.8,  -46.7) -> Mapped: (-0.90, -0.39, +0.14)
12.3s remain, Raw: ( -31.0,  -12.7,  -16.2) -> Mapped: (-0.46, -0.49, +0.76)
11.9s remain, Raw: (  -3.2,  -13.8,  -13.0) -> Mapped: (+0.07, -0.51, +0.83)
11.5s remain, Raw: ( +14.4,  -22.8,  -26.1) -> Mapped: (+0.41, -0.69, +0.56)
11.1s remain, Raw: ( +30.5,  -21.0,  -46.5) -> Mapped: (+0.72, -0.65, +0.14)
10.6s remain, Raw: ( +41.8,  +18.2,  -48.9) -> Mapped: (+0.94, +0.12, +0.09)
10.2s remain, Raw: ( +32.1,  +21.2,  -27.5) -> Mapped: (+0.75, +0.17, +0.53)
 9.8s remain, Raw: ( -25.8,  +58.2,  -39.4) -> Mapped: (-0.36, +0.90, +0.29)
 9.4s remain, Raw: ( -50.0,   +2.8,  -34.0) -> Mapped: (-0.83, -0.19, +0.40)
 9.0s remain, Raw: ( -41.1,   +2.9,  -20.3) -> Mapped: (-0.66, -0.18, +0.68)
 8.6s remain, Raw: (  +6.6,  +33.8,  -11.3) -> Mapped: (+0.26, +0.42, +0.86)
 8.1s remain, Raw: ( +34.2,  +31.2,  -33.1) -> Mapped: (+0.79, +0.37, +0.42)
 7.7s remain, Raw: ( +43.0,   +5.5,  -60.6) -> Mapped: (+0.96, -0.13, -0.15)
 7.3s remain, Raw: ( +30.6,  -22.3,  -48.9) -> Mapped: (+0.72, -0.68, +0.09)
 6.9s remain, Raw: (  +4.2,  -24.9,  -21.8) -> Mapped: (+0.21, -0.73, +0.65)
 6.5s remain, Raw: ( -23.5,   -4.4,  -10.2) -> Mapped: (-0.32, -0.33, +0.88)
 6.1s remain, Raw: ( -38.8,   +6.9,  -16.9) -> Mapped: (-0.62, -0.11, +0.75)
 5.7s remain, Raw: ( -42.1,  -19.2,  -52.5) -> Mapped: (-0.68, -0.62, +0.02)
 5.2s remain, Raw: ( -16.5,  -15.2,  -89.0) -> Mapped: (-0.19, -0.54, -0.73)
 4.8s remain, Raw: (  +2.8,  +15.2,  -98.7) -> Mapped: (+0.19, +0.06, -0.93)
 4.4s remain, Raw: (  +1.6,  -22.8,  -82.2) -> Mapped: (+0.16, -0.69, -0.59)
 4.0s remain, Raw: ( +15.6,  -28.5,  -64.8) -> Mapped: (+0.43, -0.80, -0.23)
 3.6s remain, Raw: ( +36.9,  -11.1,  -58.4) -> Mapped: (+0.85, -0.46, -0.10)
 3.2s remain, Raw: ( +44.1,  +10.0,  -53.4) -> Mapped: (+0.98, -0.04, +0.00)
 2.7s remain, Raw: ( +40.2,  +15.1,  -71.4) -> Mapped: (+0.91, +0.06, -0.37)
 2.3s remain, Raw: ( +23.7,   -2.5,  -89.1) -> Mapped: (+0.59, -0.29, -0.73)
 1.9s remain, Raw: (  -2.1,  -34.7,  -66.2) -> Mapped: (+0.09, -0.92, -0.26)
 1.5s remain, Raw: ( -42.7,   -8.5,  -75.4) -> Mapped: (-0.69, -0.41, -0.45)
 1.1s remain, Raw: ( -40.6,  +50.3,  -60.4) -> Mapped: (-0.65, +0.74, -0.14)
 0.7s remain, Raw: (  +5.0,  +60.2,  -43.0) -> Mapped: (+0.23, +0.94, +0.21)
 0.3s remain, Raw: ( +38.5,  +20.6,  -34.7) -> Mapped: (+0.88, +0.16, +0.38)
"""


def parse_log_data(text: str) -> Tuple[List[List[float]], List[List[float]]]:
    """
    Uses Regular Expressions to parse raw X,Y,Z vectors and
    calibrated/mapped X,Y,Z vectors out of the text logs.
    """
    raw_points = []
    mapped_points = []

    # Find patterns like "Raw: ( x, y, z) -> Mapped: (x, y, z)"
    pattern = r"Raw:\s*\(\s*([^,]+),\s*([^,]+),\s*([^\)]+)\)\s*->\s*Mapped:\s*\(\s*([^,]+),\s*([^,]+),\s*([^\)]+)\)"

    for line in text.strip().split("\n"):
        match = re.search(pattern, line)
        if match:
            # Extract Raw coordinates
            rx, ry, rz = map(float, match.group(1, 2, 3))
            raw_points.append([rx, ry, rz])

            # Extract Calibrated/Mapped coordinates
            mx, my, mz = map(float, match.group(4, 5, 6))
            mapped_points.append([mx, my, mz])

    return raw_points, mapped_points


def main():
    raw_data, mapped_data = parse_log_data(LOG_DATA)

    if not raw_data:
        print("Error: Could not parse any vectors out of the provided log text.")
        return

    # Unzip coordinates into individual X, Y, Z lists
    rx, ry, rz = zip(*raw_data)
    mx, my, mz = zip(*mapped_data)

    # Configure a side-by-side 3D figure layout
    fig = plt.figure(figsize=(14, 6))
    fig.suptitle(
        "Magnetometer Hard-Iron Distortion Transformation",
        fontsize=16,
        fontweight="bold",
    )

    # -----------------------------------------------------------------
    # LEFT AXIS: Uncalibrated Raw Data (Off-center Ellipsoid)
    # -----------------------------------------------------------------
    ax1 = fig.add_subplot(121, projection="3d")
    scatter1 = ax1.scatter(
        rx, ry, rz, c=rz, cmap="coolwarm", s=25, edgecolor="k", alpha=0.8
    )
    ax1.set_title("BEFORE: Raw Distorted Data", fontsize=12, pad=10)
    ax1.set_xlabel("Raw X (µT)")
    ax1.set_ylabel("Raw Y (µT)")
    ax1.set_zlabel("Raw Z (µT)")
    fig.colorbar(
        scatter1, ax=ax1, label="Z Axis Intensity Vector", shrink=0.6, pad=0.1
    )

    # Set uniform aspect limits for the raw data to showcase true geometric distortion
    max_range = max(max(rx) - min(rx), max(ry) - min(ry), max(rz) - min(rz)) / 2.0
    mid_x = (max(rx) + min(rx)) / 2.0
    mid_y = (max(ry) + min(ry)) / 2.0
    mid_z = (max(rz) + min(rz)) / 2.0
    ax1.set_xlim(mid_x - max_range, mid_x + max_range)
    ax1.set_ylim(mid_y - max_range, mid_y + max_range)
    ax1.set_zlim(mid_z - max_range, mid_z + max_range)

    # -----------------------------------------------------------------
    # RIGHT AXIS: Mapped Normal Data (Centered Unit Sphere)
    # -----------------------------------------------------------------
    ax2 = fig.add_subplot(122, projection="3d")
    scatter2 = ax2.scatter(
        mx, my, mz, c=mz, cmap="viridis", s=25, edgecolor="k", alpha=0.8
    )
    ax2.set_title("AFTER: Normalized Calibrated Sphere", fontsize=12, pad=10)
    ax2.set_xlabel("Mapped X")
    ax2.set_ylabel("Mapped Y")
    ax2.set_zlabel("Mapped Z")
    fig.colorbar(
        scatter2,
        ax=ax2,
        label="Normalized Altitude Vector",
        shrink=0.6,
        pad=0.1,
    )

    # Force a strict normalized view layout bounding box from -1 to +1
    ax2.set_xlim(-1.1, 1.1)
    ax2.set_ylim(-1.1, 1.1)
    ax2.set_zlim(-1.1, 1.1)

    # Draws alignment grid center lines through (0,0,0) for the calibrated sphere
    ax2.plot([-1.1, 1.1], [0, 0], [0, 0], "k--", alpha=0.3)
    ax2.plot([0, 0], [-1.1, 1.1], [0, 0], "k--", alpha=0.3)
    ax2.plot([0, 0], [0, 0], [-1.1, 1.1], "k--", alpha=0.3)

    plt.tight_layout()
    print("Displaying 3D graphs. You can click and drag plots to rotate...")
    plt.show()


if __name__ == "__main__":
    main()