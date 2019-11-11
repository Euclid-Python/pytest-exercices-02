import pytest
import math
from ex02.geometry import Point, Line, Arc, Geometry

NORTH = Point(0, 1)
SOUTH = Point(0, -1)
WEST = Point(-1, 0)
EAST = Point(1, 0)
NORTH_EAST = (NORTH + EAST).normalize()
NORTH_WEST = (NORTH + WEST).normalize()
SOUTH_EAST = (SOUTH + EAST).normalize()
SOUTH_WEST = (SOUTH + WEST).normalize()


class TestPoint:

    def test_add(self):
        a = Point(0.5, 0.5)
        b = Point(-1, 1)
        c = a + b
        assert c.x == -0.5
        assert c.y == 1.5


    def test_equal(self):
        a = Point(0.5, 0.5)
        b = Point(0.5 * (1 + 1e-10), 0.5)
        assert a == b


    def test_equal_float_int(self):
        a = Point(4, 1)
        b = Point(4.0, 1.0)
        assert a == b


    def test_equal_10e17(self):
        a = Point(0.0, 6.123233995736766e-17)
        b = Point(0., 0.)
        assert a == b


    def test_equal_tuple(self):
        a = Point(1.0, 4.0)
        assert a == (1, 4)


    def test_are_orthogonal(self):
        a = Point(0.5, 0.5)
        b = Point(-1, 1)
        assert a.is_orthogonal(b)


    def test_are_not_orthogonal(self):
        a = Point(1, 0.7)
        b = Point(0.5, 1)
        assert not a.is_orthogonal(b)


    def test_are_collinear(self):
        a = Point(0.5, 0.5)
        b = Point(1, 1)
        assert a.is_collinear(b)

    def test_distance_a_b(self):
        assert math.isclose(Point.distance(Point(1, 0), Point(0, 1)), math.sqrt(2))

    @pytest.mark.parametrize("a, b, expected", [
        (EAST, NORTH, 1),
        (NORTH, EAST, -1)

    ])
    def test_geometry_angle_direction(self, a, b, expected):
        assert a.vectorial_product(b) == expected


class TestLine:

    def test_coordinate_belongs_to_Line(self):
        A = Point(1, 2)
        line = Line(point=A, vector=Point(1, 1))
        assert line.contains(Point(2, 3))


    def test_line_with_zero_vector(self):
        with pytest.raises(ZeroDivisionError):
            A = Point(1, 2)
            line = Line(point=A, vector=Point(0, 0))


    def test_intersection(self):
        line_a = Line(point=Point(0, 0), vector=Point(1, 0))
        line_b = Line(point=Point(0, 0), vector=Point(0, 1))
        assert line_a.intersection(line_b) == Point(0, 0)


    def test_intersection_2(self):
        line_a = Line(point=Point(3, 1), vector=Point(1, 1))
        line_b = Line(point=Point(0, 2), vector=Point(1, 0))
        intersection = line_a.intersection(line_b)
        expected = Point(4, 2)
        assert intersection == expected, f'{intersection} != {expected}'


    def test_intersection_of_parallel_lines(self):
        line_a = Line(point=Point(0, 1), vector=Point(0, 1))
        line_b = Line(point=Point(1, 1), vector=Point(0, 1))

        with pytest.raises(ValueError):
            intersection = line_a.intersection(line_b)

class TestArc:

    def test_circular_arc(self):
        arc = Arc(start=Point(1, 0), end=Point(0, 1), start_tangent=Point(0, 1))
        assert math.isclose(arc.angle, (math.pi / 2.0))




    @pytest.mark.parametrize('a, b, angle', [
        ((-1, 0), (1, 0), math.pi),
        ((1, 0), (0, 1), math.pi / 2),
        ((1, 0), (0, -1), math.pi / 2)

    ])
    def test_find_angle_from_2_vectors(self, a, b, angle):
        def f(u, v):
            return math.acos(u.scalar_product(v))

        assert f(Point(a[0], a[1]), Point(b[0], b[1])) == angle


    def test_find_find_angle_and_chord_vector(self):
        angle, u, distance = Arc.find_angle_and_chord_vector(Point(-1, 0),
                                                             Point(1, 0),
                                                             Point(0, 1))
        assert angle == math.pi


    def test_simple_arc(self):
        candidate = Arc(Point(-1, 0),
                        Point(1, 0),
                        Point(0, 1))
        assert candidate.radius == 1
        assert candidate.angle == -math.pi
        assert candidate.center == Point(0., 0.)


    def test_45deg_arc(self):
        candidate = Arc(Point(1, 0),
                        Point(0, 1),
                        Point(0, 1))
    
        assert math.isclose(candidate.angle, math.pi / 2)
        assert candidate.center == Point(0, 0)
        assert math.isclose(candidate.radius, 1)
        assert candidate.direction == Arc.DIRECT


    def test_reverse_45deg_arc(self):
        candidate = Arc(start=Point(1, 0),
                        end=Point(0, 1),
                        start_tangent=Point(0, -1))

        assert candidate.center == Point(0, 0)
        assert math.isclose(candidate.radius, 1)
        assert candidate.end_tangent == Point(1, 0)
        assert math.isclose(candidate.angle, -3 * math.pi / 2)
        assert candidate.direction == Arc.INDIRECT
        assert candidate.length > 0


    def test_arc_with_zero_radius(self):
        candidate = Arc(start=Point(0, 0),
                        end=Point(0, 0),
                        start_tangent=Point(0, 1),
                        end_tangent=Point(0, -1))
        assert candidate.radius == 0
        assert candidate.angle == math.pi
        assert candidate.center == Point(0., 0.)


    def test_compute_center_from_both_tangents_simple(self):
        candidate = Arc.compute_center_from_both_tangents(p0=Point(-1, 0), p1=Point(1, 0), tangent_p0=Point(0, 1),
                                                          tangent_p1=Point(0, -1))
        assert candidate == Point(0, 0)


    def test_compute_center_from_both_tangents(self):
        candidate = Arc.compute_center_from_both_tangents(p0=Point(-1, 0), p1=Point(1, 0), tangent_p0=Point(1, 1),
                                                          tangent_p1=Point(1, -1))
        assert candidate == Point(0, -1)


    def test_compute_center_from_both_tangents_but_same_points(self):
        candidate = Arc.compute_center_from_both_tangents(p0=Point(0, 0), p1=Point(0, 0), tangent_p0=Point(1, 1),
                                                          tangent_p1=Point(1, -1))
        assert candidate == Point(0, 0)


    def test_compute_center_from_both_tangents_impossible(self):
        with pytest.raises(AssertionError) as ae:
            Arc.compute_center_from_both_tangents(p0=Point(-5, 2),
                                                  p1=Point(1, 0),
                                                  tangent_p0=Point(0, 1),
                                                  tangent_p1=Point(1, -1))


