import cairo
import numpy as np
import random, math, uuid

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

# Map values to a new range
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

    connectorLines = []

    numLinesX = 20
    numLinesY = 3
    xStep = float((width-100) // numLinesX)
    yStep = float(height // numLinesY)
    xOffset = (xStep // 2) + 50
    yOffset = yStep // 2

    for h in range(numLinesY):
        for i in range(numLinesX):
            x = xStep * i + xOffset
            y = yStep * h + yOffset
            yy = random.randint(25, 100)
            p0 = np.array([x + random.uniform(-(xStep//2)+10, (xStep//2)+10), random.uniform(y-50, y+50) + yy])
            p1 = np.array([x + random.uniform(-(xStep//2)+10, (xStep//2)+10), random.uniform(y-50, y+50) - yy])
            connectorLines.append(Line(p0, p1))

            if i != 0:
                numLines = 21
                l1 = i+numLinesX*h
                l2 = (i+numLinesX*h)+1

                while l2 == l1:
                    l2 = random.randint(0, len(connectorLines))

                for j in range(numLines):
                    p0 = connectorLines[l1-1].getLerp(math.pow(map(j, 0, numLines, 0, 1), 1))
                    p1 = connectorLines[l2-1].getLerp(math.pow(map(j, 0, numLines, 0, 1), 1))
                    line = Line(p0, p1)
                    line.draw(context)

# Call the main function and save an image
if __name__ == '__main__':
    if fileFormat == 'PNG':
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)
        main()
        filename = uuid.uuid4().hex[:8]
        surface.write_to_png("Images/Parallel_Lines/"+ str(filename) +".png")
    elif fileFormat == 'SVG':
        filename = uuid.uuid4().hex[:8]
        surface = cairo.SVGSurface("Images/Parallel_Lines/0-svg/"+ str(filename) +".svg", width, height)
        context = cairo.Context(surface)
        main()
        surface.finish()
