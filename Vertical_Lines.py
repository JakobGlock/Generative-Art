import cairo, math, uuid, random
import numpy as np

# Variables
fileFormat = 'PNG'
width, height = 1000, 1000

# Line class
class lineSegment:
    def __init__(self, p0, dir, id):
        self.id = id
        self.p0 = p0
        self.p1 = p0
        self.dir = dir
        self.intersect = np.array([0.0, 0.0])
        self.count = 0

    def draw(self, context):
        context.set_source_rgba(0, 0, 0, 1)
        context.move_to(self.p0[0], self.p0[1])
        context.line_to(self.p1[0], self.p1[1])
        context.stroke()

    def extendLine(self):
        self.p1 = self.p1 + self.dir

    def changeDir(self):
        self.count = self.count + 1

        if self.count%40 == 0:
            angle = math.radians(random.randint(45, 135))
            dir = np.array([math.sin(angle), math.cos(angle)])
            self.dir = dir
            return True
        else:
            return False

    def edges(self):
        if self.p1[0] >= width or self.p1[0] < 0 or self.p1[1] < 0 or self.p1[1] >= height-50:
            return True

    def lineIntersection(self, p2, p3):
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
            self.intersect = np.array([intersectX, intersectY])
            return True
        else:
            return False

    def getIntersect(self):
        return self.intersect

    def getClosetPoint(self, p):
        a = np.linalg.norm(self.p0-p)
        b = np.linalg.norm(self.p1-p)

        if a <= b:
            self.p0 = p
        else:
            self.p1 = p

# Helper function
def getDirection():
    numAngles = 2
    r = int(random.uniform(0, numAngles))
    angleStep = [0, 45]

    for i in range(numAngles):
        if i == r:
            angle = math.radians(angleStep[i])

    dir = np.array([math.sin(angle), math.cos(angle)])
    return dir

# Main function
def main():
    context.set_source_rgba(0.95, 0.95, 0.95, 1)
    context.paint()

    numWalkers = random.randint(100, 200)
    walkers = []
    xStep = float((width-100)) / numWalkers
    amt = random.uniform(0.075, 0.15)
    amtStep = random.randint(15, 80)
    startDist = random.randint(10, 150)

    index = 0
    count = 0
    for i in range(numWalkers):
        x = float((xStep * i) + 50.0)
        pos = np.array([float(x), float(50.0)])
        angle = math.radians(0)
        dir = np.array([math.sin(angle), math.cos(angle)])
        walkers.append(lineSegment(pos, dir, i))

        walk = True
        while walk:
            if count%amtStep == 0:
                r = random.uniform(0, 1)
                if r < amt and walkers[index].p0[1] > startDist:
                    dir = getDirection()
                    walkers.append(lineSegment(walkers[index].p1, dir, i))
                    index = index + 1
                else:
                    angle = math.radians(0)
                    dir = np.array([math.sin(angle), math.cos(angle)])
                    walkers.append(lineSegment(walkers[index].p1, dir, i))
                    index = index + 1

            walkers[index].extendLine()

            hitLine = False
            for w in walkers:
                if walkers[index].id != w.id:
                    intersect = walkers[index].lineIntersection(w.p0, w.p1)
                    if intersect:
                        hitLine = True

            hitEdge = walkers[index].edges()
            if hitEdge or hitLine:
                walk = False

            count = count + 1
        index = index + 1

    for walker in walkers:
        walker.draw(context)

# Call the main function and save an image
if __name__ == '__main__':
    if fileFormat == 'PNG':
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)
        main()
        fileName = uuid.uuid4().hex[:8]
        surface.write_to_png('Images/Vertical_Lines/'+str(fileName)+'.png')
    elif fileFormat == 'SVG':
        fileName = uuid.uuid4().hex[:8]
        surface = cairo.SVGSurface('Images/Vertical_Lines/0-svg/'+str(fileName)+'.svg', width, height)
        context = cairo.Context(surface)
        main()
        context.finish()
