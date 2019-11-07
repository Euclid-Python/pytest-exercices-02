import pytest

from ex02.robot import Robot, MotionController, Engine
from ex02.geometry import Point


class TestMotionController:

    @pytest.fixture()
    def init_controller(self, mocker):
        robot = mocker.Mock(spec=Robot)
        right_engine = mocker.Mock(spec=Engine)
        left_engine = mocker.Mock(spec=Engine)
        configuration = {}
        ctrl = MotionController(right_engine=right_engine,
                                left_engine=left_engine,
                                configuration=configuration)

        return ctrl, robot, right_engine, left_engine, configuration

    def test_convert_in_points(self, init_controller):
        # --given--
        ctrl, robot, _, _, _ = init_controller
        positions = [(1, 1), (10, 1), (11, 2), (10, 3), (1, 1)]

        points = ctrl.convert_in_points(positions)
        assert any(t[0] == t[1] for t in list(zip(points, positions)))

    def test_convert_in_motion_simple(self, init_controller):
        # --given--
        ctrl, robot, _, _, _ = init_controller
        positions = [(0, 0), (1, 1)]

        motions = ctrl.convert_in_motions(list(Point.new(xy) for xy in positions))
