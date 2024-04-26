from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Direction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIRECTION_UNKNOWN: _ClassVar[Direction]
    DIRECTION_UP: _ClassVar[Direction]
    DIRECTION_DOWN: _ClassVar[Direction]
    DIRECTION_LEFT: _ClassVar[Direction]
    DIRECTION_RIGHT: _ClassVar[Direction]
DIRECTION_UNKNOWN: Direction
DIRECTION_UP: Direction
DIRECTION_DOWN: Direction
DIRECTION_LEFT: Direction
DIRECTION_RIGHT: Direction

class GridCoord(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class Gridtangle(_message.Message):
    __slots__ = ("bottom_left", "top_right")
    BOTTOM_LEFT_FIELD_NUMBER: _ClassVar[int]
    TOP_RIGHT_FIELD_NUMBER: _ClassVar[int]
    bottom_left: GridCoord
    top_right: GridCoord
    def __init__(self, bottom_left: _Optional[_Union[GridCoord, _Mapping]] = ..., top_right: _Optional[_Union[GridCoord, _Mapping]] = ...) -> None: ...
