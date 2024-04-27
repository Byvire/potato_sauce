from potato_sauce.proto import geom_pb2 as _geom_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LevelConfig(_message.Message):
    __slots__ = ("ascii_file", "rule_zones")
    ASCII_FILE_FIELD_NUMBER: _ClassVar[int]
    RULE_ZONES_FIELD_NUMBER: _ClassVar[int]
    ascii_file: str
    rule_zones: _containers.RepeatedCompositeFieldContainer[RuleZone]
    def __init__(self, ascii_file: _Optional[str] = ..., rule_zones: _Optional[_Iterable[_Union[RuleZone, _Mapping]]] = ...) -> None: ...

class RuleZone(_message.Message):
    __slots__ = ("location", "gravity_direction", "player")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    GRAVITY_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    PLAYER_FIELD_NUMBER: _ClassVar[int]
    location: _geom_pb2.Gridtangle
    gravity_direction: _geom_pb2.Direction
    player: int
    def __init__(self, location: _Optional[_Union[_geom_pb2.Gridtangle, _Mapping]] = ..., gravity_direction: _Optional[_Union[_geom_pb2.Direction, str]] = ..., player: _Optional[int] = ...) -> None: ...
