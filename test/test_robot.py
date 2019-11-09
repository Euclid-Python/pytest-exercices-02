import pytest
import pytest_mock

from ex02.robot import Robot, Transmitter, MotionController, Navigator, EnergySupplier
from ex02.telecom import Telecom, Command


class TestRobot:

    @pytest.fixture()
    def init_robot(self, mocker):
        transmitter = mocker.Mock(spec=Transmitter)
        motion_controller = mocker.Mock(spec=MotionController)
        navigator = mocker.Mock(spec=Navigator)
        energy_supplier = mocker.Mock(spec=EnergySupplier)

        robot = Robot(transmitter=transmitter,
                      motion_controller=motion_controller,
                      navigator=navigator,
                      energy_supplier=energy_supplier)

        return robot, transmitter, motion_controller, navigator, energy_supplier



    def test_robot_is_moving_default_not(self, init_robot):
        # -- given --
        robot, *_ = init_robot
        # -- then --
        assert not robot.is_moving()

    def test_robot_is_moving(self, init_robot):
        # -- given --
        robot, *_ = init_robot
        # -- when --
        robot.status = Robot.STATUS_MOVING
        # -- then --
        assert robot.is_moving()

    def test_robot_is_moving(self, init_robot):
        # -- given --
        robot, *_ = init_robot
        # -- when --
        robot.status = Robot.STATUS_MOVING
        # -- then --
        assert robot.is_moving()

    def test_robot_exchange_through_transmitter(self, init_robot):
        # -- given --
        robot, transmitter, *_ = init_robot
        # -- when --
        robot.exchange(Telecom(command=Command.MOVING))
        # -- then --
        transmitter.exchange.assert_called_once()