import math

from ex02.geometry import Point
from ex02.robot import Translation, Rotation


class TestMove:

    def test_move_creation(self):
        m = Translation(Point.new((0, 0)), Point.new((1, 1)))
        assert m.start == Point.new((0, 0))
        assert m.end == Point.new((1, 1))
        assert m.length == math.sqrt(2)
        assert m.vector == Point(math.sqrt(1 / 2), math.sqrt(1 / 2))


class TestRotation:

    def test_rotation(self):
        prev_ = Translation(Point(0, 0), Point(10, 0))
        next_ = Translation(Point(10, 10), Point(0, 10))

        rot = Rotation.new_from_move(prev_, next_)
        assert rot.arc.center == Point(10,5)
        assert rot.arc.radius == 5