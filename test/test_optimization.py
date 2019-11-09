from ex02.geometry import Point
from ex02.robot import Arranger
from ex02.motion import Translation, Rotation


class TestOptimization:

    def test_optimization(self):
        # --given--
        motions = [Translation(Point(0, 0), Point(10, 0)), Translation(Point(10, 0), Point(10, 10))]
        optimizer = Arranger()
        # --when--
        result = optimizer.arrange(motions)
        # --then--
        assert len(result) == len(motions) + 1
        assert isinstance(result[1], Rotation)
