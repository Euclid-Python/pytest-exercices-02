import pytest
import math
from ex02.geometry import Point, Line, CircularArc


def test_add():
    a = Point(0.5, 0.5)
    b = Point(-1, 1)
    c = a + b
    assert c.x == -0.5
    assert c.y == 1.5


def test_equal():
    a = Point(0.5, 0.5)
    b = Point(0.5 * (1 + 1e-10), 0.5)
    assert a == b


def test_equal_float_int():
    a = Point(4, 1)
    b = Point(4.0, 1.0)
    assert a == b


def test_equal_10e17():
    a = Point(0.0, 6.123233995736766e-17)
    b = Point(0., 0.)
    assert a == b


def test_equal_tuple():
    a = Point(1.0, 4.0)
    assert a == (1, 4)


def test_are_orthogonal():
    a = Point(0.5, 0.5)
    b = Point(-1, 1)
    assert a.is_orthogonal(b)


def test_are_not_orthogonal():
    a = Point(1, 0.7)
    b = Point(0.5, 1)
    assert not a.is_orthogonal(b)


def test_are_collinear():
    a = Point(0.5, 0.5)
    b = Point(1, 1)
    assert a.is_collinear(b)


def test_coordinate_belongs_to_line():
    A = Point(1, 2)
    line = Line(A, Point(1, 1))
    assert line.contains(Point(2, 3))


def test_intersection():
    line_a = Line(Point(0, 0), Point(1, 0))
    line_b = Line(Point(0, 0), Point(0, 1))
    assert line_a.intersection(line_b) == Point(0, 0)


def test_intersection_2():
    line_a = Line(Point(3, 1), Point(1, 1))
    line_b = Line(Point(0, 2), Point(1, 0))
    intersection = line_a.intersection(line_b)
    expected = Point(4, 2)
    assert intersection == expected, f'{intersection} != {expected}'


def test_intersection_of_parallel_lines():
    line_a = Line(Point(0, 1), Point(0, 1))
    line_b = Line(Point(1, 1), Point(0, 1))

    with pytest.raises(ValueError):
        intersection = line_a.intersection(line_b)


def test_distance_a_b():
    assert math.isclose(Point.distance(Point(1, 0), Point(0, 1)), math.sqrt(2))


def test_circular_arc():
    arc = CircularArc(start=Point(1, 0), end=Point(0, 1), tangent=Point(0, 1))
    assert math.isclose(arc.angle, (math.pi / 2.0))


table_vectors_angles = [
    ((-1, 0), (1, 0), math.pi),
    ((1, 0), (0, 1), math.pi / 2),
    ((1, 0), (0, -1), math.pi / 2)

]


@pytest.mark.parametrize('a, b, angle', table_vectors_angles)
def test_find_angle_from_2_vectors(a, b, angle):
    def f(u, v):
        return math.acos(u.scalar_product(v))

    assert f(Point(a[0], a[1]), Point(b[0], b[1])) == angle

def test_find_find_angle_and_chord_vector():
    angle, u, distance = CircularArc.find_angle_and_chord_vector(Point(-1, 0),
                                                                 Point(1, 0),
                                                                 Point(0, 1))
    assert angle == math.pi


def test_simple_arc():
    candidate = CircularArc(Point(-1, 0),
                           Point(1, 0),
                           Point(0, 1))
    assert candidate.radius == 1
    assert candidate.angle == math.pi
    assert candidate.center == Point(0., 0.)


def test_45deg_arc():
    candidate = CircularArc(Point(1, 0),
                           Point(0, 1),
                           Point(0, 1))

    assert math.isclose(candidate.angle, math.pi / 2)
    assert candidate.center == Point(0, 0)
    assert math.isclose(candidate.radius, 1)


def test_reverse_45deg_arc():
    candidate = CircularArc(Point(1, 0),
                           Point(0, 1),
                           Point(0, -1))

    assert candidate.center == Point(0, 0)
    assert math.isclose(candidate.radius, 1)
    assert math.isclose(candidate.angle, math.pi / 2)


def test_compute_center_with_each_tangent_simple():
    candidate = CircularArc.compute_center_with_each_tangent(p0=Point(-1,0),
                                                 p1=Point(1, 0),
                                                 tangent_p0=Point(0,1),
                                                 tangent_p1=Point(0,-1))
    assert candidate == Point(0, 0)

def test_compute_center_with_each_tangent():
    candidate = CircularArc.compute_center_with_each_tangent(p0=Point(-1,0),
                                                 p1=Point(1, 0),
                                                 tangent_p0=Point(1,1),
                                                 tangent_p1=Point(1,-1))
    assert candidate == Point(0, -1)
