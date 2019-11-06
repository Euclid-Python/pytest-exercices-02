from ex02.robot import RobotComponent
from ex02.robot import Robot


class FooRobotComponent(RobotComponent):

    def register(self, robot: 'Robot'):
        self.robot = dict()

class TestRobotComponent:

    def test_foo(self):
        foo = FooRobotComponent()