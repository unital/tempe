# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

import micropython


@micropython.viper
def line_points(x0: int, y0: int, x1: int, y1: int, w: int, d: int, vertices: ptr16):
    dx: int = x1 - x0
    dy: int = y1 - y0

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


@micropython.viper
def bisect16(lst: ptr16, val: int, k: int) -> int:
    n: int = 0
    k -= 1
    while True:
        m: int = (n + k) >> 1
        p: int = m << 1
        v: int = lst[p]
        if v == val:
            r = lst[p + 1]
            return r
        elif n >= m and k <= m:
            return 0
        elif v < val:
            n = m + 1
        else:
            k = m - 1

@micropython.viper
def intersect_poly_rect(polygon: ptr16, n: int, x: int, y: int, w: int, h: int) -> bool:
    min_x: int = 0x7fff
    max_x: int = -0x8000
    min_y: int = 0x7fff
    max_y: int = -0x8000
    x1: int = x + w
    y1: int = y + h
    for i in range(0, n, 2):
        px = polygon[i]
        py = polygon[i+1]
        if px < min_x:
            min_x = px
        if px > max_x:
            max_x = px
        if py < min_y:
            min_y = py
        if py > max_y:
            max_y = py

    return (
        x < max_x
        and min_x < x1
        and y < max_y
        and min_y < y1
    )
