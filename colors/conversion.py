# algorithms that converts RGB to other color models

### Utilities
def get_rgb_tuple(hex: str) -> tuple: # convert hex to RGB
    if len(hex) != 6:
        raise Exception('Incorrect length')
    elif list(filter(lambda c: ord(c) > ord('g'), hex.lower())):
        raise Exception('Not a hex character')
    
    def hex_to_dec(hex: str) -> int: # converts hex to dec
        for char in range(6):
            if char%2:
                yield int(hex[char-1:char+1], 16)
    return tuple(hex_to_dec(hex))

def get_hex(rgb: tuple) -> str: # convert RGB to hex
    if len(rgb) != 3:
        raise Exception('Incorrect length')
    elif list(filter(lambda n: n > 255 or n < 0, rgb)):
        raise Exception('Values are not correct for RGB')
    
    hex_str = '#'
    for n in rgb:
        hex_str += hex(n).replace("0x","").upper().rjust(2,'0')
    return hex_str

hex1 = 'ff0000'
hex2 = 'FF00ff'
hex3 = 'ff010a'
assert(get_rgb_tuple(hex1) == (255, 0, 0))
assert(get_rgb_tuple(hex2) == (255, 0, 255))
assert(get_rgb_tuple(hex3) == (255, 1, 10))
dec1 = (11, 255, 1)
dec2 = (160, 16, 0)
assert(get_hex(dec1) == '#0BFF01')
assert(get_hex(dec2) == '#A01000')