from potato_sauce.proto import geom_pb2 as _geom_pb2
from potato_sauce.proto import mondrian_pb2 as _mondrian_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Maze(_message.Message):
    __slots__ = ("rects", "background", "start", "goal", "bounding_box", "par_info", "color", "colorblind_background", "colorblind_color", "quality", "difficulty")
    RECTS_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    BOUNDING_BOX_FIELD_NUMBER: _ClassVar[int]
    PAR_INFO_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    COLORBLIND_BACKGROUND_FIELD_NUMBER: _ClassVar[int]
    COLORBLIND_COLOR_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    rects: _containers.RepeatedCompositeFieldContainer[_geom_pb2.Gridtangle]
    background: Graphic
    start: _geom_pb2.Gridtangle
    goal: _geom_pb2.Gridtangle
    bounding_box: _geom_pb2.Gridtangle
    par_info: ParInfo
    color: ColorInfo
    colorblind_background: Graphic
    colorblind_color: ColorInfo
    quality: MazeQuality
    difficulty: str
    def __init__(self, rects: _Optional[_Iterable[_Union[_geom_pb2.Gridtangle, _Mapping]]] = ..., background: _Optional[_Union[Graphic, _Mapping]] = ..., start: _Optional[_Union[_geom_pb2.Gridtangle, _Mapping]] = ..., goal: _Optional[_Union[_geom_pb2.Gridtangle, _Mapping]] = ..., bounding_box: _Optional[_Union[_geom_pb2.Gridtangle, _Mapping]] = ..., par_info: _Optional[_Union[ParInfo, _Mapping]] = ..., color: _Optional[_Union[ColorInfo, _Mapping]] = ..., colorblind_background: _Optional[_Union[Graphic, _Mapping]] = ..., colorblind_color: _Optional[_Union[ColorInfo, _Mapping]] = ..., quality: _Optional[_Union[MazeQuality, _Mapping]] = ..., difficulty: _Optional[str] = ...) -> None: ...

class Graphic(_message.Message):
    __slots__ = ("img_path", "bottom_left")
    IMG_PATH_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_LEFT_FIELD_NUMBER: _ClassVar[int]
    img_path: str
    bottom_left: _geom_pb2.GridCoord
    def __init__(self, img_path: _Optional[str] = ..., bottom_left: _Optional[_Union[_geom_pb2.GridCoord, _Mapping]] = ...) -> None: ...

class ParInfo(_message.Message):
    __slots__ = ("shortest_path_length", "longest_path_length", "shortest_path", "longest_path")
    SHORTEST_PATH_LENGTH_FIELD_NUMBER: _ClassVar[int]
    LONGEST_PATH_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SHORTEST_PATH_FIELD_NUMBER: _ClassVar[int]
    LONGEST_PATH_FIELD_NUMBER: _ClassVar[int]
    shortest_path_length: int
    longest_path_length: int
    shortest_path: _containers.RepeatedCompositeFieldContainer[_geom_pb2.Gridtangle]
    longest_path: _containers.RepeatedCompositeFieldContainer[_geom_pb2.Gridtangle]
    def __init__(self, shortest_path_length: _Optional[int] = ..., longest_path_length: _Optional[int] = ..., shortest_path: _Optional[_Iterable[_Union[_geom_pb2.Gridtangle, _Mapping]]] = ..., longest_path: _Optional[_Iterable[_Union[_geom_pb2.Gridtangle, _Mapping]]] = ...) -> None: ...

class MazeGenConfig(_message.Message):
    __slots__ = ("scene", "dynamic_colors", "difficulty")
    SCENE_FIELD_NUMBER: _ClassVar[int]
    DYNAMIC_COLORS_FIELD_NUMBER: _ClassVar[int]
    DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    scene: _mondrian_pb2.SceneSpec
    dynamic_colors: ColorInfo
    difficulty: str
    def __init__(self, scene: _Optional[_Union[_mondrian_pb2.SceneSpec, _Mapping]] = ..., dynamic_colors: _Optional[_Union[ColorInfo, _Mapping]] = ..., difficulty: _Optional[str] = ...) -> None: ...

