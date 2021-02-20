from abc import ABC
from typing import Any, ClassVar
from enum import Enum


class Types(Enum):
    Str = str
    Int = int


class Validator(ABC):
    pass


class Guard(Validator):
    def __init__(self):
        pass

    @staticmethod
    def is_type(value: Any, var_type: ClassVar) -> None:
        if not is_type(value, var_type):
            raise Exception('Value is not a valid {}'.format(var_type))


def is_type(value: Any, var_type: ClassVar) -> bool:
    if var_type is Types.Str:
        return type(value) is str

    if var_type is Types.Int:
        return type(value) is int

    return False
