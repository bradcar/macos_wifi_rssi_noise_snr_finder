"""
Quick visualizer for Magnetometer LIS3MDL sensor Calibration Output on Rasberry Pi Zero 2 W
"""
import re
import matplotlib.pyplot as plt
from typing import List, Tuple

# Paste your console output from calibrate_lis3mdl_test.py into this LOG_DATA
LOG_DATA = """
59.6s remain, Raw: ( -25.5,  +20.1,  -96.4) -> Mapped: (+0.66, +0.27, +0.11)
59.2s remain, Raw: ( -26.0,  +20.2,  -96.9) -> Mapped: (-0.54, +0.43, -0.61)
58.8s remain, Raw: ( -25.5,  +19.6,  -95.9) -> Mapped: (+0.67, -0.69, +0.80)
58.4s remain, Raw: ( -25.7,  +19.4,  -96.8) -> Mapped: (+0.26, -0.57, -0.27)
57.9s remain, Raw: ( -25.9,  +19.9,  -96.5) -> Mapped: (-0.20, +0.13, -0.02)
57.5s remain, Raw: ( -31.4,  +20.2,  -93.5) -> Mapped: (-1.00, +0.10, +1.00)
57.1s remain, Raw: ( +25.2,   +2.1,  -90.7) -> Mapped: (+1.00, -0.84, +1.00)
56.7s remain, Raw: ( +44.6,   +5.5,  -54.7) -> Mapped: (+1.00, -0.50, +1.00)
56.3s remain, Raw: ( +35.4,  +12.1,  -30.6) -> Mapped: (+0.76, +0.13, +1.00)
55.9s remain, Raw: ( +12.2,  +31.6,  -13.0) -> Mapped: (+0.18, +1.00, +0.97)
55.4s remain, Raw: ( -33.9,  +55.8,  -68.0) -> Mapped: (-0.99, +0.81, -0.30)
55.0s remain, Raw: ( -21.3,  -26.0,  -79.1) -> Mapped: (-0.54, -1.00, -0.56)
54.6s remain, Raw: ( +21.7,  -27.0,  -63.6) -> Mapped: (+0.46, -0.83, -0.20)
54.2s remain, Raw: ( +39.4,   -4.0,  -49.8) -> Mapped: (+0.88, -0.35, +0.12)
53.8s remain, Raw: (  +9.4,  +60.0,  -54.2) -> Mapped: (+0.18, +0.97, +0.02)
53.4s remain, Raw: ( -54.0,  +38.4,  -68.3) -> Mapped: (-1.00, +0.50, -0.31)
53.0s remain, Raw: ( -17.4,  +43.6,  -12.8) -> Mapped: (-0.22, +0.60, +0.97)
52.5s remain, Raw: ( +24.2,  +12.0,  -18.9) -> Mapped: (+0.60, -0.04, +0.80)
52.1s remain, Raw: ( +11.5,   -7.6,  -15.9) -> Mapped: (+0.35, -0.44, +0.87)
51.7s remain, Raw: ( +10.5,  -22.8,  -22.8) -> Mapped: (+0.33, -0.75, +0.71)
51.3s remain, Raw: (  -6.9,  -32.8,  -34.2) -> Mapped: (-0.02, -0.95, +0.45)
50.9s remain, Raw: ( -32.2,  -29.0,  -66.5) -> Mapped: (-0.51, -0.87, -0.28)
50.5s remain, Raw: ( -45.3,  -13.1,  -67.0) -> Mapped: (-0.77, -0.55, -0.29)
50.1s remain, Raw: ( -23.8,  +61.4,  -46.2) -> Mapped: (-0.35, +0.97, +0.18)
49.6s remain, Raw: ( +13.3,   +4.4,  -12.6) -> Mapped: (+0.38, -0.19, +0.94)
49.2s remain, Raw: ( +16.3,   -7.0,  -19.7) -> Mapped: (+0.44, -0.42, +0.78)
48.8s remain, Raw: ( +26.3,  -14.5,  -28.3) -> Mapped: (+0.64, -0.58, +0.59)
48.4s remain, Raw: ( +10.8,  -30.3,  -33.9) -> Mapped: (+0.33, -0.90, +0.46)
48.0s remain, Raw: ( -26.4,  -32.8,  -54.1) -> Mapped: (-0.40, -0.94, +0.00)
47.6s remain, Raw: ( -61.0,  -10.5,  -62.5) -> Mapped: (-1.00, -0.49, -0.19)
47.1s remain, Raw: ( -21.0,  -22.1,  -85.4) -> Mapped: (-0.24, -0.72, -0.71)
46.7s remain, Raw: ( +13.9,   +4.8,  -97.4) -> Mapped: (+0.42, -0.18, -0.98)
46.3s remain, Raw: ( +12.6,  +49.4,  -24.7) -> Mapped: (+0.39, +0.72, +0.67)
45.9s remain, Raw: ( -34.4,   +7.3,  -13.3) -> Mapped: (-0.50, -0.13, +0.81)
45.5s remain, Raw: ( -57.2,  +19.3,  -48.7) -> Mapped: (-0.93, +0.12, +0.06)
45.1s remain, Raw: ( -41.8,  -18.4,  -68.3) -> Mapped: (-0.64, -0.65, -0.36)
44.7s remain, Raw: ( +17.5,  -22.5,  -77.8) -> Mapped: (+0.49, -0.73, -0.56)
44.2s remain, Raw: ( +39.2,   +7.6,  -31.7) -> Mapped: (+0.90, -0.12, +0.42)
43.8s remain, Raw: (  -4.9,   +8.6,   -3.7) -> Mapped: (+0.06, -0.10, +1.00)
43.4s remain, Raw: ( -59.2,  +13.0,  -53.9) -> Mapped: (-0.97, -0.01, -0.06)
43.0s remain, Raw: ( -48.2,   +6.9,  -80.4) -> Mapped: (-0.76, -0.14, -0.62)
42.6s remain, Raw: ( -19.2,  -16.4,  -89.2) -> Mapped: (-0.21, -0.61, -0.81)
42.2s remain, Raw: ( +26.5,  -23.4,  -62.5) -> Mapped: (+0.65, -0.75, -0.24)
41.8s remain, Raw: ( +42.1,   +4.1,  -46.1) -> Mapped: (+0.95, -0.19, +0.10)
41.3s remain, Raw: ( +14.2,  +50.6,  -79.1) -> Mapped: (+0.42, +0.75, -0.59)
40.9s remain, Raw: ( -41.5,  -14.4,  -75.2) -> Mapped: (-0.63, -0.57, -0.51)
40.5s remain, Raw: (  +2.4,  -33.9,  -38.2) -> Mapped: (+0.20, -0.94, +0.27)
40.1s remain, Raw: (  -6.1,  -35.6,  -46.0) -> Mapped: (+0.04, -0.98, +0.10)
39.7s remain, Raw: ( +39.2,   -6.2,  -43.9) -> Mapped: (+0.90, -0.39, +0.15)
39.3s remain, Raw: ( +13.1,  +41.8,  -17.1) -> Mapped: (+0.40, +0.57, +0.71)
38.9s remain, Raw: ( -20.0,  +56.9,  -78.7) -> Mapped: (-0.22, +0.87, -0.59)
38.4s remain, Raw: ( -24.8,  -32.3,  -55.6) -> Mapped: (-0.31, -0.91, -0.08)
38.0s remain, Raw: (  +1.7,  -36.0,  -51.0) -> Mapped: (+0.19, -0.99, +0.02)
37.6s remain, Raw: ( +42.9,   +8.9,  -57.9) -> Mapped: (+0.97, -0.09, -0.13)
37.2s remain, Raw: ( +21.3,   +1.5,  -14.6) -> Mapped: (+0.56, -0.24, +0.77)
36.8s remain, Raw: ( +31.1,   +0.7,  -22.1) -> Mapped: (+0.74, -0.25, +0.61)
36.4s remain, Raw: (  -8.7,  -28.6,  -22.2) -> Mapped: (-0.01, -0.84, +0.61)
36.0s remain, Raw: ( -55.5,   -0.1,  -36.3) -> Mapped: (-0.90, -0.27, +0.32)
35.5s remain, Raw: ( -56.0,   -1.9,  -66.4) -> Mapped: (-0.91, -0.31, -0.30)
35.1s remain, Raw: ( -22.7,  -33.2,  -42.4) -> Mapped: (-0.27, -0.93, +0.19)
34.7s remain, Raw: ( +25.1,   -6.1,  -86.2) -> Mapped: (+0.63, -0.39, -0.71)
34.3s remain, Raw: (  +7.5,  -19.8,  -86.1) -> Mapped: (+0.30, -0.66, -0.71)
33.9s remain, Raw: (  +7.8,  -24.2,  -78.8) -> Mapped: (+0.30, -0.75, -0.56)
33.5s remain, Raw: ( -24.0,  +63.0,  -44.0) -> Mapped: (-0.30, +0.99, +0.16)
33.1s remain, Raw: ( -20.9,   -1.6,   -5.6) -> Mapped: (-0.24, -0.30, +0.95)
32.6s remain, Raw: ( +17.6,  -25.9,  -32.2) -> Mapped: (+0.49, -0.78, +0.40)
32.2s remain, Raw: ( +11.9,  -33.1,  -54.6) -> Mapped: (+0.38, -0.93, -0.06)
31.8s remain, Raw: ( -11.6,  -33.9,  -42.8) -> Mapped: (-0.07, -0.94, +0.18)
31.4s remain, Raw: (  +0.9,  -20.8,  -85.1) -> Mapped: (+0.17, -0.68, -0.69)
31.0s remain, Raw: (  -3.9,  +57.0,  -78.5) -> Mapped: (+0.08, +0.87, -0.55)
30.6s remain, Raw: ( -18.1,  +19.7,   -2.7) -> Mapped: (-0.19, +0.12, +1.00)
30.1s remain, Raw: (  +7.5,  -20.2,  -19.6) -> Mapped: (+0.30, -0.67, +0.65)
29.7s remain, Raw: ( -17.9,  -19.5,  -18.1) -> Mapped: (-0.19, -0.66, +0.68)
29.3s remain, Raw: (  -2.6,  -33.1,  -39.6) -> Mapped: (+0.10, -0.93, +0.24)
28.9s remain, Raw: (  +1.7,   -6.8,  -95.1) -> Mapped: (+0.19, -0.41, -0.90)
28.5s remain, Raw: ( -23.4,  +59.5,  -72.5) -> Mapped: (-0.29, +0.90, -0.41)
28.1s remain, Raw: (  -3.6,  +61.3,  -36.8) -> Mapped: (+0.09, +0.94, +0.31)
27.7s remain, Raw: ( +31.6,  +19.1,  -24.2) -> Mapped: (+0.75, +0.11, +0.57)
27.2s remain, Raw: (  -5.4,  -35.2,  -44.6) -> Mapped: (+0.05, -0.97, +0.16)
26.8s remain, Raw: ( -37.7,  -23.4,  -44.5) -> Mapped: (-0.56, -0.74, +0.16)
26.4s remain, Raw: ( -26.8,  -30.2,  -44.1) -> Mapped: (-0.35, -0.87, +0.17)
26.0s remain, Raw: ( +36.4,   -9.2,  -58.0) -> Mapped: (+0.84, -0.45, -0.11)
25.6s remain, Raw: (  +7.7,  +24.4,   -7.3) -> Mapped: (+0.30, +0.21, +0.91)
25.2s remain, Raw: ( -38.4,  +21.7,  -11.3) -> Mapped: (-0.57, +0.16, +0.83)
24.8s remain, Raw: ( -39.5,  +32.5,  -18.6) -> Mapped: (-0.59, +0.37, +0.68)
24.3s remain, Raw: ( -23.8,  +43.4,  -18.4) -> Mapped: (-0.30, +0.59, +0.68)
23.9s remain, Raw: ( +28.0,  +39.6,  -35.4) -> Mapped: (+0.68, +0.51, +0.34)
23.5s remain, Raw: ( +11.2,  -25.1,  -70.1) -> Mapped: (+0.37, -0.77, -0.36)
23.1s remain, Raw: ( +13.9,  -24.5,  -33.4) -> Mapped: (+0.42, -0.76, +0.38)
22.7s remain, Raw: ( +20.7,  -25.4,  -43.5) -> Mapped: (+0.55, -0.77, +0.18)
22.3s remain, Raw: ( +35.2,  +35.4,  -38.9) -> Mapped: (+0.82, +0.43, +0.27)
21.9s remain, Raw: ( -14.8,  -16.1,  -13.4) -> Mapped: (-0.13, -0.59, +0.78)
21.4s remain, Raw: ( -39.2,  +31.7,  -15.7) -> Mapped: (-0.59, +0.35, +0.74)
21.0s remain, Raw: ( +21.5,  +38.1,  -22.2) -> Mapped: (+0.56, +0.48, +0.61)
20.6s remain, Raw: ( +30.8,  -11.3,  -32.9) -> Mapped: (+0.74, -0.50, +0.39)
20.2s remain, Raw: ( -13.1,  -25.3,  -25.5) -> Mapped: (-0.09, -0.77, +0.54)
19.8s remain, Raw: (  +3.9,  -30.6,  -36.9) -> Mapped: (+0.23, -0.88, +0.31)
19.4s remain, Raw: ( +41.6,  +18.7,  -57.3) -> Mapped: (+0.94, +0.10, -0.10)
18.9s remain, Raw: ( +24.7,  +48.0,  -68.8) -> Mapped: (+0.62, +0.68, -0.33)
18.5s remain, Raw: ( -36.9,  +56.1,  -37.2) -> Mapped: (-0.54, +0.83, +0.30)
18.1s remain, Raw: ( -39.8,  +51.6,  -42.3) -> Mapped: (-0.60, +0.74, +0.20)
17.7s remain, Raw: ( +16.1,   -6.1,  -89.9) -> Mapped: (+0.46, -0.40, -0.76)
17.3s remain, Raw: ( +15.2,  -29.7,  -44.7) -> Mapped: (+0.44, -0.86, +0.15)
16.9s remain, Raw: ( -48.5,   -5.1,  -71.6) -> Mapped: (-0.76, -0.38, -0.39)
16.5s remain, Raw: ( -53.3,  +15.8,  -72.8) -> Mapped: (-0.85, +0.03, -0.41)
16.0s remain, Raw: ( -49.5,   -8.8,  -37.8) -> Mapped: (-0.78, -0.45, +0.29)
15.6s remain, Raw: ( -41.0,  -11.0,  -26.6) -> Mapped: (-0.62, -0.49, +0.52)
15.2s remain, Raw: ( -28.2,  +22.2,   -7.9) -> Mapped: (-0.38, +0.16, +0.89)
14.8s remain, Raw: (  -8.8,  +52.9,  -21.0) -> Mapped: (-0.01, +0.77, +0.63)
14.4s remain, Raw: ( +22.9,  +46.6,  -33.0) -> Mapped: (+0.59, +0.64, +0.39)
14.0s remain, Raw: ( +26.0,  +12.4,  -87.8) -> Mapped: (+0.65, -0.03, -0.71)
13.6s remain, Raw: ( +28.4,   +3.7,  -85.0) -> Mapped: (+0.69, -0.20, -0.66)
13.1s remain, Raw: ( +29.1,  -19.8,  -60.6) -> Mapped: (+0.70, -0.67, -0.17)
12.7s remain, Raw: ( +24.3,  +28.1,  -19.9) -> Mapped: (+0.61, +0.28, +0.65)
12.3s remain, Raw: ( -17.0,  +63.7,  -55.4) -> Mapped: (-0.17, +0.98, -0.06)
11.9s remain, Raw: ( +12.0,  +59.6,  -55.7) -> Mapped: (+0.38, +0.90, -0.07)
11.5s remain, Raw: ( +38.4,   +4.5,  -35.8) -> Mapped: (+0.88, -0.19, +0.33)
11.1s remain, Raw: (  -7.6,  -35.9,  -61.5) -> Mapped: (+0.01, -0.98, -0.18)
10.7s remain, Raw: ( -45.0,  -11.9,  -32.3) -> Mapped: (-0.70, -0.51, +0.40)
10.2s remain, Raw: ( -36.1,   +8.2,  -12.5) -> Mapped: (-0.53, -0.11, +0.80)
 9.8s remain, Raw: ( -14.1,  +22.9,   -5.2) -> Mapped: (-0.11, +0.17, +0.95)
 9.4s remain, Raw: (  +6.2,  +47.4,  -19.8) -> Mapped: (+0.27, +0.66, +0.66)
 9.0s remain, Raw: ( +31.2,  -17.5,  -46.9) -> Mapped: (+0.74, -0.62, +0.11)
 8.6s remain, Raw: ( -50.4,   -9.6,  -53.3) -> Mapped: (-0.80, -0.47, -0.02)
 8.2s remain, Raw: ( -55.6,  +34.2,  -45.2) -> Mapped: (-0.90, +0.40, +0.14)
 7.7s remain, Raw: ( -58.5,  +26.2,  -50.2) -> Mapped: (-0.95, +0.24, +0.04)
 7.3s remain, Raw: ( -17.5,  -32.9,  -49.2) -> Mapped: (-0.18, -0.92, +0.06)
 6.9s remain, Raw: ( +20.2,  -27.5,  -47.9) -> Mapped: (+0.54, -0.82, +0.09)
 6.5s remain, Raw: ( +40.5,  +22.7,  -48.5) -> Mapped: (+0.92, +0.17, +0.08)
 6.1s remain, Raw: ( +23.3,  +52.4,  -50.7) -> Mapped: (+0.59, +0.75, +0.03)
 5.7s remain, Raw: ( -17.2,  +64.3,  -48.3) -> Mapped: (-0.17, +0.99, +0.08)
 5.3s remain, Raw: ( -47.6,  +38.3,  -73.1) -> Mapped: (-0.75, +0.48, -0.42)
 4.8s remain, Raw: ( -20.0,   +8.0,   -7.6) -> Mapped: (-0.22, -0.12, +0.90)
 4.4s remain, Raw: ( -20.9,  -20.3,  -85.3) -> Mapped: (-0.24, -0.68, -0.66)
 4.0s remain, Raw: (  +6.3,  +37.2,  -96.4) -> Mapped: (+0.27, +0.45, -0.86)
 3.6s remain, Raw: (  -5.2,  -12.1,  -93.8) -> Mapped: (+0.05, -0.52, -0.81)
 3.2s remain, Raw: ( -19.0,  -25.8,  -26.2) -> Mapped: (-0.21, -0.79, +0.53)
 2.8s remain, Raw: ( -24.2,  +35.4,  -11.0) -> Mapped: (-0.30, +0.42, +0.84)
 2.3s remain, Raw: ( -19.0,  +40.0,  -95.2) -> Mapped: (-0.21, +0.51, -0.84)
 1.9s remain, Raw: ( -22.2,  -15.4,  -88.6) -> Mapped: (-0.27, -0.58, -0.71)
 1.5s remain, Raw: (  -6.2,  +33.2,  -98.9) -> Mapped: (+0.04, +0.37, -0.91)
 1.1s remain, Raw: ( +29.9,  +20.8,  -22.9) -> Mapped: (+0.72, +0.13, +0.60)
 0.7s remain, Raw: ( +27.0,  -17.4,  -69.6) -> Mapped: (+0.66, -0.62, -0.33)
 0.3s remain, Raw: ( +16.1,  +14.1,  -95.7) -> Mapped: (+0.46, +0.00, -0.85)
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