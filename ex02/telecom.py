from abc import ABC, abstractmethod
from enum import (Enum)
from typing import Dict


class Kind(Enum):
    """
    Enumeration for telecom kinds.
    """
    MOTION = 'motion'


class Command(Enum):
    """
    Enumeration for telecom commands.
    """
    READY_FOR_LOADING = 'ready_for_loading'
    MOVING = 'moving'
    LOADING = 'loading'
    LOADED_OK = 'loaded_ok'
    LOADED_INVALID = 'loaded_invalid'
    MOVE = 'move'
    MOVED = 'moved'


class Telecommunication(object):

    @classmethod
    def new_command(cls, kind: Kind, command: Command, payload=None, errors=None):
        assert isinstance(kind, Kind)
        assert isinstance(command, Command)

        tc = {'kind': kind, 'command': command}
        if payload is not None:
            tc['payload'] = payload
        if errors is not None:
            tc['errors'] = errors

        return tc


class Exchanger(ABC):

    @abstractmethod
    def exchange(self, tm: Dict) -> Dict:
        pass
