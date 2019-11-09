from unittest.mock import call

import pytest

from ex02.robot import Robot, MotionController, Engine, Rotation, Translation, Optimizer
from ex02.geometry import Point


class TestMotionController:

    @pytest.fixture()
    def init_controller(self, mocker):
        robot = mocker.Mock(spec=Robot)
        right_engine = mocker.Mock(spec=Engine)
        left_engine = mocker.Mock(spec=Engine)
        optimizer = mocker.Mock(spec=Optimizer)
        configuration = {}
        ctrl = MotionController(right_engine=right_engine,
                                left_engine=left_engine,
                                optimizer=optimizer,
                                configuration=configuration)

        return ctrl, robot, optimizer, right_engine, left_engine, configuration

    @pytest.fixture()
    def convert_to_points(self):
        def convert(positions):
            return list(Point.new(xy) for xy in positions)
        return convert

    def test_convert_in_points(self, init_controller):
        # --given--
        ctrl, robot, *_ = init_controller
        positions = [(1, 1), (10, 1), (11, 2), (10, 3), (1, 1)]

        points = ctrl.convert_in_points(positions)
        assert any(t[0] == t[1] for t in list(zip(points, positions)))

    def test_convert_in_motion_simple(self, init_controller):
        # --given--
        ctrl, robot, *_ = init_controller
        positions = [(0, 0), (1, 1)]
        # --when--
        motions = ctrl.convert_in_motions(list(Point.new(xy) for xy in positions))
        # --then--
        assert len(motions) == 1


    def test_convert_in_motion_5_points(self, init_controller, convert_to_points):
        # --given--
        ctrl, robot, *_ = init_controller
        positions = [(0, 0), (1, 1), (3,1), (3,0), (0,0)]
        # --when--
        motions = ctrl.convert_in_motions( convert_to_points(positions))
        # --then--
        assert len(motions) == 4


    def test_optimize_motions(self, init_controller, convert_to_points):
        #--given--
        ctrl, robot, optimizer, *_ = init_controller
        motions = [Translation(Point(0, 0), Point(10, 0)), Translation(Point(10, 0), Point(10, 10))]
        #--when--
        results = ctrl.optimize_motions(motions)
        #--then--
        optimizer.optimize.assert_called()


    def test_translation(self, init_controller):
        #--given--
        ctrl, robot, optimizer, right_engine, left_engine, *_ = init_controller
        tr = Translation(Point(0, 0), Point(10, 0))
        # --when--
        ctrl.run_translation(tr)
        right_engine.run.assert_called_with(10.)
        left_engine.run.assert_called_with(10.)
