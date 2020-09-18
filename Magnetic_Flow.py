from graphics.Graphics import setup, export
from graphics.Geometry import background, color, stroke, Line, line_width
import math
import random

# Some variables
height, width = 1000, 1000
grid_size = 100
border, mag_border = 50, 450
step_x, step_y = (width//grid_size), (height//grid_size)


# Particle class
class Particle:
    def __init__(self, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.frc_x = 0
        self.frc_y = 0
        self.lx, self.ly = self.x, self.y
        self.draw_stroke = True

    def update(self):

        self.x = self.x + self.frc_x
        self.y = self.y + self.frc_y

        self.vel_x = self.vel_x * 0.9
        self.vel_y = self.vel_y * 0.9

        self.x = self.x + self.vel_x
        self.y = self.y + self.vel_y

    def edges(self):
        if self.x <= 50 or self.x >= width-50 or self.y <= 50 or self.y >= height-50:
            self.draw_stroke = False
        else:
            self.draw_stroke = True

    def reset_force(self):
        self.frc_x = 0
        self.frc_y = 0

    def set_force(self, fx, fy):
        self.frc_x = self.frc_x + fx
        self.frc_y = self.frc_y + fy

    def set_last_pos(self):
        self.lx, self.ly = self.x, self.y

    def calculate_force(self, mx, my, mp):
        dy = mx - self.x
        dx = my - self.y
        angle = math.atan2(dy, dx) * mp
        sx = math.sin(angle)
        sy = math.cos(angle)
        return [sx, sy]

    def draw(self):
        if self.draw_stroke is not False:
            line_width(0.9)
            Line(self.lx, self.ly, self.x, self.y)
            stroke()


# Magnet Class
class magnet:
    def __init__(self, x, y, pole):
        self.x = x
        self.y = y
        self.p = pole


def draw():

    background(0.95, 0.95, 0.95, 1.0)
    color(0.0, 0.0, 0.0, 1.0)

    magnets = []
    my_particles = []
    num_magnets = random.randint(2, 8)
    sum_x, sum_y = 0, 0
    sums = 0

    print("Number of Magnets: " + str(num_magnets))

    for m in range(num_magnets):
        pole = 1
        if random.uniform(0, 1) < 0.5:
            pole = -1

        magnets.append(magnet(
                random.randint(100, width-100),
                random.randint(100, height-100),
                pole
        ))

    start_num = 360
    a = (math.pi*2)/start_num

    for x in range(100, width-100, (width-200)//1):
        for y in range(100, height-100, (height-200)//1):
            for i in range(start_num):
                xx = x + (math.sin(a*i)*250) + ((width-200)//2)
                yy = y + (math.cos(a*i)*250) + ((height-200)//2)
                vx = random.uniform(-1, 1)*0.5
                vy = random.uniform(-1, 1)*0.5
                my_particles.append(Particle(xx, yy, vx, vy))

    for p in my_particles:
        for t in range(1000):
            for m in magnets:
                sums = p.calculate_force(m.x, m.y, m.p*4)
                sum_x = sum_x + sums[0]
                sum_y = sum_y + sums[1]

            sum_x = sum_x / len(magnets)
            sum_y = sum_y / len(magnets)

            p.reset_force()
            p.set_force(sum_x, sum_y)
            p.update()
            p.edges()
            if t % 8 == 0:
                p.draw()
                p.set_last_pos()


def main():
    setup(width, height)
    draw()
    export()


if __name__ == '__main__':
    main()
