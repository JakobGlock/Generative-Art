import cairo
import math
import random
import uuid
import numpy as np

#############################
# This script is a bit slow #
#############################

# Variables
fileFormat = 'PNG'
width, height = 1000, 1000
border = 50
centerX, centerY = width/2.0, height/2.0


# Line Class
class Line:
    def __init__(self, p0, dir, id, angle, connect):
        self.id = id
        self.p0 = p0
        self.p1 = p0
        self.dir = dir
        self.angle = angle
        self.connect = connect

    def draw(self, context):
        context.set_source_rgba(0, 0, 0, 1)
        context.move_to(self.p0[0], self.p0[1])
        context.line_to(self.p1[0], self.p1[1])
        context.stroke()

    def update(self):
        self.p1 = self.p1 + self.dir

    def changeDir(self, a):
        currentAngle = math.atan2(a[1], a[0]) * 180 / math.pi
        newDir = 90
        b = random.randint(0, 2)
        if b == 0:
            newDir = 0
        elif b == 1:
            newDir = 22.5 / 2.0
        else:
            newDir = -(22.5 / 2.0)
        angle = math.radians(currentAngle + newDir)
        dir = np.array([math.cos(angle), math.sin(angle)])
        self.dir = dir

    def edges(self):
        if self.p1[0] >= width-border or self.p1[0] < border or self.p1[1] < border or self.p1[1] >= height-border:
            return True

    def intersect(self, p2, p3):
        A1 = self.p1[1] - self.p0[1]
        B1 = self.p0[0] - self.p1[0]
        C1 = A1 * self.p0[0] + B1 * self.p0[1]
        A2 = p3[1] - p2[1]
        B2 = p2[0] - p3[0]
        C2 = A2 * p2[0] + B2 * p2[1]
        denom = A1 * B2 - A2 * B1

        if denom == 0:
            return False

        intersectX = (B2 * C1 - B1 * C2) / denom
        intersectY = (A1 * C2 - A2 * C1) / denom

        rx0 = (intersectX - self.p0[0]) / (self.p1[0] - self.p0[0])
        ry0 = (intersectY - self.p0[1]) / (self.p1[1] - self.p0[1])
        rx1 = (intersectX - p2[0]) / (p3[0] - p2[0])
        ry1 = (intersectY - p2[1]) / (p3[1] - p2[1])

        if(((rx0 >= 0 and rx0 <= 1) or (ry0 >= 0 and ry0 <= 1)) and ((rx1 >= 0 and rx1 <= 1) or (ry1 >= 0 and ry1 <= 1))):
            return True
        else:
            return False

    def getLength(self):
        dist = math.hypot(self.p0[0] - self.p1[0], self.p0[1] - self.p1[1])
        return dist

    def getLerp(self, _t):
        x = self.p0[0]+(self.p1[0]-self.p0[0])*_t
        y = self.p0[1]+(self.p1[1]-self.p0[1])*_t
        p = np.array([x, y])
        return p

    def getDirection(self):
        dir = (self.p0 - self.p1) / self.getLength()
        return dir * -1.0


# Main function
def main():
    context.set_source_rgba(0.95, 0.95, 0.95, 1.0)
    context.paint()

    walkers = []
    index = 0
    angle = (math.pi*2) / 90.0
    pos = np.array([100, 100])
    dir = np.array([1, 1])
    walkers.append(Line(pos, dir, 0, angle * 180.0 / math.pi, -1))
    lineLength = 20
    depth = -1

    for i in range(3000):
        if i != 0:
            if stopDrawing is True:
                connect = random.randint(0, i-1)
                pos = walkers[connect].getLerp(random.uniform(0.25, 0.75))
                dist = math.hypot(
                        walkers[i-1].p0[0] - centerX,
                        walkers[i-1].p0[1] - centerY
                )
                c = np.array([centerX, centerY])
                dir = ((walkers[i-1].p0 - c) / dist) * -1.0
                walkers.append(Line(pos, dir, i, angle * 180.0 / math.pi, connect))
                walkers[i].changeDir(walkers[i].dir)
                lineLength = 10
                index = index + 1
            else:
                pos = walkers[i-1].p1
                dir = walkers[i-1].dir
                walkers.append(Line(pos, dir, i, angle * 180 / math.pi, -1))
                walkers[i].changeDir(walkers[i-1].dir)

        if index > 400:
            break

        stopDrawing = False

        while walkers[i].getLength() < lineLength:
            walkers[i].update()

            for w in walkers:
                if walkers[i].id != w.id and walkers[i-1].id != w.id and walkers[i].connect != w.id:
                    if walkers[i].intersect(w.p0, w.p1) or walkers[i].edges():
                        stopDrawing = True
                        break

            if stopDrawing:
                break

        walkers[i].draw(context)


# Call the main function and save an image
if __name__ == '__main__':
    if fileFormat == 'PNG':
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)
        main()
        fileName = uuid.uuid4().hex[:8]
        surface.write_to_png("Images/Line_Walker/"+str(fileName)+".png")
    elif fileFormat == 'SVG':
        fileName = uuid.uuid4().hex[:8]
        surface = cairo.SVGSurface(
                "Images/Line_Walker/0-svg/"+str(fileName)+".svg",
                width,
                height
        )
        context = cairo.Context(surface)
        main()
        context.finish()
