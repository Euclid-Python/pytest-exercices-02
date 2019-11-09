import math

from ex02.motion import Translation, Rotation
from ex02.telecom import Telecom, Exchanger
import inspect
from typing import List

from ex02.telecom import Command
from ex02.geometry import Point, Arc


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

class Transmitter(RobotComponent, Exchanger):

    def __init__(self):
        super().__init__()
        self._handlers = self._find_handlers_for_suffix(self, '_on_')

    @staticmethod
    def _find_handlers_for_suffix(instance, prefix):
        """
        Find methods starting with prefix
        :param instance:
        :param prefix:
        :return: a dictionary of functions indexed by postfix
        """

        def name(fn, prefix_):
            return fn[0][len(prefix_):]

        def match(fn, prefix_):
            return fn[0].startswith(prefix_)

        return {name(fn, prefix): getattr(instance, fn[0])
                for fn in inspect.getmembers(instance, inspect.ismethod)
                if match(fn, prefix)}

    """
    Transmitter Class
    """

    def exchange(self, tc: Telecom) -> Telecom:
        cmd = tc.command
        method = self._handlers[cmd.name]
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

    def _on_MOVE(self, tc: Telecom) -> Telecom:
        if self.robot.is_moving():
            return Telecom(command=Command.MOVING)
        # -----------------------------------------
        # TO BE DEVELOPPED
        # ------------------------------------------

class Wheel:

    def run(self, length):
        pass

class EnergySupplier(RobotComponent):
    """Energy supplier is an energy tank"""

    def __init__(self, quantity: float = 1000.0):
        self.quantity = quantity

    def consume(self, quantity: float) -> float:
        self.quantity = self.quantity - quantity

    def has_enough(self, quantity: float) -> float:
        return quantity < self.quantity


class MotionController(RobotComponent):
    CONSUMPTION_PER_LENGTH_UNIT = 1
    DEFAULT_WHEEL_AXIS_LENGTH = 1
    DEFAULT_TIME_STEP = 0.1
    DEFAULT_SPEED = 0.1

    def __init__(self, right_wheel: Wheel, left_wheel: Wheel, configuration):
        self.right_wheel = right_wheel
        self.left_wheel = left_wheel

        self.speed = configuration.get('speed', MotionController.DEFAULT_SPEED)
        self.time_step = configuration.get('time_step', MotionController.DEFAULT_TIME_STEP)
        self.consumption_per_length_unit = configuration.get('consumption_per_length_unit',
                                                             MotionController.CONSUMPTION_PER_LENGTH_UNIT)
        self.configuration = configuration
        super().__init__()

    def run_translation(self, translation: 'Translation', energy_supplier: 'EnergySupplier'):
        """
        Runs translation
        :param translation:
        :param energy_supplier: EnergySupplier to supply energy for translation
        :return:
        """
        length = translation.length
        steps, length_step, duration = self._compute_step_param(length)
        consumption_per_step = self.get_required_energy_for(length_step)

        for s in range(steps):
            self.right_wheel.run(length_step)
            self.left_wheel.run(length_step)
            energy_supplier.consume(2 * consumption_per_step)

    def run_rotation(self, rotation: 'Rotation', energy_supplier: 'EnergySupplier'):
        """
        Runs rotation
        :param rotation:
        :param energy_supplier:
        :return:
        """
        wheel_axis = self.configuration.get('wheel_axis_length', MotionController.DEFAULT_WHEEL_AXIS_LENGTH)

        if rotation.is_on_the_spot():
            self._run_rotation_on_spot(rotation, wheel_axis, energy_supplier)
        else:
            self._run_rotation_on_center(rotation, wheel_axis, energy_supplier)

    def _compute_step_param(self, length):
        duration = length / self.speed
        steps = math.floor(duration / self.time_step)
        length_step = length / steps
        return steps, length_step, duration

    def move(self, motion, energy_supplier):
        if isinstance(motion, Translation):
            self.run_translation(motion, energy_supplier)
        elif isinstance(motion, Rotation):
            self.run_rotation(motion, energy_supplier)
        else:
            raise ValueError(f"Motion {motion} can not be understood")

    def _run_rotation_on_spot(self, rotation, wheel_axis, energy_supplier):
        angle = rotation.arc.angle
        length = angle * wheel_axis / 2
        steps, length_step, duration = self._compute_step_param(length)
        consumption_per_step = self.get_required_energy_for(length_step)

        for s in range(steps):
            self.right_wheel.run(length_step)
            self.left_wheel.run(-length_step)
            energy_supplier.consume(2 * consumption_per_step)

    def _run_rotation_on_center(self, rotation, wheel_axis, energy_supplier):
        angle = rotation.arc.angle
        radius = rotation.arc.radius

        big_radius = (radius + wheel_axis / 2)
        sho_radius = (radius - wheel_axis / 2)

        big_length = big_radius * angle

        ratio = sho_radius / big_radius

        steps, length_step, duration = self._compute_step_param(big_length)

        right_len_step = length_step
        left_len_step = length_step

        if rotation.arc.direction == Arc.DIRECT:
            left_len_step = ratio * length_step
        else:
            right_len_step = ratio * length_step

        consumption_per_step = self.get_required_energy_for(left_len_step) \
                               + self.get_required_energy_for(right_len_step)

        for s in range(steps):
            self.right_wheel.run(right_len_step)
            self.left_wheel.run(left_len_step)
            energy_supplier.consume(consumption_per_step)

    def get_required_energy_for(self, length: float):
        return self.consumption_per_length_unit * length


