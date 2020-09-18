import graphics.Config as config
from numpy import clip
from math import hypot, sqrt
from .Helpers import TWO_PI
from .Vector import Vector as vec2


# Circle class
class Circle:
    def __init__(self, x, y, r):
        self.context = config.Context
        self.pos = vec2([x, y])
        self.radius = r
        self.draw()

    def draw(self):
        self.context.arc(self.pos.x, self.pos.y, self.radius, 0, TWO_PI)

    def get_radius(self):
        return self.radius

    def get_position(self):
        return self.pos

    def set_position(self, _position):
        self.pos = _position


# Line class
class Line:
    def __init__(self, x1, y1, x2, y2, draw=True):
        self.context = config.Context
        self.p0 = vec2([x1, y1])
        self.p1 = vec2([x2, y2])
        self.id = None
        if draw:
            self.draw()

    def draw(self):
        self.context.move_to(self.p0.x, self.p0.y)
        self.context.line_to(self.p1.x, self.p1.y)

    def get_length(self):
        return sqrt((self.p1.x - self.p0.x)**2 + (self.p1.y - self.p0.y)**2)

    def set_id(self, id):
        self.id = id

    def get_lerp(self, _t):
        x = self.p0.x+(self.p1.x-self.p0.x)*_t
        y = self.p0.y+(self.p1.y-self.p0.y)*_t
        p = vec2([x, y])
        return p

    def get_direction(self):
        d = (self.p0 - self.p1) / self.get_length()
        return d * -1.0


# Particle class built on the Circle class
class Particle(Circle):
    def __init__(self, _x, _y, _r):
        Circle.__init__(self, _x, _y, _r)
        self.vel = vec2([0.0, 0.0])
        self.frc = vec2([0.0, 0.0])
        self.width = 1000
        self.height = 1000

    def update(self):
        self.vel += self.frc
        self.pos += self.vel

    def edges(self):
        if self.pos.x <= 0 or self.pos.x >= self.width:
            self.vel.x = self.vel.x * -1

        if self.pos.y <= 0 or self.pos.y >= self.height:
            self.vel.y = self.vel.y * -1

    def add_force(self, _x, _y, _amt, _limit):
        fx, fy = _x * _amt, _y * _amt
        fx, fy = clip(fx - self.vel.x, -_limit, _limit), clip(fy - self.vel.y, -_limit, _limit)
        self.frc.x += fx
        self.frc.y += fy


def circle_three_points(A, B, C):

    y_delta_a = B.y - A.y
    y_delta_a = B.x - A.x
    y_delta_b = C.y - B.y
    x_delta_b = C.x - B.x
    center = vec2([0.0, 0.0])

    a_slope = float(y_delta_a / y_delta_a)
    b_slope = float(y_delta_b / x_delta_b)
    center.x = (a_slope * b_slope * (A.y - C.y) + b_slope * (A.x + B.x) - a_slope * (B.x + C.x)) / (2.0 * (b_slope - a_slope))
    center.y = -1 * (center.x - (A.x + B.x) / 2.0) / a_slope + (A.y + B.y) / 2.0

    radius = hypot(center.x - A.x, center.y - A.y)
    return {'center': center, 'radius': radius}


def background(r, g, b, a):
    config.Context.set_source_rgba(r, g, b, a)
    config.Context.paint()


def color(r, g, b, a):
    config.Context.set_source_rgba(r, g, b, a)


def stroke():
    config.Context.stroke()


def fill():
    config.Context.fill()


def line_width(value):
    config.Context.set_line_width(value)


def set_line_cap(value):
    if value == "LINE_CAP_BUTT":
        config.Context.set_line_cap(0)
    elif value == "LINE_CAP_ROUND":
        config.Context.set_line_cap(1)
    elif value == "LINE_CAP_SQUARE":
        config.Context.set_line_cap(2)
    else:
        config.Context.set_line_cap(2)
