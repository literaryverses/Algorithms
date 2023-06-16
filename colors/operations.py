# A collection of color schemes

primary = {'red': (255, 0, 0), # primary colors of light
           'green': (0, 255, 0),
           'blue': (0, 0, 255), }

def pastel(rgb: tuple) -> tuple: # returns pastel color
    rgb = list(rgb)
    for i,part in enumerate(rgb):
        rgb[i] = (part + 255)//2 # add white to each primary
    return tuple(rgb)