import pytest
import math
from ex02.geometry import Point, Line, Arc, Geometry


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
    arc = Arc(start=Point(1, 0), end=Point(0, 1), start_tangent=Point(0, 1))
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
    angle, u, distance = Arc.find_angle_and_chord_vector(Point(-1, 0),
                                                         Point(1, 0),
                                                         Point(0, 1))
    assert angle == math.pi


def test_simple_arc():
    candidate = Arc(Point(-1, 0),
                    Point(1, 0),
                    Point(0, 1))
    assert candidate.radius == 1
    assert candidate.angle == -math.pi
    assert candidate.center == Point(0., 0.)


def test_45deg_arc():
    candidate = Arc(Point(1, 0),
                    Point(0, 1),
                    Point(0, 1))

    assert math.isclose(candidate.angle, math.pi / 2)
    assert candidate.center == Point(0, 0)
    assert math.isclose(candidate.radius, 1)
    assert candidate.direction == Arc.DIRECT


def test_reverse_45deg_arc():
    candidate = Arc(start=Point(1, 0),
                    end=Point(0, 1),
                    start_tangent=Point(0, -1))

    assert candidate.center == Point(0, 0)
    assert math.isclose(candidate.radius, 1)
    assert candidate.end_tangent == Point(1,0)
    assert math.isclose(candidate.angle, -3*math.pi / 2)
    assert candidate.direction == Arc.INDIRECT


def test_arc_with_zero_radius():
    candidate = Arc(start=Point(0, 0),
                    end=Point(0, 0),
                    start_tangent=Point(0, 1),
                    end_tangent=Point(0, -1))
    assert candidate.radius == 0
    assert candidate.angle == math.pi
    assert candidate.center == Point(0., 0.)


def test_compute_center_from_both_tangents_simple():
    candidate = Arc.compute_center_from_both_tangents(p0=Point(-1, 0), p1=Point(1, 0), tangent_p0=Point(0, 1),
                                                      tangent_p1=Point(0, -1))
    assert candidate == Point(0, 0)


def test_compute_center_from_both_tangents():
    candidate = Arc.compute_center_from_both_tangents(p0=Point(-1, 0), p1=Point(1, 0), tangent_p0=Point(1, 1),
                                                      tangent_p1=Point(1, -1))
    assert candidate == Point(0, -1)


def test_compute_center_from_both_tangents_but_same_points():
    candidate = Arc.compute_center_from_both_tangents(p0=Point(0, 0), p1=Point(0, 0), tangent_p0=Point(1, 1),
                                                      tangent_p1=Point(1, -1))
    assert candidate == Point(0, 0)


def rotate(vector, angle):
    from math import cos, sin
    x = vector.x * cos(angle) - vector.y * sin(angle)
    y = vector.x * sin(angle) + vector.y * cos(angle)
    return Point(x, y)


def rotate_from_axe(vector, axe):
    axe = axe.normalize()
    cos_ = axe.x
    sin_ = -axe.y
    x = vector.x * cos_ - vector.y * sin_
    y = vector.x * sin_ + vector.y * cos_
    return Point(x, y)

@pytest.mark.parametrize("vector, axe, expected", [
    ( (0, 1), (1, 0), (0, 1) ),
    ( (0, 1), (0, 1), (1, 0)),
    ((0, 1), (0.5, 0.5), (0.5, 0.5)),
    ((0, 1), (-0.5, -0.5), (-0.5, -0.5)),
])
def test_rotate_from_axe(vector, axe, expected):
    vector = Point.new(vector)
    axe = Point.new(axe)
    expected = Point.new(expected).normalize()
    assert rotate_from_axe(vector, axe) == expected
    assert rotate_from_axe(expected, Point(axe.x, - axe.y)) == vector

@pytest.mark.parametrize("vector, axe, expected", [
    ( (0, 1), (1, 0), (0, -1) ),
    ( (0, 1), (0, 1), (0,1)),
    ((0, 1), (0.5, 0.5), (1, 0)),
    ((0, 1), (-0.5, -0.5), (1, 0)),
])
def test_get_symmetrical_with_rotate_from_axe(vector, axe, expected):
    vector = Point.new(vector)
    axe = Point.new(axe)
    expected = Point.new(expected).normalize()

    symmetrical = rotate_from_axe(vector, axe)
    symmetrical = Point(symmetrical.x, -symmetrical.y)

    assert rotate_from_axe(symmetrical, Point(axe.x, - axe.y)) == expected


@pytest.mark.parametrize("vector, axe, expected", [
    ( (0, 1), (1, 0), (0, -1) ),
    ( (0, 1), (0, 1), (0,1)),
    ((0, 1), (0.5, 0.5), (1, 0)),
    ((0, 1), (-0.5, -0.5), (1, 0)),
    ((1, 1), (0,1), (-1, 1)),
])
def test_geometry_get_symmetrical(vector, axe, expected):
    vector = Point.new(vector)
    axe = Point.new(axe)
    expected = Point.new(expected).normalize()
    assert expected == Geometry.get_symmetrical(vector, axe).normalize()

@pytest.mark.parametrize("a, b, expected", [
    ( (1,0), (0,1), 1),
    ((0, 1), (1, 0), -1)

])
def test_geometry_angle_direction(a,b, expected):
    a = Point.new(a)
    b = Point.new(b)
    assert a.vectorial_product(b) == expected

def test_find_angle_from_tangents_and_points():
    a = Point(1,0)
    b = Point(0,1)
    ta = Point(0,-1)
    tb = Point(1,0)
    c = Point(0,0)
    vk = (c-a).vectorial_product(ta)

    assert vk == 1
    def rotate_from_center(c, p, phi):
        radius = Point.distance(c, p)
        x = radius * math.cos(phi)
        y = radius * math.sin(phi)
        rotated = Point(x,y) + c
        return rotated

    rotated = rotate_from_center(c, a, math.pi/2)
    assert rotated == b

    rotated = rotate_from_center(c, a, -3*math.pi/2)
    assert rotated == b
