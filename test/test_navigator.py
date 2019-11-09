import pytest

from ex02.geometry import Point
from ex02.robot import Robot, Arranger, Navigator
from ex02.motion import Translation


class TestNavigator:

    @pytest.fixture()
    def init_controller(self, mocker):
        robot = mocker.Mock(spec=Robot)
        optimizer = mocker.Mock(spec=Arranger)
        nav = Navigator(arranger=optimizer)

        return nav, robot, optimizer


    @pytest.fixture()
    def convert_to_points(self):
        def convert(positions):
            return list(Point.new(xy) for xy in positions)
        return convert

    def test_convert_in_points(self, init_controller):
        # --given--
        nav, robot, *_ = init_controller
        positions = [(1, 1), (10, 1), (11, 2), (10, 3), (1, 1)]

        points = nav.to_points(positions)
        assert any(t[0] == t[1] for t in list(zip(points, positions)))

    def test_convert_in_motion_simple(self, init_controller):
        # --given--
        nav, robot, *_ = init_controller
        positions = [(0, 0), (1, 1)]
        # --when--
        motions = nav.to_translations(list(Point.new(xy) for xy in positions))
        # --then--
        assert len(motions) == 1


    def test_convert_in_motion_5_points(self, init_controller, convert_to_points):
        # --given--
        nav, robot, *_ = init_controller
        positions = [(0, 0), (1, 1), (3,1), (3,0), (0,0)]
        # --when--
        motions = nav.to_translations(convert_to_points(positions))
        # --then--
        assert len(motions) == 4


    def test_optimize_motions(self, init_controller, convert_to_points):
        # --given--
        nav, robot, optimizer, *_ = init_controller
        motions = [Translation(Point(0, 0), Point(10, 0)), Translation(Point(10, 0), Point(10, 10))]
        # --when--
        results = nav.arrange_translations(motions)
        # --then--
        optimizer.arrange.assert_called()