class TestGeometry:
    @pytest.mark.parametrize("vector, reference, expected", [
        (NORTH, EAST, NORTH),
        (NORTH, NORTH, EAST),
        (WEST, NORTH, NORTH),
        (EAST, NORTH, SOUTH),
        (SOUTH, NORTH, WEST),
        (NORTH, SOUTH, WEST),
        (WEST, SOUTH, SOUTH),
        (EAST, SOUTH, NORTH),
        (SOUTH, SOUTH, EAST),
        (NORTH * 2, EAST, NORTH * 2),
        (NORTH * -5, NORTH, EAST * -5),
        (NORTH, NORTH_EAST, NORTH_EAST),
        (NORTH, SOUTH_WEST, SOUTH_WEST),
    ])
    def test_rotate_from_axe(self, vector, reference, expected):
        assert Geometry.transpose_rotation_relative_to(vector, reference) == expected
        # Reverse
        assert Geometry.transpose_rotation_relative_to(expected, Point(reference.x, - reference.y)) == vector


    def test_rotate_from_axe_with_null(self):
        # when
        vector = Point(0, 0)
        reference = NORTH_WEST
        assert Geometry.transpose_rotation_relative_to(vector, reference) == vector


    def test_rotate_from_axe_with_reference_null(self):
        # when
        vector = NORTH
        reference = Point(0, 0)
        with pytest.raises(ZeroDivisionError):
            Geometry.transpose_rotation_relative_to(vector, reference)


    @pytest.mark.parametrize("vector, axe, expected", [
        (NORTH, EAST, SOUTH),
        (NORTH, NORTH, NORTH),
        (NORTH, NORTH_EAST, EAST),
        (NORTH, SOUTH_WEST, EAST),
        (NORTH_EAST, NORTH, NORTH_WEST),
        (NORTH_EAST * 2.3, NORTH, NORTH_WEST * 2.3),
    ])
    def test_geometry_get_symmetrical(self, vector, axe, expected):
        assert expected == Geometry.get_symmetrical(vector, axe)

    @pytest.mark.parametrize("params",
                         [{"line0": Line(point=Point(0, 1), vector=Point(0, 1)),
                           "line1": Line(point=Point(3, 5), vector=Point(1, 0)),
                           "intersection": Point(0, 2)},
                          {"line0": Line(point=Point(0, 1), vector=Point(0, 1)),
                           "line1": Line(point=Point(5, 3), vector=Point(1, 0)),
                           "intersection": Point(0, -2)},
                          ])
    def test_get_tangent_point_from_lines(self, params):
        line0 = params['line0']
        line1 = params['line1']
        intersection = params['intersection']

        assert Geometry.get_tangent_point_from_lines(line0, line1) == intersection


    @pytest.mark.parametrize("params",
                             [
                                 {'point': Point(1, 0),
                                  'vector': Point(1, 0),
                                  'candidate': Point(3, 0),
                                  'expected': True},
                                 {'point': Point(1, 0),
                                  'vector': Point(1, 0),
                                  'candidate': Point(-3, 0),
                                  'expected': False},
                                 {'point': Point(1, 0),
                                  'vector': Point(1, 0),
                                  'candidate': Point(1, 1),
                                  'expected': False}

                             ])
    def test_is_beyond(self, params):
        point = params['point']
        vector = params['vector']
        candidate = params['candidate']
        expected = params['expected']
        assert Geometry.is_beyond_point(candidate, point, vector) == expected


class ProofOfConcepts:

    def test_find_angle_from_tangents_and_points(self):
        a = Point(1, 0)
        b = Point(0, 1)
        ta = Point(0, -1)
        tb = Point(1, 0)
        c = Point(0, 0)
        vk = (c - a).vectorial_product(ta)

        assert vk == 1

        def rotate_from_center(c, p, phi):
            radius = Point.distance(c, p)
            x = radius * math.cos(phi)
            y = radius * math.sin(phi)
            rotated = Point(x, y) + c
            return rotated

        rotated = rotate_from_center(c, a, math.pi / 2)
        assert rotated == b

        rotated = rotate_from_center(c, a, -3 * math.pi / 2)
        assert rotated == b



