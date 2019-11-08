from ex02.geometry import Point
from ex02.robot import Translation, Optimizer, Rotation


class TestOptimization:

    def test_optimization(self):
        # --given--
        motions = [Translation(Point(0, 0), Point(10, 0)), Translation(Point(10, 0), Point(10, 10))]
        optimizer = Optimizer()
        # --when--
        result = optimizer.optimize(motions)
        # --then--
        assert len(result) == len(motions) + 1
        assert isinstance(result[1], Rotation)
