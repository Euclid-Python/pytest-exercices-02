from ex02.geometry import Point
from ex02.robot import Move, Optimizer


class TestOptimization:

    def test_optimization(self):
        # --given--
        motions = [Move(Point(0, 0), Point(10, 0)), Move(Point(10, 0), Point(10, 10))]
        optimizer = Optimizer()
        # --when--
        result = optimizer.optimize(motions)
        # --then--
        assert len(result) == len(motions) + 1
