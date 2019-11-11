import pytest

from ex02.geometry import Point
from ex02.robot import Arranger, CurveArranger
from ex02.motion import Translation, Rotation


class TestBaseArranger:

    def test_optimization(self):
        # --given--
        motions = [Translation(Point(0, 0), Point(10, 0)), Translation(Point(10, 0), Point(10, 10))]
        arranger = Arranger()
        # --when--
        result = arranger.arrange(motions)
        # --then--
        assert len(result) == len(motions) + 1
        assert isinstance(result[1], Rotation)

def is_rotation(r):
    return isinstance(r, Rotation)

def is_on_the_spot(r):
    return is_rotation(r) and r.is_on_the_spot()


def get_simple_rotations_indices(motions):
    return [idx for idx, t in enumerate(motions)
     if is_rotation(t) and not is_on_the_spot(t)]


def get_on_the_spot_indices(arranged_motions):
    return [idx for idx, t in enumerate(arranged_motions)
     if is_on_the_spot(t)]


class TestCurveArranger:

    @staticmethod
    def to_translation(points):
        translations = []
        start = points[0]
        for p in points[1:]:
            translations.append(Translation(start, p))
            start = p
        return translations

    def test_base(self):
        points = [(0,0), (0,5),(1,8),(3,9),(5,8), (7,5), (6,0),(0,0)]
        motions = self.__class__.to_translation(list(Point.new(xy) for xy in points))
        # -- when --
        arranger = CurveArranger()
        arranged_motions = arranger.arrange(motions)

        assert (any(isinstance(t, Rotation) for t in arranged_motions))

        on_the_spot_positions = get_on_the_spot_indices(arranged_motions)
        simple_rotation_positions = get_simple_rotations_indices(arranged_motions)

        assert on_the_spot_positions == [4, 9]
        assert simple_rotation_positions == [2,7]

    @pytest.mark.parametrize('points, size, indices_on_spot, indices_simple',[
        ([(0,0), (1,5), (3,7), (5,5),(6,0)], 6, [4],[2]),
        ([(0,0), (1,5),(3,5),(4,0),(0,0)], 6, [1], [4]),
        ([(0, 0), (1, 5), (2, 6), (4, 0),(1,0)], 6, [4], [2])
    ])
    def test_simple_rotation(self, points, size, indices_on_spot, indices_simple):
        motions = self.__class__.to_translation(list(Point.new(xy) for xy in points))

        arranger = CurveArranger()
        arranged_motions = arranger.arrange(motions)

        assert(len(arranged_motions)) == size

        on_the_spot_positions = get_on_the_spot_indices(arranged_motions)
        simple_rotation_positions = get_simple_rotations_indices(arranged_motions)

        assert on_the_spot_positions == indices_on_spot
        assert simple_rotation_positions == indices_simple
