import graphics.Config as config
from graphics.Graphics import setup, export
from graphics.Geometry import Line, background, color, stroke
from graphics.Helpers import map
from graphics.Generators import NoiseLoop
import math
import random

width, height = 1000, 1000


def draw():
    background(0.95, 0.95, 0.95, 1.0)
    color(0, 0, 0, 1)

    grid_x, grid_y = 1, 1
    x_step, y_step = width//grid_x, height//grid_y
    x_offset, y_offset = x_step//2, y_step//2

    n_loop = []
    offset = []
    num_layers = 40
    s = (x_offset // num_layers)

    for xxx in range(grid_x):
        for yyy in range(grid_y):
            center_x = xxx * x_step + x_offset
            center_y = yyy * y_step + y_offset
            for layer in range(num_layers):
                offset = random.randint(0, 360)
                n_loop.append(NoiseLoop(map(layer, 0, num_layers, 1, 4), s*layer, s*layer+s))
                num_points = 360
                for i in range(num_points):
                    r = n_loop[layer].get_value(i)
                    x = r * math.cos(math.radians(i)) + center_x
                    y = r * math.sin(math.radians(i)) + center_y
                    # Think of a better way to do this
                    config.Context.line_to(x, y)
                config.Context.close_path()
                stroke()

                if layer != 0:
                    num_lines = map(layer, 0, num_layers, 16, 2)
                    num_points = 360 / num_lines
                    for i in range(int(num_points)):
                        r = n_loop[layer].get_value(i*num_lines+offset)
                        x = r * math.cos(math.radians(i*num_lines+offset)) + center_x
                        y = r * math.sin(math.radians(i*num_lines+offset)) + center_y

                        r = n_loop[layer-1].get_value(i*num_lines+offset)
                        xx = r * math.cos(math.radians(i*num_lines+offset)) + center_x
                        yy = r * math.sin(math.radians(i*num_lines+offset)) + center_y
                        Line(xx, yy, x, y)
                        stroke()


def main():
    setup(width, height)
    draw()
    export()


if __name__ == '__main__':
    main()