class ColorInfo(_message.Message):
    __slots__ = ("current_node_color", "path_color", "tile_colors", "border_color", "invalid_move_base_color", "invalid_move_highlight_color", "goal_color_cycle", "splash_text_color", "splash_box_color")
    CURRENT_NODE_COLOR_FIELD_NUMBER: _ClassVar[int]
    PATH_COLOR_FIELD_NUMBER: _ClassVar[int]
    TILE_COLORS_FIELD_NUMBER: _ClassVar[int]
    BORDER_COLOR_FIELD_NUMBER: _ClassVar[int]
    INVALID_MOVE_BASE_COLOR_FIELD_NUMBER: _ClassVar[int]
    INVALID_MOVE_HIGHLIGHT_COLOR_FIELD_NUMBER: _ClassVar[int]
    GOAL_COLOR_CYCLE_FIELD_NUMBER: _ClassVar[int]
    SPLASH_TEXT_COLOR_FIELD_NUMBER: _ClassVar[int]
    SPLASH_BOX_COLOR_FIELD_NUMBER: _ClassVar[int]
    current_node_color: str
    path_color: str
    tile_colors: _containers.RepeatedScalarFieldContainer[str]
    border_color: str
    invalid_move_base_color: str
    invalid_move_highlight_color: str
    goal_color_cycle: _containers.RepeatedScalarFieldContainer[str]
    splash_text_color: str
    splash_box_color: str
    def __init__(self, current_node_color: _Optional[str] = ..., path_color: _Optional[str] = ..., tile_colors: _Optional[_Iterable[str]] = ..., border_color: _Optional[str] = ..., invalid_move_base_color: _Optional[str] = ..., invalid_move_highlight_color: _Optional[str] = ..., goal_color_cycle: _Optional[_Iterable[str]] = ..., splash_text_color: _Optional[str] = ..., splash_box_color: _Optional[str] = ...) -> None: ...

class ColorPool(_message.Message):
    __slots__ = ("name", "palettes", "defaults")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PALETTES_FIELD_NUMBER: _ClassVar[int]
    DEFAULTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    palettes: _containers.RepeatedCompositeFieldContainer[ColorInfo]
    defaults: ColorInfo
    def __init__(self, name: _Optional[str] = ..., palettes: _Optional[_Iterable[_Union[ColorInfo, _Mapping]]] = ..., defaults: _Optional[_Union[ColorInfo, _Mapping]] = ...) -> None: ...

class StandardBoxLevelGen(_message.Message):
    __slots__ = ("width", "height", "edge_sizes", "edge_size_combinations", "scale_by", "thin_rect_strategy")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    EDGE_SIZES_FIELD_NUMBER: _ClassVar[int]
    EDGE_SIZE_COMBINATIONS_FIELD_NUMBER: _ClassVar[int]
    SCALE_BY_FIELD_NUMBER: _ClassVar[int]
    THIN_RECT_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    edge_sizes: _containers.RepeatedScalarFieldContainer[int]
    edge_size_combinations: _containers.RepeatedCompositeFieldContainer[_mondrian_pb2.RectTargetSize]
    scale_by: int
    thin_rect_strategy: _mondrian_pb2.ThinRectStrategy
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ..., edge_sizes: _Optional[_Iterable[int]] = ..., edge_size_combinations: _Optional[_Iterable[_Union[_mondrian_pb2.RectTargetSize, _Mapping]]] = ..., scale_by: _Optional[int] = ..., thin_rect_strategy: _Optional[_Union[_mondrian_pb2.ThinRectStrategy, str]] = ...) -> None: ...

class MazeGeometryConfig(_message.Message):
    __slots__ = ("name", "color_pool", "colorblind_color_pool", "standard_box_level", "filters")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COLOR_POOL_FIELD_NUMBER: _ClassVar[int]
    COLORBLIND_COLOR_POOL_FIELD_NUMBER: _ClassVar[int]
    STANDARD_BOX_LEVEL_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    name: str
    color_pool: str
    colorblind_color_pool: str
    standard_box_level: StandardBoxLevelGen
    filters: _containers.RepeatedCompositeFieldContainer[MazeFilter]
    def __init__(self, name: _Optional[str] = ..., color_pool: _Optional[str] = ..., colorblind_color_pool: _Optional[str] = ..., standard_box_level: _Optional[_Union[StandardBoxLevelGen, _Mapping]] = ..., filters: _Optional[_Iterable[_Union[MazeFilter, _Mapping]]] = ...) -> None: ...

