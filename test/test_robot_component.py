from ex02.robot import RobotComponent
from ex02.robot import Robot


class TestRobotComponent:

    class FooRobotComponent(RobotComponent):

        def register(self, robot: 'Robot'):
            self.robot = dict()

        def _prefix_something(self):
            pass

        def _prefix_something_else(self):
            pass

    def test_find_handlers_for_suffix(self):
        # -- given --
        foo = TestRobotComponent.FooRobotComponent()
        # -- when --
        results = RobotComponent.find_handlers_for_suffix(foo,'_prefix_')
        # -- then --
        # keys are function postfix
        assert [t for t in results.keys()] == ['something', 'something_else']
        # values are functions
        assert any(callable(f) for f in results.values())
        # and names are the real names
        assert any(f.__name__.startswith('_prefix_') for f in results.values())