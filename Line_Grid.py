import cairo
import uuid
import random
import math
import numpy as np

# Some variables
fileFormat = 'PNG'
width, height = 1000, 1000


# Line class
class Line:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

    def draw(self, context):
        context.set_source_rgba(0, 0, 0, 1)
        context.move_to(self.p0[0], self.p0[1])
        context.line_to(self.p1[0], self.p1[1])
        context.stroke()

    def getLerp(self, _t):
        x = self.p0[0]+(self.p1[0]-self.p0[0])*_t
        y = self.p0[1]+(self.p1[1]-self.p0[1])*_t
        p = np.array([x, y])
        return p


# Map a value to a new range
def map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)


# Main function
def main():

    context.set_source_rgba(0.95, 0.95, 0.95, 1.0)
    context.paint()

    context.set_source_rgba(0, 0, 0, 1)

    border = 50
    borderSQ = border*2
    numLines = 18
    yStep = float((height-borderSQ)/numLines)
    xStep = float((width-borderSQ)/numLines)
    yOffset = yStep/2.0
    xOffset = xStep/2.0
    unOffset = 10
    myLines = []

    for i in range(numLines):
        for j in range(numLines-1):
            if j == 0:
                p1 = np.array([
                    xStep*j+xOffset + random.uniform(-xOffset, xOffset) + border,
                    yStep*i+yOffset + random.uniform(-yOffset, yOffset) + border
                ])
                p2 = np.array([
                    xStep*(j+1)+xOffset + random.uniform(-xOffset, xOffset) + border,
                    yStep*i+yOffset + random.uniform(-yOffset, yOffset) + border
                ])
                myLines.append(Line(p1, p2))
            else:
                p1 = np.array([
                    myLines[(j+(numLines-1)*i)-1].p1[0],
                    myLines[(j+(numLines-1)*i)-1].p1[1]
                ])
                p2 = np.array([
                    xStep*(j+1)+xOffset + random.uniform(-xOffset, xOffset) + border,
                    yStep*i+yOffset + random.uniform(-yOffset, yOffset) + border
                ])
                myLines.append(Line(p1, p2))

    index = 0
    for i in range(numLines):
        index = index + 1
        for j in range(numLines-1):
            if i != 0:
                lerpLines = int(map(i, 0, numLines, 1, 12))+1
                for k in range(lerpLines):
                    p0 = myLines[(j+(numLines-1)*(i-1))].getLerp(math.pow(map(k, 0, lerpLines-1, 0, 1), 1))
                    p1 = myLines[(j+(numLines-1)*i)].getLerp(math.pow(map(k, 0, lerpLines-1, 0, 1), 1))
                    line = Line(p0, p1)
                    line.draw(context)

    for line in myLines:
        line.draw(context)


# Call the main function
if __name__ == '__main__':
    if fileFormat == 'PNG':
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)
        main()
        filename = uuid.uuid4().hex[:8]
        surface.write_to_png("Images/Line_Grid/" + str(filename) + ".png")
    elif fileFormat == 'SVG':
        filename = uuid.uuid4().hex[:8]
        surface = cairo.SVGSurface(
                "Images/Line_Grid/0-svg/" + str(filename) + ".svg",
                width,
                height
        )
        context = cairo.Context(surface)
        main()
        surface.finish()
