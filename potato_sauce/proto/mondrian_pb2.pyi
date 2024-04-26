from potato_sauce.proto import geom_pb2 as _geom_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ThinRectStrategy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THIN_RECT_UNSPECIFIED: _ClassVar[ThinRectStrategy]
    THIN_RECT_SUBSUME: _ClassVar[ThinRectStrategy]
    THIN_RECT_IGNORE: _ClassVar[ThinRectStrategy]
THIN_RECT_UNSPECIFIED: ThinRectStrategy
THIN_RECT_SUBSUME: ThinRectStrategy
THIN_RECT_IGNORE: ThinRectStrategy

class SceneSpec(_message.Message):
    __slots__ = ("bounding_box", "components", "scale_by", "thin_rect_strategy")
    BOUNDING_BOX_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    SCALE_BY_FIELD_NUMBER: _ClassVar[int]
    THIN_RECT_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    bounding_box: _geom_pb2.Gridtangle
    components: _containers.RepeatedCompositeFieldContainer[SceneComponent]
    scale_by: int
    thin_rect_strategy: ThinRectStrategy
    def __init__(self, bounding_box: _Optional[_Union[_geom_pb2.Gridtangle, _Mapping]] = ..., components: _Optional[_Iterable[_Union[SceneComponent, _Mapping]]] = ..., scale_by: _Optional[int] = ..., thin_rect_strategy: _Optional[_Union[ThinRectStrategy, str]] = ...) -> None: ...

class Color(_message.Message):
    __slots__ = ("red", "green", "blue", "alpha")
    RED_FIELD_NUMBER: _ClassVar[int]
    GREEN_FIELD_NUMBER: _ClassVar[int]
    BLUE_FIELD_NUMBER: _ClassVar[int]
    ALPHA_FIELD_NUMBER: _ClassVar[int]
    red: int
    green: int
    blue: int
    alpha: int
    def __init__(self, red: _Optional[int] = ..., green: _Optional[int] = ..., blue: _Optional[int] = ..., alpha: _Optional[int] = ...) -> None: ...

class SceneComponent(_message.Message):
    __slots__ = ("locations", "exclude_locations", "tiling_config")
    LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    TILING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    locations: _containers.RepeatedCompositeFieldContainer[_geom_pb2.Gridtangle]
    exclude_locations: _containers.RepeatedCompositeFieldContainer[_geom_pb2.Gridtangle]
    tiling_config: TilingConfig
    def __init__(self, locations: _Optional[_Iterable[_Union[_geom_pb2.Gridtangle, _Mapping]]] = ..., exclude_locations: _Optional[_Iterable[_Union[_geom_pb2.Gridtangle, _Mapping]]] = ..., tiling_config: _Optional[_Union[TilingConfig, _Mapping]] = ...) -> None: ...

class TilingConfig(_message.Message):
    __slots__ = ("fill_colors", "border_color", "shade_out_of_bounds", "edge_sizes", "edge_size_combinations")
    FILL_COLORS_FIELD_NUMBER: _ClassVar[int]
    BORDER_COLOR_FIELD_NUMBER: _ClassVar[int]
    SHADE_OUT_OF_BOUNDS_FIELD_NUMBER: _ClassVar[int]
    EDGE_SIZES_FIELD_NUMBER: _ClassVar[int]
    EDGE_SIZE_COMBINATIONS_FIELD_NUMBER: _ClassVar[int]
    fill_colors: _containers.RepeatedCompositeFieldContainer[Color]
    border_color: Color
    shade_out_of_bounds: bool
    edge_sizes: _containers.RepeatedScalarFieldContainer[int]
    edge_size_combinations: _containers.RepeatedCompositeFieldContainer[RectTargetSize]
    def __init__(self, fill_colors: _Optional[_Iterable[_Union[Color, _Mapping]]] = ..., border_color: _Optional[_Union[Color, _Mapping]] = ..., shade_out_of_bounds: bool = ..., edge_sizes: _Optional[_Iterable[int]] = ..., edge_size_combinations: _Optional[_Iterable[_Union[RectTargetSize, _Mapping]]] = ...) -> None: ...

class RectTargetSize(_message.Message):
    __slots__ = ("width", "height")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...
