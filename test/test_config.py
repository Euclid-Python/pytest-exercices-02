from ex02.robot import Robot

class Foo:
    def bar(self):
        return "ok"

def test_its_ok():
    assert Robot is not None

def test_fn():
    fn = getattr(Foo,'bar')
    foo = Foo()
    assert fn(foo) == "ok"