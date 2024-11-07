# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT


def contains(rect_1, rect_2):
    return (
        rect_1[0] >= rect_2[0]
        and rect_1[0] + rect_1[2] <= rect_2[0] + rect_2[2]
        and rect_1[1] >= rect_2[1]
        and rect_1[1] + rect_1[3] <= rect_2[1] + rect_2[3]
    )


def line_points(x0, y0, x1, y1, w, d, vertices):
    dx = x1 - x0
    dy = y1 - y0

    # stuff to handle inter division always round down, when we really
    # want away from 0
    if dx == 0:
        mx = -((w + 1) // 2)
    else:
        if dy > 0:
            mx = -w * dy // d
        else:
            mx = -(w * dy // d)
    if dy == 0:
        my = (w + 1) // 2
    else:
        if dx > 0:
            my = -(-w * dx // d)
        else:
            my = w * dx // d

    vertices[0] = x0 + mx
    vertices[1] = y0 + my
    vertices[2] = x1 + mx
    vertices[3] = y1 + my
    vertices[4] = x1 - mx
    vertices[5] = y1 - my
    vertices[6] = x0 - mx
    vertices[7] = y0 - my


def bisect16(lst, val, n):
    while True:
        m = (len(lst) & ~7) >> 1
        l = lst[m:]
        v = l[0] | (l[1] << 8)
        if v == val:
            l = lst[m + 2 :]
            return l[0] | (l[1] << 8)
        if not m:
            return 0
        lst = lst[m:] if v < val else lst[:m]

def intersect_poly_rect(polygon, n, x, y, w, h):
    polygon = list(polygon)
    max_x = max(polygon[::2])
    min_x = min(polygon[::2])
    max_y = max(polygon[1::2])
    min_y = min(polygon[1::2])
    return (
        x < max_x
        and min_x < x + w
        and y < max_y
        and min_y < y + h
    )


def blit_argb16_rgb565(rgb_buf, w1: int, h1: int, s1: int, argb_buf, x: int, y: int, w2: int, h2: int, s2: int):
    for i in range(h2):
        y1 = y + i
        if y1 < 0:
            continue
        if y1 >= h1:
            break
        for j in range(w2):
            x1 = x + j
            if x1 < 0:
                continue
            if x1 >= w1:
                break
            argb16 = argb_buf.pixel(j, i)
            a = argb16 >> 12
            if a == 0:
                continue
            else:
                r1 = (argb16 & 0x0f00) >> 7
                g1 = (argb16 & 0x00f0) >> 2
                b1 = (argb16 & 0x000f) << 1
                if a != 0xf:
                    fade = 0x10 - a
                    rgb565 = rgb_buf.pixel(x1, y1)
                    rgb565 = (rgb565 >> 8) | ((rgb565 & 0xff) << 8)
                    r2 = rgb565 >> 11
                    g2 = (rgb565 & 0x00000_111111_00000) >> 5
                    b2 = rgb565 & 0x00000_000000_11111
                    r1 += (fade * r2) >> 4
                    g1 += (fade * g2) >> 4
                    b1 += (fade * b2) >> 4
                rgb565 = (r1 << 11) | (g1 << 5) | b1
                rgb565 = (rgb565 >> 8) | ((rgb565 & 0xff) << 8)
                rgb_buf.pixel(x1, y1, rgb565)

# replace with faster viper versions where available
try:
    from ._speedups import bisect16, line_points, intersect_poly_rect, blit_argb16_rgb565
except SyntaxError:
    pass
