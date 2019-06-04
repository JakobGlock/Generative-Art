import cairo, math, random, uuid
import numpy as np
from noise import pnoise2

# Some variables
fileFormat = 'PNG'
width, height = 1000, 1000
centerX, centerY = width/2, height/2
TWO_PI = math.pi*2.0

# Noise generator class
class NoiseLoop:
    def __init__(self, diameter, min, max):
        self.diameter = diameter
        self.min = min
        self.max = max
        self.noiseSeed = random.randint(0, 10000)

    def getValue(self, a):
        x = self.map(math.cos(math.radians(a)), -1, 1, 0, self.diameter)
        y = self.map(math.sin(math.radians(a)), -1, 1, 0, self.diameter)
        r = pnoise2(x+self.noiseSeed, y+self.noiseSeed)
        return self.map(r, -1, 1, self.min, self.max)

    def map(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value - leftMin) / float(leftSpan)
        return rightMin + (valueScaled * rightSpan)

    def setNoiseSeed(self, _offset):
        self.noiseSeed = _offset

# Line class
class Line:
    def __init__(self, context, x1, y1, x2, y2):
        self.context = context
        self.p0 = np.array([x1, y1])
        self.p1 = np.array([x2, y2])
        self.id = None

    def draw(self):
        self.context.move_to(self.p0[0], self.p0[1])
        self.context.line_to(self.p1[0], self.p1[1])

    def getLength(self):
        return sqrt((self.p1[0] - self.p0[0])**2 + (self.p1[1] - self.p0[1])**2)

    def setId(self, id):
        self.id = id

# Map a value to a new range
def map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def main():

    context.set_source_rgba(0.95, 0.95, 0.95, 1.0)
    context.paint()

    context.set_source_rgba(0.0, 0.0, 0.0, 1.0)
    gridX, gridY = 1, 1
    xStep, yStep = width//gridX, height//gridY
    xOffset, yOffset = xStep//2, yStep//2

    nLoop = []
    offset = []
    numLayers = 40
    s = (xOffset // numLayers)

    for xxx in range(gridX):
        for yyy in range(gridY):
            centerX = xxx * xStep + xOffset
            centerY = yyy * yStep + yOffset
            for l in range(numLayers):
                offset = random.randint(0, 360)
                nLoop.append(NoiseLoop(map(l, 0, numLayers, 1, 4), s*l, s*l+s))
                numPoints = 360
                for i in range(numPoints):
                    r = nLoop[l].getValue(i)
                    x = r * math.cos(math.radians(i)) + centerX
                    y = r * math.sin(math.radians(i)) + centerY
                    context.line_to(x, y)
                context.close_path()
                context.stroke()

                if l != 0:
                    numLines = map(l, 0, numLayers, 16, 2)
                    numPoints = 360 / numLines
                    for i in range(int(numPoints)):
                        r = nLoop[l].getValue(i*numLines+offset)
                        x = r * math.cos(math.radians(i*numLines+offset)) + centerX
                        y = r * math.sin(math.radians(i*numLines+offset)) + centerY

                        r = nLoop[l-1].getValue(i*numLines+offset)
                        xx = r * math.cos(math.radians(i*numLines+offset)) + centerX
                        yy = r * math.sin(math.radians(i*numLines+offset)) + centerY
                        line = Line(context, xx, yy, x, y)
                        line.draw()
                        context.stroke()

# Call the main function
if __name__ == '__main__':
    if fileFormat == 'PNG':
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)
        main()
        fileName = uuid.uuid4().hex[:8]
        surface.write_to_png("Images/Mosaic_Circles/"+ str(fileName) +".png")
    elif fileFormat == 'SVG':
        fileName = uuid.uuid4().hex[:8]
        surface = cairo.SVGSurface("Images/Mosaic_Circles/0-svg/"+str(fileName)+".svg", width, height)
        context = cairo.Context(surface)
        main()
        surface.finish()
