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

@micropython.viper
def blit_argb16_rgb565(rgb_buf: ptr16, w1: int, h1: int, s1: int, argb_buf: ptr16, x: int, y: int, w2: int, h2: int, s2: int):
    rgb565: int = 0
    for i in range(h2):
        y1: int = y + i
        if y1 < 0:
            continue
        if y1 >= h1:
            break
        for j in range(w2):
            x1: int = x + j
            if x1 < 0:
                continue
            if x1 >= w1:
                break
            argb16: int = argb_buf[i * s2 + j]
            if argb16 == 0:
                continue
            else:
                a: int = argb16 >> 12
                r1: int = (argb16 & 0x0f00) >> 7
                g1: int = (argb16 & 0x00f0) >> 2
                b1: int = (argb16 & 0x000f) << 1
                if a != 0xf:
                    fade: int = 0x10 - a
                    rgb565 = rgb_buf[y1 * s1 + x1]
                    rgb565 = (rgb565 >> 8) | ((rgb565 & 0xff) << 8)
                    r2: int = rgb565 >> 11
                    g2: int = (rgb565 & 0b00000_111111_00000) >> 5
                    b2: int = rgb565 & 0b00000_000000_11111
                    r1 += (fade * r2) >> 4
                    g1 += (fade * g2) >> 4
                    b1 += (fade * b2) >> 4
                    print(hex(r1), hex(g1), hex(b1))
                rgb565 = (r1 << 11) | (g1 << 5) | b1
                if a != 0xf:
                    print(hex(rgb565))
                rgb565 = (rgb565 >> 8) | ((rgb565 & 0xff) << 8)
                rgb_buf[y1 * s1 + x1] = rgb565