class MazeFilter(_message.Message):
    __slots__ = ("quantity", "relation", "value", "action", "priority")
    class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACTION_UNKNOWN: _ClassVar[MazeFilter.Action]
        INCLUDE: _ClassVar[MazeFilter.Action]
        EXCLUDE: _ClassVar[MazeFilter.Action]
    ACTION_UNKNOWN: MazeFilter.Action
    INCLUDE: MazeFilter.Action
    EXCLUDE: MazeFilter.Action
    class Quantity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        QUANTITY_UNKNOWN: _ClassVar[MazeFilter.Quantity]
        SHORTEST_PATH_STEPS: _ClassVar[MazeFilter.Quantity]
        COMPRESSED_SHORTEST_PATH_STEPS: _ClassVar[MazeFilter.Quantity]
        LONGEST_PATH_STEPS: _ClassVar[MazeFilter.Quantity]
        COMPRESSED_LONGEST_PATH_STEPS: _ClassVar[MazeFilter.Quantity]
        SHORTEST_LONGEST_EDIT_DISTANCE: _ClassVar[MazeFilter.Quantity]
        LONGEST_PATH_TIMED_OUT: _ClassVar[MazeFilter.Quantity]
        REACHABLE_BOUNDING_BOX_MINOR_AXIS_LENGTH: _ClassVar[MazeFilter.Quantity]
        UNREACHABLE_TILE_COUNT: _ClassVar[MazeFilter.Quantity]
        SOLUTION_BOUNDING_BOX_MINOR_AXIS_LENGTH: _ClassVar[MazeFilter.Quantity]
        TILE_COUNT: _ClassVar[MazeFilter.Quantity]
        MAX_TILE_AREA: _ClassVar[MazeFilter.Quantity]
        TILES_NOT_IN_LONGEST_PATH: _ClassVar[MazeFilter.Quantity]
        TILES_IN_LONGEST_PATH_PERCENT: _ClassVar[MazeFilter.Quantity]
    QUANTITY_UNKNOWN: MazeFilter.Quantity
    SHORTEST_PATH_STEPS: MazeFilter.Quantity
    COMPRESSED_SHORTEST_PATH_STEPS: MazeFilter.Quantity
    LONGEST_PATH_STEPS: MazeFilter.Quantity
    COMPRESSED_LONGEST_PATH_STEPS: MazeFilter.Quantity
    SHORTEST_LONGEST_EDIT_DISTANCE: MazeFilter.Quantity
    LONGEST_PATH_TIMED_OUT: MazeFilter.Quantity
    REACHABLE_BOUNDING_BOX_MINOR_AXIS_LENGTH: MazeFilter.Quantity
    UNREACHABLE_TILE_COUNT: MazeFilter.Quantity
    SOLUTION_BOUNDING_BOX_MINOR_AXIS_LENGTH: MazeFilter.Quantity
    TILE_COUNT: MazeFilter.Quantity
    MAX_TILE_AREA: MazeFilter.Quantity
    TILES_NOT_IN_LONGEST_PATH: MazeFilter.Quantity
    TILES_IN_LONGEST_PATH_PERCENT: MazeFilter.Quantity
    class Relation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RELATION_UNKNOWN: _ClassVar[MazeFilter.Relation]
        GREATER_THAN: _ClassVar[MazeFilter.Relation]
        LESS_THAN: _ClassVar[MazeFilter.Relation]
    RELATION_UNKNOWN: MazeFilter.Relation
    GREATER_THAN: MazeFilter.Relation
    LESS_THAN: MazeFilter.Relation
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    quantity: MazeFilter.Quantity
    relation: MazeFilter.Relation
    value: int
    action: MazeFilter.Action
    priority: int
    def __init__(self, quantity: _Optional[_Union[MazeFilter.Quantity, str]] = ..., relation: _Optional[_Union[MazeFilter.Relation, str]] = ..., value: _Optional[int] = ..., action: _Optional[_Union[MazeFilter.Action, str]] = ..., priority: _Optional[int] = ...) -> None: ...

