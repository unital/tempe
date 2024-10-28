"""Named web color lookup

This uses a hashing approach, so will give false positives.
"""
import array

# This module works by using a perfect hash of the names of the extended
# web colors into an array of ~325 colors (the _data array).  The hashing
# algorithm was generated by gperf and manually translated into Python.
# This approach vastly reduces the memory footprint of a lookup table of
# web colors even given the relative inefficiency of the hash.

# It may be possible to do slightly better, as "gray" and "grey" map to
# different entries in the current scheme, and it includes the basic web
# colors which have their own module.

_data = array.array(
    "H",
    b"\x07\xff\x00\x00\x84\x10\x00\x00\x84\x10\x04\x00\x00\x00\x04\x10"
    b"\xfb\xea\x00\x00\x07\xe0\x9a\x85\x00\x00\x00\x00\xfd\x20\xff\xbd"
    b"\x6c\x12\xd6\x9a\x97\x72\x00\x00\x6c\x12\xd6\x9a\xfc\xef\xfa\x20"
    b"\x36\x66\xec\x10\xdb\x7a\x07\xef\x00\x00\x00\x00\xfb\x08\x74\x33"
    b"\xf8\x1f\x03\x00\x00\x00\x74\x33\xfe\xa0\x46\xfa\x00\x00\xc6\x18"
    b"\x88\x00\x88\x11\x00\x00\x00\x00\x90\x1a\x00\x00\xe7\x3f\x2c\x4a"
    b"\x99\x99\x00\x00\x00\x00\xec\xaf\xff\x7c\xff\xda\x00\x10\xf8\x00"
    b"\xd5\xb1\xcc\x27\x80\x00\xff\x16\x00\x00\x00\x00\x80\x10\x1d\x95"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf8\x1f\x48\x10\xff\x7e"
    b"\xfc\x40\xfc\x0e\xff\xbc\x86\x7d\x7f\xe0\xb1\x04\xff\xd9\x8d\xd1"
    b"\xf7\xff\x00\x00\x53\x45\x00\x00\x00\x00\x00\x00\xbc\x21\x00\x00"
    b"\x24\x44\x00\x00\x00\x00\x61\x93\x00\x00\xdd\x23\x00\x11\xae\x3b"
    b"\xff\x1c\x00\x00\x97\xd2\xfd\xb8\xfe\x19\x00\x00\x00\x00\x00\x00"
    b"\xca\xeb\x3d\x8e\x00\x00\xff\x18\xf6\xf6\x07\xff\xef\xff\x18\xcd"
    b"\x00\x00\x8a\x22\x00\x00\xf5\x0b\x41\xf1\x6a\xd9\xae\xbc\x44\x16"
    b"\x00\x00\xba\xba\x43\x5c\x7f\xc0\x00\x00\x1c\x9f\xff\xfb\xdf\xff"
    b"\x7f\xfa\xaf\xe5\xdb\x72\x00\x00\x00\x00\xff\xdf\xff\xfd\xff\x59"
    b"\xef\x31\x00\x19\x6b\x4d\x00\x00\xad\x55\x00\x00\x6b\x4d\x00\x00"
    b"\xad\x55\x84\x00\x00\x1f\x00\x00\x00\x00\x7b\x5d\xc0\xb0\xef\x55"
    b"\xd5\xfa\x00\x00\x00\x00\xdc\xfb\xff\xdb\x00\x00\x00\x00\xd3\x43"
    b"\x00\x00\x00\x00\x07\xd3\x2a\x69\x00\x00\x00\x00\x00\x00\x2a\x69"
    b"\x00\x00\x00\x00\x00\x00\x89\x5c\x00\x00\x5c\xf3\x6c\x64\xa1\x45"
    b"\x00\x00\xf7\xbb\x04\x51\x00\x00\x00\x00\x00\x00\xec\x1d\x46\x99"
    b"\x00\x00\xdd\xd0\xbd\xad\xd8\x87\xff\x7a\xbc\x71\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\xef\xfd\x00\x00\xf8\x92\x00\x00\xfe\xf5\x00\x00"
    b"\x00\x00\xde\xfb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x64\xbd\x00\x00\x93\x7b\x00\x00\x00\x00\x00\x00\xae\xfc"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\xff\x5a\x00\x00\xfb\x56\x00\x00\xfe\xd7"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x7a\x00\x00\x00\x00"
    b"\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x66\x75\x00\x00\x00\x00\x00\x00\xff\xe0\x00\x00\x00\x00\x00\x00"
    b"\xef\xdf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x86\x7f\x9e\x66\x00\x00\x00\x00\x00\x00\xff\xdf\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\xf7\xbe\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xaf\x7d\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x05\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xdd",
)

_assoc_values = array.array(
    "H",
    b"P\x01\x07\x00,\x00\x03\x00\x0f\x00\x03\x00;\x00\x05\x00\x11\x00"
    b"\x03\x00P\x01\x8a\x00\x04\x00\x0f\x00%\x00\x0c\x005\x00\x88\x00"
    b"\x03\x00\x03\x00\n\x00@\x00(\x00l\x00\x17\x00o\x00P\x01\x08\x00"
    b"P\x01"
)


def _perf_hash(s):
    """Hash function that gives a unique value for each web color.
    """
    l = len(s)
    v = l
    for i in [0, 2, 5, 6, 7, 11, 12]:
        if i >= l or v >= 336:
            break
        c = max(0, min(len(_assoc_values) - 1, ord(s[i]) - 96))
        if i == 2:
            v += _assoc_values[c + 2]
        else:
            v += _assoc_values[c]
    return v


def color(name):
    """Return the RGB565 value for a web color, or 0x0000 if no match."""
    index = _perf_hash(name) - 10
    if 0 <= index < len(_data):
        return _data[index]
    else:
        return 0x0000