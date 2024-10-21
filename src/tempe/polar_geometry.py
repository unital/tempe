from array import array
from math import cos, sin, pi

from .geometry import RowGeometry


def polar_points(cx, cy, geometry):
    rows = [None] * len(geometry)
    row = 0
    for r, theta in geometry:
        buffer = array('h', [int(cx + r * cos(theta * pi / 180)), int(cy + r * sin(theta * pi / 180))])
        rows[row] = buffer
        row += 1
    return RowGeometry(rows)

def polar_point_arrays(cx, cy, geometry):
    rows = [None] * len(geometry)
    row = 0
    for points in geometry:
        buffer = array('h', bytearray(2*len(points)))
        for i in range(0, len(points), 2):
            r = points[i]
            theta = points[i+1] * pi / 180
            buffer[i] = int(cx + r * cos(theta))
            buffer[i + 1] = int(cy + r * sin(theta))
        rows[row] = buffer
        row += 1
    return RowGeometry(rows)


def polar_rects(cx, cy, geometry, *, decimation=8):
    rows = [None] * len(geometry)
    row = 0
    for r, theta, delta_r, delta_theta in geometry:
        r2 = r + delta_r
        n_steps = (abs(delta_theta * max(r, r2)) >> decimation) + 1
        buffer = array('h', bytearray(8*n_steps + 8))
        for i in range(n_steps + 1):
            current_theta = (theta + i * delta_theta // n_steps) * pi / 180
            buffer[2*i] = int(cx + r * cos(current_theta))
            buffer[2*i+1] = int(cy + r * sin(current_theta))
            buffer[-2*i-2] = int(cx + r2 * cos(current_theta))
            buffer[-2*i-1] = int(cy + r2 * sin(current_theta))
        rows[row] = buffer
        row += 1
    return RowGeometry(rows)


def polar_r_lines(cx, cy, geometry):
    rows = [None] * len(geometry)
    row = 0
    for r, theta, delta_r in geometry:
        r2 = r + delta_r
        theta *= (pi / 180)
        buffer = array('h', [
            int(cx + r * cos(theta)),
            int(cy + r * sin(theta)),
            int(cx + r2 * cos(theta)),
            int(cy + r2 * sin(theta)),
        ])
        rows[row] = buffer
        row += 1
    return RowGeometry(rows)


def polar_theta_lines(cx, cy, geometry, *, include_center=False, decimation=8):
    rows = [None] * len(geometry)
    row = 0
    for r, theta, delta_theta in geometry:
        n_steps = (abs(delta_theta * r) >> decimation) + 1
        buffer = array('h', bytearray(4*n_steps + 4 + 4 * include_center))
        for i in range(n_steps + 1):
            current_theta = (theta + i * delta_theta // n_steps) * pi / 180
            buffer[2*i] = int(cx + r * cos(current_theta))
            buffer[2*i+1] = int(cy + r * sin(current_theta))
        if include_center:
            buffer[-2] = cx
            buffer[-1] = cy
        rows[row] = buffer
        row += 1
    return RowGeometry(rows)


def polar_lines(cx, cy, geometry, *, include_center=False, decimation=8):
    rows = [None] * len(geometry)
    row = 0
    for r1, theta_1, r2, theta_2 in geometry:
        delta_theta = (theta_2 - theta_1)
        delta_r = (r2 - r1)
        n_steps = (abs(delta_theta * max(r, r2)) >> decimation) + 1
        buffer = array('h', bytearray(4*n_steps + 4 + 4 * include_center))
        for i in range(n_steps + 1):
            theta = (theta_1 + i * delta_theta // n_steps) * pi / 180
            r = r1 + (i * delta_r) // n_steps
            buffer[2*i] = int(cx + r * cos(theta))
            buffer[2*i+1] = int(cy + r * sin(theta))
        if include_center:
            buffer[-2] = cx
            buffer[-1] = cy
        rows[row] = buffer
        row += 1
    return RowGeometry(rows)