class MazeQuality(_message.Message):
    __slots__ = ("shortest_path_steps", "compressed_shortest_path_steps", "longest_path_steps", "compressed_longest_path_steps", "shortest_longest_edit_distance", "longest_path_timed_out", "reachable_bounding_box_minor_axis_length", "unreachable_tile_count", "solution_bounding_box_minor_axis_length", "tile_count", "max_tile_area", "tiles_not_in_longest_path", "tiles_in_longest_path_percent")
    SHORTEST_PATH_STEPS_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_SHORTEST_PATH_STEPS_FIELD_NUMBER: _ClassVar[int]
    LONGEST_PATH_STEPS_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_LONGEST_PATH_STEPS_FIELD_NUMBER: _ClassVar[int]
    SHORTEST_LONGEST_EDIT_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    LONGEST_PATH_TIMED_OUT_FIELD_NUMBER: _ClassVar[int]
    REACHABLE_BOUNDING_BOX_MINOR_AXIS_LENGTH_FIELD_NUMBER: _ClassVar[int]
    UNREACHABLE_TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_BOUNDING_BOX_MINOR_AXIS_LENGTH_FIELD_NUMBER: _ClassVar[int]
    TILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_TILE_AREA_FIELD_NUMBER: _ClassVar[int]
    TILES_NOT_IN_LONGEST_PATH_FIELD_NUMBER: _ClassVar[int]
    TILES_IN_LONGEST_PATH_PERCENT_FIELD_NUMBER: _ClassVar[int]
    shortest_path_steps: int
    compressed_shortest_path_steps: int
    longest_path_steps: int
    compressed_longest_path_steps: int
    shortest_longest_edit_distance: int
    longest_path_timed_out: int
    reachable_bounding_box_minor_axis_length: int
    unreachable_tile_count: int
    solution_bounding_box_minor_axis_length: int
    tile_count: int
    max_tile_area: int
    tiles_not_in_longest_path: int
    tiles_in_longest_path_percent: int
    def __init__(self, shortest_path_steps: _Optional[int] = ..., compressed_shortest_path_steps: _Optional[int] = ..., longest_path_steps: _Optional[int] = ..., compressed_longest_path_steps: _Optional[int] = ..., shortest_longest_edit_distance: _Optional[int] = ..., longest_path_timed_out: _Optional[int] = ..., reachable_bounding_box_minor_axis_length: _Optional[int] = ..., unreachable_tile_count: _Optional[int] = ..., solution_bounding_box_minor_axis_length: _Optional[int] = ..., tile_count: _Optional[int] = ..., max_tile_area: _Optional[int] = ..., tiles_not_in_longest_path: _Optional[int] = ..., tiles_in_longest_path_percent: _Optional[int] = ...) -> None: ...

class MazeVariantSpec(_message.Message):
    __slots__ = ("name", "level_groups", "metadata")
    NAME_FIELD_NUMBER: _ClassVar[int]
    LEVEL_GROUPS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    level_groups: _containers.RepeatedCompositeFieldContainer[SubVariantSpec]
    metadata: VariantMetadata
    def __init__(self, name: _Optional[str] = ..., level_groups: _Optional[_Iterable[_Union[SubVariantSpec, _Mapping]]] = ..., metadata: _Optional[_Union[VariantMetadata, _Mapping]] = ...) -> None: ...

class SubVariantSpec(_message.Message):
    __slots__ = ("geometry_names", "level_count", "difficulty")
    GEOMETRY_NAMES_FIELD_NUMBER: _ClassVar[int]
    LEVEL_COUNT_FIELD_NUMBER: _ClassVar[int]
    DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    geometry_names: _containers.RepeatedScalarFieldContainer[str]
    level_count: int
    difficulty: str
    def __init__(self, geometry_names: _Optional[_Iterable[str]] = ..., level_count: _Optional[int] = ..., difficulty: _Optional[str] = ...) -> None: ...

class VariantMetadata(_message.Message):
    __slots__ = ("url_tag", "title_phrase", "you_have_completed_phrase")
    URL_TAG_FIELD_NUMBER: _ClassVar[int]
    TITLE_PHRASE_FIELD_NUMBER: _ClassVar[int]
    YOU_HAVE_COMPLETED_PHRASE_FIELD_NUMBER: _ClassVar[int]
    url_tag: str
    title_phrase: str
    you_have_completed_phrase: str
    def __init__(self, url_tag: _Optional[str] = ..., title_phrase: _Optional[str] = ..., you_have_completed_phrase: _Optional[str] = ...) -> None: ...

class LevelBatchConfig(_message.Message):
    __slots__ = ("variants", "geometries", "color_pools")
    VARIANTS_FIELD_NUMBER: _ClassVar[int]
    GEOMETRIES_FIELD_NUMBER: _ClassVar[int]
    COLOR_POOLS_FIELD_NUMBER: _ClassVar[int]
    variants: _containers.RepeatedCompositeFieldContainer[MazeVariantSpec]
    geometries: _containers.RepeatedCompositeFieldContainer[MazeGeometryConfig]
    color_pools: _containers.RepeatedCompositeFieldContainer[ColorPool]
    def __init__(self, variants: _Optional[_Iterable[_Union[MazeVariantSpec, _Mapping]]] = ..., geometries: _Optional[_Iterable[_Union[MazeGeometryConfig, _Mapping]]] = ..., color_pools: _Optional[_Iterable[_Union[ColorPool, _Mapping]]] = ...) -> None: ...
