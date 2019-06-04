import cairo, math, uuid, random
import numpy as np

# Some variables
fileFormat = 'PNG'
width, height = 1000, 1000

# Line class
class Line:
    def __init__(self, p0, dir, id):
        self.id = id
        self.p0 = p0
        self.p1 = p0
        self.dir = dir

    def draw(self, context):
        context.set_source_rgba(0.15, 0.15, 0.15, 1)
        context.move_to(self.p0[0], self.p0[1])
        context.line_to(self.p1[0], self.p1[1])
        context.stroke()

    def update(self):
        self.p1 = self.p1 + self.dir

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

    def changeDir(self, a):
        currentAngle = math.atan2(a[1], a[0]) * 180 / math.pi
        newDir = random.randint(-15, 15)
        angle = math.radians(currentAngle + newDir)
        dir = np.array([math.cos(angle), math.sin(angle)])
        self.dir = dir

    def getLength(self):
        dist = math.hypot(self.p0[0] - self.p1[0], self.p0[1] - self.p1[1])
        return dist

    def getDirection(self):
        dir = (self.p0 - self.p1) / self.getLength()
        return dir * -1.0

    def getDistFromCenter(self, center):
        dist = math.hypot(self.p1[0] - center[0], self.p1[1] - center[1])
        return dist

# Main function
def main():

    context.set_source_rgba(0.95, 0.95, 0.95, 1.0)
    context.paint()

    gridSize = 3
    border = 40
    xStep = (width-(border*2)) / float(gridSize)
    yStep = (height-(border*2)) / float(gridSize)
    xOffset = xStep / 2.0
    yOffset = yStep / 2.0

    for y in range(gridSize):
        for x in range(gridSize):
            xPos = xStep * x + xOffset + border
            yPos = yStep * y + yOffset + border
            myLines = []
            numLines = 180
            angle = (2*math.pi) / float(numLines)
            centerX = width / 2.0
            centerY = height / 2.0
            center = np.array([xPos, yPos])
            circleSize = (xStep / 2.0) - 10

            order = []
            for i in range(numLines):
                order.append(i)

                random.shuffle(order)

            for i in range(numLines):
                index = order[i]
                pos = np.array([(math.cos(angle*index) * (circleSize-0.1))+center[0], (math.sin(angle*index) * (circleSize-0.1))+center[1]])
                dir = (pos - np.array([centerX, centerY])) * -1.0
                myLines.append(Line(pos, dir, i))
                myLines[i].changeDir(dir)

                while myLines[i].getDistFromCenter(center) < circleSize:
                    myLines[i].update()

                    stopDrawing = False
                    for line in myLines:
                        if line.id != myLines[i].id:
                            if myLines[i].intersect(line.p0, line.p1):
                                stopDrawing = True
                                break

                    if stopDrawing:
                        break

            for line in myLines:
                if line.getLength() > 0:
                    line.draw(context)

# Call the main function and save image
if __name__ == '__main__':
    if fileFormat == 'PNG':
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)
        main()
        filename = str(uuid.uuid4().hex[:8])
        surface.write_to_png("Images/Circular/" + filename + ".png")
    else:
        filename = str(uuid.uuid4().hex[:8])
        surface = cairo.SVGSurface("Images/Circular/0-svg/" + filename + ".svg", width, height)
        context = cairo.Context(surface)
        main()
        surface.finish()
