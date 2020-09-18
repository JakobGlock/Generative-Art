from graphics.Graphics import setup, export
from graphics.Geometry import Line, background, color, stroke
from graphics.Helpers import map
from graphics.Vector import Vector as vec2
import random
import math


# Some variables
width, height = 1000, 1000


# Main function
def draw():
    background(0.95, 0.95, 0.95, 1.0)
    color(0, 0, 0, 1)

    connector_lines = []

    num_lines_x = 20
    num_lines_y = 3
    x_step = float((width-100) // num_lines_x)
    y_step = float(height // num_lines_y)
    x_offset = (x_step // 2) + 50
    y_offset = y_step // 2

    for h in range(num_lines_y):
        for i in range(num_lines_x):
            x = x_step * i + x_offset
            y = y_step * h + y_offset
            yy = random.randint(25, 100)
            p0 = vec2([
                x + random.uniform(-(x_step//2)+10, (x_step//2)+10),
                random.uniform(y-50, y+50) + yy
            ])
            p1 = vec2([
                x + random.uniform(-(x_step//2)+10, (x_step//2)+10),
                random.uniform(y-50, y+50) - yy
            ])
            connector_lines.append(Line(p0[0], p0[1], p1[0], p1[1]))

            if i != 0:
                num_lines = 21
                l1 = i+num_lines_x*h
                l2 = (i+num_lines_x*h)+1

                while l2 == l1:
                    l2 = random.randint(0, len(connector_lines))

                for j in range(num_lines+1):
                    p0 = connector_lines[l1-1].get_lerp(math.pow(map(j, 0, num_lines, 0, 1), 1))
                    p1 = connector_lines[l2-1].get_lerp(math.pow(map(j, 0, num_lines, 0, 1), 1))
                    Line(p0[0], p0[1], p1[0], p1[1])
                    stroke()


def main():
    setup(width, height)
    draw()
    export()


# Call the main function
if __name__ == '__main__':
    main()
