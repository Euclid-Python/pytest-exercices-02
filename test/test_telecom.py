from ex02.telecom import Telecom, Command



class TestNewCommand:

    def test_new_telecom(self):
        tc = Telecom(command=Command.READY_FOR_LOADING)


