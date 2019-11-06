from ex02.telecom import Telecommunication, Exchanger
import inspect
from typing import List, Dict

from ex02.telecom import Command


class RobotComponent:
    """
    Class for robot's component needing direct access to robot instance.
    """

    def __init__(self):
        self.robot = None

    def register(self, robot: 'Robot'):
        """
        Registers component to robot
        :param robot:
        :return:
        """
        self.robot = robot


    def find_handlers_for_suffix(self, prefix):
        """
        Find methods starting with prefix
        :param prefix:
        :return: a dictionnary of functions
        """

        def fname(fn, prefix):
            return fn[0][len(prefix):]

        def is_func(fn, prefix):
            return fn[0].startswith(prefix)

        return {fname(fn, prefix): getattr(self, fn[0])
                for fn in inspect.getmembers(self, inspect.ismethod)
                if is_func(fn, prefix)}


class Robot:

    STATUS_MOVING = 'moving'

    def __init__(self, transmitter: 'Transmitter', motion_controller: 'MotionController'):
        self.transmitter = transmitter
        self.motion_controller = motion_controller
        self.register_components()
        self.status = None

    def register_components(self):
        self.transmitter.register(self)
        self.motion_controller.register(self)

    def is_moving(self):
        return self.status is Robot.STATUS_MOVING


class Transmitter(RobotComponent, Exchanger):

    def __init__(self):
        super().__init__()
        self.handlers = self.find_handlers_for_suffix('_on_')

    """
    Transmitter Class
    """

    def exchange(self, tc: Dict) -> Dict:
        cmd = tc['command']
        method = self.handlers[cmd.name]
        return method(tc)

    def _on_READY_FOR_LOADING(self, tc: Dict) -> Dict:
        if self.robot.is_moving():
            return Telecommunication.new_command(kind=tc['kind'],command=tc['command'])
        return Telecommunication.new_command(kind=tc['kind'],command=Command.MOVING)

class Wheel:
    pass


class Engine:

    def __init__(self, wheel: Wheel):
        self.wheel = wheel


class EnergySupplier:

    def __init__(self, quantity: float = 1000.0):
        self.quantity = quantity


class MotionController(RobotComponent):

    def __init__(self, right_engine: Engine, left_engine: Engine, configuration):
        self.right_engine = right_engine
        self.left_engine = left_engine
        self.configuration = configuration
        super().__init__()
