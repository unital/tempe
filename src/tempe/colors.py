def rgb_to_rgb565(colors):
    rgb565_colors = []
    for color in colors:
        r, g, b = color
        bytes = (int(r * 0x1F) << 11) | (int(g * 0x3F) << 5) | int(b * 0x1F)
        rgb565_colors.append((bytes >> 8) | ((bytes & 0xFF) << 8))
    return rgb565_colors


def rgb444_to_rgb565(r, g, b):
    bytes = (r << 12) | (g << 7) | (b << 1)
    return (bytes >> 8) | ((bytes & 0xFF) << 8)


def rgb565(r, g, b):
    bytes = (int(r * 0x1F) << 11) | (int(g * 0x3F) << 5) | int(b * 0x1F)
    return (bytes >> 8) | ((bytes & 0xFF) << 8)


black = grey_0 = 0x0000
white = 0xFFFF
# grey_1 = rgb565(0b00010, 0b000100, 0b00010)
# grey_2 = rgb565(0b00100, 0b001000, 0b00100)
# grey_3 = rgb565(0b00110, 0b001100, 0b00110)
# grey_4 = rgb565(0b01000, 0b010000, 0b01000)
# grey_5 = rgb565(0b01010, 0b010100, 0b01010)
# grey_6 = rgb565(0b01100, 0b011000, 0b01100)
# grey_7 = rgb565(0b01110, 0b011100, 0b01110)
# grey_8 = rgb565(0b10000, 0b010000, 0b10000)
# grey_9 = rgb565(0b10010, 0b100100, 0b10010)
# grey_a = rgb565(0b10100, 0b101000, 0b10100)
# grey_b = rgb565(0b10110, 0b101100, 0b10110)
# grey_c = rgb565(0b11000, 0b110000, 0b11000)
# grey_d = rgb565(0b11010, 0b110100, 0b11010)
# grey_e = rgb565(0b11100, 0b111000, 0b11100)
# grey_f = rgb565(0b11110, 0b111100, 0b11110)
grey_1 = rgb444_to_rgb565(0x1, 0x1, 0x1)
grey_2 = rgb444_to_rgb565(0x2, 0x2, 0x2)
grey_3 = rgb444_to_rgb565(0x3, 0x3, 0x3)
grey_4 = rgb444_to_rgb565(0x4, 0x4, 0x4)
grey_5 = rgb444_to_rgb565(0x5, 0x5, 0x5)
grey_6 = rgb444_to_rgb565(0x6, 0x6, 0x6)
grey_7 = rgb444_to_rgb565(0x7, 0x7, 0x7)
grey_8 = rgb444_to_rgb565(0x8, 0x8, 0x8)
grey_9 = rgb444_to_rgb565(0x9, 0x9, 0x9)
grey_a = rgb444_to_rgb565(0xA, 0xA, 0xA)
grey_b = rgb444_to_rgb565(0xB, 0xB, 0xB)
grey_c = rgb444_to_rgb565(0xC, 0xC, 0xC)
grey_d = rgb444_to_rgb565(0xD, 0xD, 0xD)
grey_e = rgb444_to_rgb565(0xE, 0xE, 0xE)
grey_f = rgb444_to_rgb565(0xF, 0xF, 0xF)
