import graphics.Config as config
from graphics.Graphics import setup, export
from graphics.Geometry import Circle, background, color, stroke

width, height = 1000, 1000


def draw():
    # Draw stuff here
    background(0.95, 0.95, 0.95, 1.0)
    color(0, 0, 0, 1.0)
    Circle(width*0.5, height*0.5, 250)
    stroke()


def main():
    setup(width, height)
    draw()
    export()


if __name__ == '__main__':
    main()
