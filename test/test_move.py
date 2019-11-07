import math

from ex02.geometry import Point
from ex02.robot import Move, Rotation


class testMove:

    def test_move_creation(self):
        m = Move(Point.new((1, 1)))
        assert m.start == 1.0
        assert m.end == 1.0
        assert m.length == math.sqrt(2)
        assert m.vector == Point(math.sqrt(1 / 2), math.sqrt(1 / 2))
