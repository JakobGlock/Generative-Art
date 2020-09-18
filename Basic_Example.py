import graphics.Config as config
from graphics.Graphics import setup, export
from graphics.Geometry import background, color, Circle, stroke
from random import randint

width = 2000
height = 2000


def draw():
    background(0.95, 0.95, 0.95, 1.0)
    color(0, 0, 0, 0.01)

    for k in range(100):
        step = 100 / 4
        for j in range(0, width+100, 100):
            for i in range(0, height+100, 100):
                r = randint(-4, 4)
                offset_x = step / r if r != 0 else 0
                r = randint(-4, 4)
                offset_y = step / r if r != 0 else 0
                Circle(i+offset_x, j+offset_y, 10)
                stroke()


def main():
    # Pass optional overrides
    setup(width, height)
    draw()
    export()


if __name__ == '__main__':
    main()
