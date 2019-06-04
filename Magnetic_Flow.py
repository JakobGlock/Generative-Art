import cairo, math, random, uuid

# Set to SVG to export an SVG file
fileFormat = 'PNG'

# Some variables
height = 1000
width = 1000
gridSize = 100
border, magBorder = 50, 450
stepX, stepY = (width//gridSize), (height//gridSize)

# Particle class
class Particle:
    def __init__(self, x, y, velX, velY):
        self.x = x
        self.y = y
        self.velX = velX
        self.velY = velY
        self.frcX = 0
        self.frcY = 0
        self.lx, self.ly = self.x, self.y
        self.drawStroke = True

    def update(self):

        self.x = self.x + self.frcX
        self.y = self.y + self.frcY

        self.velX = self.velX * 0.9
        self.velY = self.velY * 0.9

        self.x = self.x + self.velX
        self.y = self.y + self.velY

    def edges(self):
        if self.x <= 50 or self.x >= width-50 or self.y <= 50 or self.y >= height-50:
            self.drawStroke = False
        else:
            self.drawStroke = True

    def resetForce(self):
        self.frcX = 0
        self.frcY = 0

    def setForce(self, fx, fy):
        self.frcX = self.frcX + fx
        self.frcY = self.frcY + fy

    def setLastPos(self):
        self.lx, self.ly = self.x, self.y

    def calculateForce(self, mx, my, mp):
        dy = mx - self.x
        dx = my - self.y
        angle = math.atan2(dy, dx) * mp
        sx = math.sin(angle)
        sy = math.cos(angle)
        return [sx, sy]

    def draw(self, context):
        if self.drawStroke != False:
            context.set_line_width(0.9)
            context.set_source_rgba(0, 0, 0, 1)
            context.move_to(self.lx, self.ly)
            context.line_to(self.x, self.y)
            context.stroke()

# Magnet Class
class magnet:
    def __init__(self, x, y, pole):
        self.x = x
        self.y = y
        self.p = pole

# Main function
def main():

    context.set_source_rgba(0.95, 0.95, 0.95, 1)
    context.paint()

    magnets = []
    myParticles = []
    numMagnets = random.randint(2, 8)
    sumX, sumY = 0, 0
    sums = 0

    print("Number of Magnets: " + str(numMagnets))

    for m in range(numMagnets):
        pole = 1
        if random.uniform(0, 1) < 0.5:
            pole = -1

        magnets.append(magnet(random.randint(100, width-100), random.randint(100, height-100), pole))

    startNum = 360
    a = (math.pi*2)/startNum

    for x in range(100, width-100, (width-200)//1):
        for y in range(100, height-100, (height-200)//1):
            for i in range(startNum):
                xx, yy = x + (math.sin(a*i)*250) + ((width-200)//2), y + (math.cos(a*i)*250) + ((height-200)//2)#random.randint(100, width-100), random.randint(100, height-100)
                vx, vy = random.uniform(-1, 1)*0.5, random.uniform(-1, 1)*0.5
                myParticles.append(Particle(xx, yy, vx, vy))

    for p in myParticles:
        for t in range(1000):
            for m in magnets:
                sums = p.calculateForce(m.x, m.y, m.p*4)
                sumX = sumX + sums[0]
                sumY = sumY + sums[1]

            sumX = sumX / len(magnets)
            sumY = sumY / len(magnets)

            p.resetForce()
            p.setForce(sumX, sumY)
            p.update()
            p.edges()
            if t%8 == 0:
                p.draw(context)
                p.setLastPos()

# Call the main function
if __name__ == '__main__':
    if fileFormat == 'PNG':
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)
        main()
        filename = uuid.uuid4().hex[:8]
        surface.write_to_png('Images/Magnetic_Flow/'+ str(filename) +'.png')
    elif fileFormat == 'SVG':
        filename = uuid.uuid4().hex[:8]
        surface = cairo.SVGSurface('Images/Magnetic_Flow/0-svg/'+ str(filename) +'.svg', width, height)
        context = cairo.Context(surface)
        main()
        surface.finish()
