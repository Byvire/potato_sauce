# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: potato_sauce/proto/mazetangle.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from potato_sauce.proto import geom_pb2 as potato__sauce_dot_proto_dot_geom__pb2
from potato_sauce.proto import mondrian_pb2 as potato__sauce_dot_proto_dot_mondrian__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#potato_sauce/proto/mazetangle.proto\x12\x17potato_sauce.mazetangle\x1a\x1dpotato_sauce/proto/geom.proto\x1a!potato_sauce/proto/mondrian.proto\"\x97\x04\n\x04Maze\x12,\n\x05rects\x18\x01 \x03(\x0b\x32\x1d.potato_sauce.geom.Gridtangle\x12\x34\n\nbackground\x18\x02 \x01(\x0b\x32 .potato_sauce.mazetangle.Graphic\x12,\n\x05start\x18\x03 \x01(\x0b\x32\x1d.potato_sauce.geom.Gridtangle\x12+\n\x04goal\x18\x04 \x01(\x0b\x32\x1d.potato_sauce.geom.Gridtangle\x12\x33\n\x0c\x62ounding_box\x18\x05 \x01(\x0b\x32\x1d.potato_sauce.geom.Gridtangle\x12\x32\n\x08par_info\x18\x06 \x01(\x0b\x32 .potato_sauce.mazetangle.ParInfo\x12\x31\n\x05\x63olor\x18\x07 \x01(\x0b\x32\".potato_sauce.mazetangle.ColorInfo\x12?\n\x15\x63olorblind_background\x18\x08 \x01(\x0b\x32 .potato_sauce.mazetangle.Graphic\x12<\n\x10\x63olorblind_color\x18\t \x01(\x0b\x32\".potato_sauce.mazetangle.ColorInfo\x12\x35\n\x07quality\x18\n \x01(\x0b\x32$.potato_sauce.mazetangle.MazeQuality\"N\n\x07Graphic\x12\x10\n\x08img_path\x18\x01 \x01(\t\x12\x31\n\x0b\x62ottom_left\x18\x02 \x01(\x0b\x32\x1c.potato_sauce.geom.GridCoord\"\xaf\x01\n\x07ParInfo\x12\x1c\n\x14shortest_path_length\x18\x01 \x01(\x05\x12\x1b\n\x13longest_path_length\x18\x02 \x01(\x05\x12\x34\n\rshortest_path\x18\x03 \x03(\x0b\x32\x1d.potato_sauce.geom.Gridtangle\x12\x33\n\x0clongest_path\x18\x04 \x03(\x0b\x32\x1d.potato_sauce.geom.Gridtangle\"|\n\rMazeGenConfig\x12/\n\x05scene\x18\x01 \x01(\x0b\x32 .potato_sauce.mondrian.SceneSpec\x12:\n\x0e\x64ynamic_colors\x18\x02 \x01(\x0b\x32\".potato_sauce.mazetangle.ColorInfo\"\xc7\x01\n\tColorInfo\x12\x1a\n\x12\x63urrent_node_color\x18\x01 \x01(\t\x12\x12\n\npath_color\x18\x02 \x01(\t\x12\x13\n\x0btile_colors\x18\x03 \x03(\t\x12\x14\n\x0c\x62order_color\x18\x04 \x01(\t\x12\x1f\n\x17invalid_move_base_color\x18\x05 \x01(\t\x12$\n\x1cinvalid_move_highlight_color\x18\x06 \x01(\t\x12\x18\n\x10goal_color_cycle\x18\x07 \x03(\t\"\x85\x01\n\tColorPool\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x34\n\x08palettes\x18\x02 \x03(\x0b\x32\".potato_sauce.mazetangle.ColorInfo\x12\x34\n\x08\x64\x65\x66\x61ults\x18\x03 \x01(\x0b\x32\".potato_sauce.mazetangle.ColorInfo\"\xe6\x01\n\x13StandardBoxLevelGen\x12\r\n\x05width\x18\x03 \x01(\x05\x12\x0e\n\x06height\x18\x04 \x01(\x05\x12\x12\n\nedge_sizes\x18\x05 \x03(\x05\x12\x45\n\x16\x65\x64ge_size_combinations\x18\x08 \x03(\x0b\x32%.potato_sauce.mondrian.RectTargetSize\x12\x10\n\x08scale_by\x18\x06 \x01(\x05\x12\x43\n\x12thin_rect_strategy\x18\x07 \x01(\x0e\x32\'.potato_sauce.mondrian.ThinRectStrategy\"\xe1\x01\n\x12MazeGeometryConfig\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\ncolor_pool\x18\x02 \x01(\t\x12\x1d\n\x15\x63olorblind_color_pool\x18\x03 \x01(\t\x12J\n\x12standard_box_level\x18\x04 \x01(\x0b\x32,.potato_sauce.mazetangle.StandardBoxLevelGenH\x00\x12\x34\n\x07\x66ilters\x18\n \x03(\x0b\x32#.potato_sauce.mazetangle.MazeFilterB\x08\n\x06\x63onfig\"\x9b\x06\n\nMazeFilter\x12>\n\x08quantity\x18\x03 \x01(\x0e\x32,.potato_sauce.mazetangle.MazeFilter.Quantity\x12>\n\x08relation\x18\x04 \x01(\x0e\x32,.potato_sauce.mazetangle.MazeFilter.Relation\x12\r\n\x05value\x18\x05 \x01(\x05\x12:\n\x06\x61\x63tion\x18\x01 \x01(\x0e\x32*.potato_sauce.mazetangle.MazeFilter.Action\x12\x10\n\x08priority\x18\x02 \x01(\x05\"6\n\x06\x41\x63tion\x12\x12\n\x0e\x41\x43TION_UNKNOWN\x10\x00\x12\x0b\n\x07INCLUDE\x10\x01\x12\x0b\n\x07\x45XCLUDE\x10\x02\"\xb4\x03\n\x08Quantity\x12\x14\n\x10QUANTITY_UNKNOWN\x10\x00\x12\x17\n\x13SHORTEST_PATH_STEPS\x10\x01\x12\"\n\x1e\x43OMPRESSED_SHORTEST_PATH_STEPS\x10\x02\x12\x16\n\x12LONGEST_PATH_STEPS\x10\x03\x12!\n\x1d\x43OMPRESSED_LONGEST_PATH_STEPS\x10\x04\x12\"\n\x1eSHORTEST_LONGEST_EDIT_DISTANCE\x10\x05\x12\x1a\n\x16LONGEST_PATH_TIMED_OUT\x10\x06\x12,\n(REACHABLE_BOUNDING_BOX_MINOR_AXIS_LENGTH\x10\x07\x12\x1a\n\x16UNREACHABLE_TILE_COUNT\x10\x08\x12+\n\'SOLUTION_BOUNDING_BOX_MINOR_AXIS_LENGTH\x10\t\x12\x0e\n\nTILE_COUNT\x10\n\x12\x11\n\rMAX_TILE_AREA\x10\x0b\x12\x1d\n\x19TILES_NOT_IN_LONGEST_PATH\x10\x0c\x12!\n\x1dTILES_IN_LONGEST_PATH_PERCENT\x10\r\"A\n\x08Relation\x12\x14\n\x10RELATION_UNKNOWN\x10\x00\x12\x10\n\x0cGREATER_THAN\x10\x01\x12\r\n\tLESS_THAN\x10\x02\"\xd5\x03\n\x0bMazeQuality\x12\x1b\n\x13shortest_path_steps\x18\x01 \x01(\x05\x12&\n\x1e\x63ompressed_shortest_path_steps\x18\x02 \x01(\x05\x12\x1a\n\x12longest_path_steps\x18\x03 \x01(\x05\x12%\n\x1d\x63ompressed_longest_path_steps\x18\x04 \x01(\x05\x12&\n\x1eshortest_longest_edit_distance\x18\x05 \x01(\x05\x12\x1e\n\x16longest_path_timed_out\x18\x06 \x01(\x05\x12\x30\n(reachable_bounding_box_minor_axis_length\x18\x07 \x01(\x05\x12\x1e\n\x16unreachable_tile_count\x18\x08 \x01(\x05\x12/\n\'solution_bounding_box_minor_axis_length\x18\t \x01(\x05\x12\x12\n\ntile_count\x18\n \x01(\x05\x12\x15\n\rmax_tile_area\x18\x0b \x01(\x05\x12!\n\x19tiles_not_in_longest_path\x18\x0c \x01(\x05\x12%\n\x1dtiles_in_longest_path_percent\x18\r \x01(\x05\"j\n\x0fMazeVariantSpec\x12\x0c\n\x04name\x18\x01 \x01(\t\x12=\n\x0clevel_groups\x18\x04 \x03(\x0b\x32\'.potato_sauce.mazetangle.SubVariantSpecJ\x04\x08\x02\x10\x03J\x04\x08\x03\x10\x04\"<\n\x0eSubVariantSpec\x12\x15\n\rgeometry_name\x18\x01 \x01(\t\x12\x13\n\x0blevel_count\x18\x02 \x01(\x05\"\xc8\x01\n\x10LevelBatchConfig\x12:\n\x08variants\x18\x01 \x03(\x0b\x32(.potato_sauce.mazetangle.MazeVariantSpec\x12?\n\ngeometries\x18\x02 \x03(\x0b\x32+.potato_sauce.mazetangle.MazeGeometryConfig\x12\x37\n\x0b\x63olor_pools\x18\x03 \x03(\x0b\x32\".potato_sauce.mazetangle.ColorPoolb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'potato_sauce.proto.mazetangle_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_MAZE']._serialized_start=131
  _globals['_MAZE']._serialized_end=666
  _globals['_GRAPHIC']._serialized_start=668
  _globals['_GRAPHIC']._serialized_end=746
  _globals['_PARINFO']._serialized_start=749
  _globals['_PARINFO']._serialized_end=924
  _globals['_MAZEGENCONFIG']._serialized_start=926
  _globals['_MAZEGENCONFIG']._serialized_end=1050
  _globals['_COLORINFO']._serialized_start=1053
  _globals['_COLORINFO']._serialized_end=1252
  _globals['_COLORPOOL']._serialized_start=1255
  _globals['_COLORPOOL']._serialized_end=1388
  _globals['_STANDARDBOXLEVELGEN']._serialized_start=1391
  _globals['_STANDARDBOXLEVELGEN']._serialized_end=1621
  _globals['_MAZEGEOMETRYCONFIG']._serialized_start=1624
  _globals['_MAZEGEOMETRYCONFIG']._serialized_end=1849
  _globals['_MAZEFILTER']._serialized_start=1852
  _globals['_MAZEFILTER']._serialized_end=2647
  _globals['_MAZEFILTER_ACTION']._serialized_start=2087
  _globals['_MAZEFILTER_ACTION']._serialized_end=2141
  _globals['_MAZEFILTER_QUANTITY']._serialized_start=2144
  _globals['_MAZEFILTER_QUANTITY']._serialized_end=2580
  _globals['_MAZEFILTER_RELATION']._serialized_start=2582
  _globals['_MAZEFILTER_RELATION']._serialized_end=2647
  _globals['_MAZEQUALITY']._serialized_start=2650
  _globals['_MAZEQUALITY']._serialized_end=3119
  _globals['_MAZEVARIANTSPEC']._serialized_start=3121
  _globals['_MAZEVARIANTSPEC']._serialized_end=3227
  _globals['_SUBVARIANTSPEC']._serialized_start=3229
  _globals['_SUBVARIANTSPEC']._serialized_end=3289
  _globals['_LEVELBATCHCONFIG']._serialized_start=3292
  _globals['_LEVELBATCHCONFIG']._serialized_end=3492
# @@protoc_insertion_point(module_scope)
