from os import path, makedirs
from math import pi, hypot
from numpy import where, cross
from subprocess import call
from sys import platform
from .Vector import Vector as vec2
from .Vector import sub_vec, add_vec

# Useful constants
PI = pi
HALF_PI = PI/2
TWO_PI = pi*2


# Useful functions
# Map a value to a new range
def map(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = float(value - left_min) / float(left_span)
    return right_min + (value_scaled * right_span)


# Lerp between two points
def lerp(x1, y1, x2, y2, _amt):
    x = x1+(x2-x1)*_amt
    y = y1+(y2-y1)*_amt
    return vec2([x, y])


# Create a folder if it does not exist
def does_path_exist(folder_path):
    if not path.exists(folder_path):
        makedirs(folder_path)


# Same as range(), but uses floats, requires all arguments!
def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step


# Open a file or image
def open_file(f):
    opener = "open" if platform == "darwin" else "xdg-open"
    call([opener, f])


# Get distance between two points
def dist(x1, y1, x2, y2):
    d = hypot(x1 - x2, y1 - y2)
    return d


# Get length of a vector
def length(p):
    return hypot(p[0], p[1])


# Scalar projection on a point
def scalar_projection(p, a, b):
    ap = sub_vec(p, a)
    ab = sub_vec(b, a)
    ab.normalize()
    ab *= ap.dot(ab)
    point = add_vec(a, ab)
    return point


# Find the closest point, points should be an array of vec2
def find_closest_point(a, points):
    current = None
    shortest = None
    for p in points:
        d = dist(a.x, a.y, p.x, p.y)
        if current is None:
            current = d
            shortest = d

        if d < current:
            current = d
            shortest = p
    return shortest
