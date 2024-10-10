

def rgb_to_rgb565(colors):
    rgb565_colors = []
    for color in colors:
        r, g, b = color
        bytes = (int(r*0x1f) << 11) | (int(g*0x3f) << 5) | int(b*0x1f)
        rgb565_colors.append((bytes >> 8) | ((bytes & 0xff) << 8))
    return rgb565_colors
