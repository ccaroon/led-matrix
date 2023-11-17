__ACORN = {
    "width": 7,
    "height": 3,
    "bitmap": [
        0,1,0,0,0,0,0,
        0,0,0,1,0,0,0,
        1,1,0,0,1,1,1,
    ]
}

__BUNNIES = {
    "width": 8,
    "height": 4,
    "bitmap": [
        1,0,0,0,0,0,1,0,
        0,0,1,0,0,0,1,0,
        0,0,1,0,0,1,0,1,
        0,1,0,1,0,0,0,0,
    ]
}

__CONWAY = {
    "width": 7,
    "height": 9,
    "bitmap": [
        0,0,1,1,1,0,0,
        0,0,1,0,1,0,0,
        0,0,1,0,1,0,0,
        0,0,0,1,0,0,0,
        1,0,1,1,1,0,0,
        0,1,0,1,0,1,0,
        0,0,0,1,0,0,1,
        0,0,1,0,1,0,0,
        0,0,1,0,1,0,0,
    ]
}

__BLINKER = {
    "width": 3,
    "height": 3,
    "bitmap": [
        0,0,0,
        1,1,1,
        0,0,0
    ]
}

__GLIDER = {
    "width": 3,
    "height": 3,
    "bitmap": [
        0,1,0,
        0,0,1,
        1,1,1
    ]
}

__PULSAR = {
    "width": 15,
    "height": 15,
    "bitmap": [
        0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,
        0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,
        0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        1,1,1,0,0,1,1,0,1,1,0,0,1,1,1,
        0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,
        0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,
        0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,
        1,1,1,0,0,1,1,0,1,1,0,0,1,1,1,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,
        0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,
        0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,
    ]
}

__R_PENTOMINO = {
    "width": 3,
    "height": 3,
    "bitmap": [
        0,1,1,
        1,1,0,
        0,1,0
    ]
}

PATTERNS = {
    "acorn": __ACORN,
    # "blinker": __BLINKER,
    "bunnies": __BUNNIES,
    "conway": __CONWAY,
    # "glider": __GLIDER,
    # "pulsar": __PULSAR,
    "r-pentomino": __R_PENTOMINO
}
