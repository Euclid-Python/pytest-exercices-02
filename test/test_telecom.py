from ex02.telecom import Telecommunication, Kind, Command


class TestEnum:

    def test_enum(self):
        assert 'MOTION' in Kind.__members__


class TestNewCommand:

    def test_new_telecom(self):
        tc = Telecommunication.new_command(kind=Kind.MOTION, command=Command.READY_FOR_LOADING)


