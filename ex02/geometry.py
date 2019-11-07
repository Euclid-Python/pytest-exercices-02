import math

""""
Module for simple geometry in 2D
"""


class Point:
    def __init__(self, x, y=None):
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def new(cls, xy):
        return Point(xy[0], xy[1])

    def normal(self):
        return Point(-self.y, self.x)

    def normalize(self, d=0):
        if d == 0:
            d = math.sqrt(self.x * self.x + self.y * self.y)
        return Point(self.x / d, self.y / d)

    def scalar_product(self, other: 'Point'):
        return self.x * other.x + self.y * other.y

    def is_orthogonal(self, other: 'Point'):
        product = self.scalar_product(other)
        return math.isclose(product, 0)

    def is_collinear(self, other: 'Point'):
        return self.is_orthogonal(other.normal())

    def __add__(self, other: 'Point'):
        r = NotImplemented
        if isinstance(other, Point):
            r = Point(self.x + other.x, self.y + other.y)
        return r

    def __sub__(self, other: 'Point'):
        r = NotImplemented
        if isinstance(other, Point):
            r = Point(self.x - +other.x, self.y - other.y)
        return r

    def __mul__(self, other):
        r = NotImplemented
        if isinstance(other, float) or isinstance(other, int):
            factor = float(other)
            r = Point(self.x * factor, self.y * factor)
        return r

    def __eq__(self, other: 'Point'):
        r = NotImplemented
        if isinstance(other, tuple):
            other = Point.new(other)
        if isinstance(other, Point):
            r = math.isclose(self.x, other.x, abs_tol=1e-9) and math.isclose(self.y, other.y, abs_tol=1e-9)
        return r

    def __repr__(self):
        return f'p({self.x}, {self.y})'

    @staticmethod
    def distance(a: 'Point', b: 'Point') -> float:
        dx = a.x - b.x
        dy = a.y - b.y
        return math.sqrt(dx * dx + dy * dy)


class Segment:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Line:
    def __init__(self, point: Point, vector: Point):
        self.point = point
        self.vector = vector.normalize()

    def contains(self, point: Point):
        a = self.point
        b = point
        v_ab = Point(a.x - b.x, a.y - b.y)
        return v_ab.is_collinear(self.vector)

    def intersection(self, line: 'Line'):
        v0 = self.vector
        p0 = self.point

        v1 = line.vector
        p1 = line.point

        v1_v0 = v1.scalar_product(v0)

        dp = p1 - p0

        dp_vo = dp.scalar_product(v0)
        dp_v1 = dp.scalar_product(v1)

        if math.isclose( math.fabs(v1_v0), 1.):
            raise ValueError('Lines are parallel')
        else:
            coef0 = (dp_vo - dp_v1 * v1_v0) / (1 - v1_v0 * v1_v0)

        return v0 * coef0 + p0

    def __repr__(self):
        return f'line({self.point}, {self.vector})'


class CircularArc:
    def __init__(self, start: Point, end: Point, tangent: Point):
        self.start = start
        self.end = end
        self.center = CircularArc.compute_center_with_tangent(start, end, tangent)
        self.radius = Point.distance(self.center, self.start)
        self.angle = 2 * math.asin(Point.distance(start, end) / (2 * self.radius))
        self.length = self.angle * math.pi * self.radius

    @staticmethod
    def compute_center(start, end, radius, angle):
        chord = Point((end.x - start.x), (end.y - start.y))
        c = Point((end.x + start.x) / 2, (end.y + start.y) / 2)
        ortho_c = chord.normal()
        ortho_c = ortho_c.normalize()
        center = ortho_c * radius * math.cos(angle / 2) + c
        return center

    @staticmethod
    def compute_center_with_tangent(start, end, tangent):
        chord = end - start
        c = Point((end.x + start.x) / 2, (end.y + start.y) / 2)
        try:
            center = CircularArc.compute_intersection_with_each_tangent(start, c, tangent, chord)
        except ValueError:
            center = c
        return center

    @staticmethod
    def compute_center_with_each_tangent(p0, p1, tangent_p0, tangent_p1):
        try:
            center = CircularArc.compute_intersection_with_each_tangent(p0, p1, tangent_p0, tangent_p1)
        except ValueError:
            center = Point((p1.x + p0.x) / 2, (p1.y + p0.y) / 2)
        return center

    @staticmethod
    def compute_intersection_with_each_tangent(p0, p1, tangent_p0, tangent_p1):
        radial_p0 = tangent_p0.normal()
        radial_p1 = tangent_p1.normal()
        line_p0 = Line(p0, radial_p0)
        line_p1 = Line(p1, radial_p1)
        return line_p0.intersection(line_p1)


    @staticmethod
    def find_angle_and_chord_vector(start, end, tangent):
        a = start
        b = end
        v = tangent

        distance = Point.distance(a, b)
        u = Point(b.x - a.x, b.y - a.y)
        u = u.normalize(distance)
        v = v.normalize()
        angle = math.acos(u.scalar_product(v))
        sign = u.x * v.y + u.y * v.x
        angle = 2 * angle * sign

        return angle, u, distance