from numpy import cross


# Is a point on a line segment
def point_on_segment(p, a, b, EPSILON=10.0):
    ap = a - p
    ab = a - b
    c = cross(ap, ab)
    if c < -EPSILON and c > EPSILON:
        return False

    KAP = ap.dot(ab)
    if KAP < 0:
        return False
    if KAP == 0:
        return True

    KAB = ab.dot(ab)
    if KAP > KAB:
        return False
    if KAP == KAB:
        return True

    return True


# Intersection method stolen from:
# https://algorithmtutor.com/Computational-Geometry/Check-if-two-line-segment-intersect/
def direction(p1, p2, p3):
    return cross(p3 - p1, p2 - p1)


def on_segment(p1, p2, p):
    return min(p1.x, p2.x) <= p.x <= max(p1.x, p2.x) and \
            min(p1.y, p2.y) <= p.y <= max(p1.y, p2.y)


def intersect(a, b):
    p1, p2, p3, p4 = a.p0, a.p1, b.p0, b.p1
    d1 = direction(p3, p4, p1)
    d2 = direction(p3, p4, p2)
    d3 = direction(p1, p2, p3)
    d4 = direction(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    elif d1 == 0 and on_segment(p3, p4, p1):
        return True
    elif d2 == 0 and on_segment(p3, p4, p2):
        return True
    elif d3 == 0 and on_segment(p1, p2, p3):
        return True
    elif d4 == 0 and on_segment(p1, p2, p4):
        return True
    else:
        return False
