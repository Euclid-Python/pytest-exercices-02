import math
from math import isclose, fabs
from ex02.geometry import Line, Point, Arc


def test_find_point_on_circle():
    p0 = Point(0,1)
    v0 = Point(0,1)
    p1 = Point(3,5)
    v1 = Point(1,0)

    line0 = Line(point=p0, vector=v0)
    line1 = Line(point=p1, vector=v1)

    bissec_vector = (v0 + v1).normalize()
    assert bissec_vector == Point(1,1).normalize()

    bissec_line = Line(point=p1, vector=bissec_vector)

    intersec =line0.intersection(bissec_line)

    assert intersec == (0,2)

    def is_beyond_point(line, p):
        return (p-line.point).scalar_product(line.vector) > 0

    assert is_beyond_point(line0, intersec)

    new_line0 = Line(intersec,v0)

    center =Arc.compute_center_from_both_tangents(intersec,p1, v0,v1)
    assert math.isclose(Point.distance(intersec,center), Point.distance(p1,center))


