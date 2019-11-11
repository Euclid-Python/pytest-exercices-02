from ex02.robot import Transmitter
from ex02.telecom import Telecom, Command
import pytest
from pytest_mock import mocker


class TestTransmitter:

    @pytest.fixture()
    def init_transmitter(self, mocker):
        robot = mocker.Mock()
        robot.is_moving.return_value = False
        transmitter = Transmitter()
        transmitter.register(robot)
        return robot, transmitter

    def test_valid_fixture(self, init_transmitter):
        robot, tr = init_transmitter
        assert robot.is_moving() == False

    def test_send_tc_ready_for_loading(self, init_transmitter):
        # given
        robot, tr = init_transmitter
        tc = Telecom(command=Command.READY_FOR_LOADING)
        # when
        tm = tr.exchange(tc)
        # then
        assert tm.command == Command.READY_FOR_LOADING

    def test_send_tc_ready_for_loading_when_moving(self, init_transmitter):
        # given
        robot, tr = init_transmitter
        tc = Telecom(command=Command.READY_FOR_LOADING)
        # when
        robot.is_moving.return_value = True
        tm = tr.exchange(tc)
        # then
        assert tm.command == Command.MOVING

    def test_send_tc_on_loading_when_moving(self, init_transmitter):
        # given
        robot, tr = init_transmitter
        tc = Telecom(command=Command.LOADING)
        # when
        robot.is_moving.return_value = True
        tm = tr.exchange(tc)
        # then
        assert tm.command == Command.MOVING

    def test_send_tc_on_loading_without_payload(self, init_transmitter):
        # given
        robot, tr = init_transmitter
        tc = Telecom(command=Command.LOADING)
        # when
        tm = tr.exchange(tc)
        # then
        assert tm.command == Command.LOADED_INVALID

    def test_send_tc_on_loading_with_payload(self, init_transmitter):
        # given
        robot, tr = init_transmitter
        # when
        tc = Telecom(command=Command.LOADING, payload=['foo'])
        tm = tr.exchange(tc)
        # then
        assert tm.command == Command.LOADED_OK

    def test_send_tc_on_loading_when_robot_raise_error(self, init_transmitter):
        # given
        robot, tr = init_transmitter
        robot.load_positions.side_effect = ValueError('Mocked Exception')
        # when
        tc = Telecom(command=Command.LOADING, payload=['foo'])
        tm = tr.exchange(tc)
        # then
        assert tm.command == Command.LOADED_INVALID

    def test_send_tc_move_BUG(self, init_transmitter):
        # given
        robot, tr = init_transmitter
        # when
        robot.run.side_effect = ValueError("Mocked Exception")
        tc = Telecom(command=Command.MOVE)
        tm = tr.exchange(tc)
        # then
        assert tm.command == Command.INVALID

    def test_send_tc_move(self, init_transmitter):
        # given
        robot, tr = init_transmitter
        # when
        tc = Telecom(command=Command.MOVE)
        tm = tr.exchange(tc)
        # then
        assert tm.command == Command.MOVED

class TestFindHandler:
    class FooRobotComponent(Transmitter):

        def register(self, robot: 'Robot'):
            self.robot = dict()

        def _prefix_something(self):
            pass

        def _prefix_something_else(self):
            pass

    def test_find_handlers_for_suffix(self):
        # -- given --
        foo = TestFindHandler.FooRobotComponent()
        # -- when --
        results = Transmitter._find_handlers_for_suffix(foo, '_prefix_')
        # -- then --
        # keys are function postfix
        assert [t for t in results.keys()] == ['something', 'something_else']
        # values are functions
        assert any(callable(f) for f in results.values())
        # and names are the real names
        assert any(f.__name__.startswith('_prefix_') for f in results.values())
