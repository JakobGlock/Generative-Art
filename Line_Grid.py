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

    border = 50
    border_sQ = border*2
    num_lines = 18
    y_step = float((height-border_sQ)/num_lines)
    x_step = float((width-border_sQ)/num_lines)
    y_offset = y_step/2.0
    x_offset = x_step/2.0
    un_offset = 10
    my_lines = []

    for i in range(num_lines):
        for j in range(num_lines-1):
            if j == 0:
                p1 = vec2([
                    x_step*j+x_offset + random.uniform(-x_offset, x_offset) + border,
                    y_step*i+y_offset + random.uniform(-y_offset, y_offset) + border
                ])
                p2 = vec2([
                    x_step*(j+1)+x_offset + random.uniform(-x_offset, x_offset) + border,
                    y_step*i+y_offset + random.uniform(-y_offset, y_offset) + border
                ])
                my_lines.append(Line(p1[0], p1[1], p2[0], p2[1]))
            else:
                p1 = vec2([
                    my_lines[(j+(num_lines-1)*i)-1].p1[0],
                    my_lines[(j+(num_lines-1)*i)-1].p1[1]
                ])
                p2 = vec2([
                    x_step*(j+1)+x_offset + random.uniform(-x_offset, x_offset) + border,
                    y_step*i+y_offset + random.uniform(-y_offset, y_offset) + border
                ])
                my_lines.append(Line(p1[0], p1[1], p2[0], p2[1]))

    index = 0
    for i in range(num_lines):
        index = index + 1
        for j in range(num_lines-1):
            if i != 0:
                lerp_lines = int(map(i, 0, num_lines, 1, 12))+1
                for k in range(lerp_lines):
                    p0 = my_lines[(j+(num_lines-1)*(i-1))].get_lerp(math.pow(map(k, 0, lerp_lines-1, 0, 1), 1))
                    p1 = my_lines[(j+(num_lines-1)*i)].get_lerp(math.pow(map(k, 0, lerp_lines-1, 0, 1), 1))
                    Line(p0[0], p0[1], p1[0], p1[1]).draw()
                    stroke()

    for line in my_lines:
        line.draw()
        stroke()


def main():
    setup(width, height)
    draw()
    export()


# Call the main function
if __name__ == '__main__':
    main()
