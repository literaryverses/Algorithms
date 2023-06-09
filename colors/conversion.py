# algorithms that converts RGB to other color models

def html_to_rgb(hex: str) -> tuple: # convert hex to RGB
    if len(hex) != 6:
        raise Exception('Incorrect length')
    elif list(filter(lambda c: ord(c) > ord('g'), hex.lower())):
        raise Exception('Not a hex character')
    
    def hex_to_dec(hex: str) -> int: # converts hex to dec
        for char in range(6):
            if char%2:
                yield int(hex[char-1:char+1], 16)
    return tuple(hex_to_dec(hex))

def html_to_rgb(rgb: tuple) -> str: # convert RGB to HTML format
    if len(rgb) != 3:
        raise Exception('Incorrect length')
    elif list(filter(lambda n: n > 255 or n < 0, rgb)):
        raise Exception('Values are not correct for RGB')
    
    html_str = '#'
    for p in rgb:
        html_str += hex(p).replace("0x","").upper().rjust(2,'0')
    return html_str