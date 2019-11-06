from ex02.robot import Transmitter
from ex02.telecom import Telecommunication, Kind, Command
import pytest
from pytest_mock import mocker

new_command = Telecommunication.new_command


class TestTransmitter:

    @pytest.fixture()
    def init_transmitter(self, mocker):
        robot = mocker.Mock()
        transmitter = Transmitter()
        transmitter.register(robot)
        return robot, transmitter

    def test_transmitter_instantiation(self, init_transmitter):
        robot, tr = init_transmitter
        assert robot is not None and tr is not None

    def test_send_tc_ready_for_loading(self, init_transmitter):
        # given
        robot, tr = init_transmitter
        tc = new_command(kind=Kind.MOTION, command=Command.READY_FOR_LOADING)
        # when
        tm = tr.exchange(tc)
        # then
        assert tm['command'] == Command.READY_FOR_LOADING

    def test_send_tc_ready_for_loading_when_moving(self, init_transmitter):
        # given
        robot, tr = init_transmitter
        tc = new_command(kind=Kind.MOTION, command=Command.READY_FOR_LOADING)
        # when
        robot.is_moving.return_value = False
        tm = tr.exchange(tc)
        # then
        assert tm['command'] == Command.MOVING


