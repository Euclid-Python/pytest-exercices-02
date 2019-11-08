from ex02.telecom import Telecom, Exchanger
import inspect
from typing import List, Dict

from ex02.telecom import Command
from ex02.geometry import Point, Segment, Arc


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

    @staticmethod
    def find_handlers_for_suffix(instance, prefix):
        """
        Find methods starting with prefix
        :param instance:
        :param prefix:
        :return: a dictionary of functions indexed by postfix
        """

        def name(fn, prefix):
            return fn[0][len(prefix):]

        def match(fn, prefix):
            return fn[0].startswith(prefix)

        return {name(fn, prefix): getattr(instance, fn[0])
                for fn in inspect.getmembers(instance, inspect.ismethod)
                if match(fn, prefix)}


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

    def load_positions(self, motions: List):
        pass

    def is_moving(self):
        return self.status is Robot.STATUS_MOVING


class Transmitter(RobotComponent, Exchanger):

    def __init__(self):
        super().__init__()
        self.handlers = self.find_handlers_for_suffix(self, '_on_')

    """
    Transmitter Class
    """

    def exchange(self, tc: Telecom) -> Telecom:
        cmd = tc.command
        method = self.handlers[cmd.name]
        return method(tc)

    def _on_READY_FOR_LOADING(self, tc: Telecom) -> Telecom:
        if self.robot.is_moving():
            return Telecom(command=Command.MOVING)
        return Telecom(command=tc.command)

    def _on_LOADING(self, tc: Telecom) -> Telecom:
        if self.robot.is_moving():
            return Telecom(command=Command.MOVING)

        if not tc.payload:
            return Telecom(command=Command.LOADED_INVALID, errors=['no payload'])

        try:
            self.robot.load_positions(tc.payload)
            return Telecom(command=Command.LOADED_OK)
        except Exception as e:
            return Telecom(command=Command.LOADED_INVALID, errors=[str(e)])


class Wheel:
    pass


class Engine:

    def __init__(self, wheel: Wheel):
        self.wheel = wheel

    def run(self, length: float):
        self.wheel.run(length)


class EnergySupplier:

    def __init__(self, quantity: float = 1000.0):
        self.quantity = quantity


class MotionController(RobotComponent):

    def __init__(self, right_engine: Engine, left_engine: Engine, optimizer: 'Optimizer', configuration):
        self.right_engine = right_engine
        self.left_engine = left_engine
        self.optimizer = optimizer
        self.configuration = configuration
        super().__init__()

    def compute_motions(self, positions):
        points = self.convert_in_points(positions)
        motions = self.convert_in_motions(points)
        new_motions = self.optimize_motions(motions)
        return new_motions

    def convert_in_points(self, positions):
        return list([Point.new(xy) for xy in positions])

    def convert_in_motions(self, points):
        """
        Converts points into motion collection
        :param points:
        :return: segment collection
        """
        motions = []
        start = points[0]
        for p in points[1:]:
            motions.append(Translation(start, p))
            start = p
        return motions

    def optimize_motions(self, motions):
        return self.optimizer.optimize(motions)

    def run_translation(self, translation: 'Translation'):
        length = translation.length
        self.right_engine.run(length)
        self.left_engine.run(length)

    def run_rotation(self, rotation: 'Rotation'):
        if rotation.is_on_the_spot():
            pass





class Optimizer:

    def optimize(self, motions: List) -> List:
        new_motions = []
        previous_move = None
        for move in motions:
            if previous_move:
                if not previous_move.is_parallel_with(move):
                    rotation = Rotation.new_from_move(previous_move, move)
                    new_motions.append(rotation)
            previous_move = move
            new_motions.append(move)
        return new_motions

class Translation:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = self.get_length()
        self.vector = (end - start).normalize()

    def get_length(self):
        return Point.distance(self.start, self.end)

    def is_parallel_with(self, other: 'Translation'):
        return self.vector.is_collinear(other.vector)


class Rotation:

    def __init__(self, start: Point, end: Point, start_vector: Point, end_vector: Point):
        self.arc = Arc(start, end, start_vector, end_vector)


    def is_on_the_spot(self) -> bool :
        """
        Indicates if rotation is on _the spot, i.e. with a radius == 0
        :return: True if is on the spot
        """
        return self.arc.radius == 0

    @classmethod
    def new_from_move(cls, previous_move, move):
        return Rotation(previous_move.end, move.start, previous_move.vector, move.vector)