class Navigator(RobotComponent):

    def __init__(self, arranger: 'Arranger'):
        self.arranger = arranger

    def compute_motions(self, positions):
        points = self.to_points(positions)
        motions = self.to_translations(points)
        new_motions = self.arrange_translations(motions)
        return new_motions

    def compute_total_distance(self, motions):
        return super(len(m) for m in motions)

    def arrange_translations(self, translations):
        return self.arranger.arrange(translations)

    def to_points(self, positions):
        return list([Point.new(xy) for xy in positions])

    def to_translations(self, points):
        """
        Converts points into motion collection
        :param points:
        :return: translation collection
        """
        translations = []
        start = points[0]
        for p in points[1:]:
            translations.append(Translation(start, p))
            start = p
        return translations


class Arranger:

    def arrange(self, motions: List) -> List:
        new_motions = []
        previous_move = None
        for move in motions:
            if previous_move:
                if not previous_move.is_parallel_with(move):
                    rotation = Rotation.new_from_translations(previous_move, move)
                    new_motions.append(rotation)
            previous_move = move
            new_motions.append(move)
        return new_motions


class Robot:
    STATUS_MOTIONLESS = 'motionless'
    STATUS_MOVING = 'moving'

    def __init__(self, transmitter: Transmitter,
                 motion_controller: MotionController,
                 navigator: Navigator,
                 energy_supplier: EnergySupplier):
        self.transmitter = transmitter
        self.motion_controller = motion_controller
        self.navigator = navigator
        self.energy_supplier = energy_supplier
        self._register_components()
        self.status = None
        self.motions = []

    def _register_components(self):
        self.transmitter.register(self)
        self.motion_controller.register(self)
        self.navigator.register(self)
        self.energy_supplier.register(self)

    def load_positions(self, positions: List):
        motions = self.navigator.compute_motions(positions)
        total_length = self.navigator.compute_total_distance(motions)
        total_energy = self.motion_controller.get_required_energy_for(total_length)
        if not self.energy_supplier.has_enough(total_energy):
            raise ValueError("Not enough energy")
        self.motions = motions

    def run(self):
        if len(self.motions) > 0:
            self.status = Robot.STATUS_MOVING
            for motion in self.motions:
                self.motion_controller.move(motion)
            self.status = Robot.STATUS_MOTIONLESS
        else:
            raise ValueError("Empty motion list")

    def is_moving(self):
        return self.status is Robot.STATUS_MOVING
