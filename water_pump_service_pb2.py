# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: water_pump_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18water_pump_service.proto\x12\x12water_pump_service\"\x18\n\x16TurnOnWaterPumpRequest\"\x19\n\x17TurnOffWaterPumpRequest\"\x19\n\x06Status\x12\x0f\n\x07message\x18\x01 \x01(\t2\xca\x01\n\x10WaterPumpService\x12Y\n\x0fTurnOnWaterPump\x12*.water_pump_service.TurnOnWaterPumpRequest\x1a\x1a.water_pump_service.Status\x12[\n\x10TurnOffWaterPump\x12+.water_pump_service.TurnOffWaterPumpRequest\x1a\x1a.water_pump_service.Statusb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'water_pump_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_TURNONWATERPUMPREQUEST']._serialized_start=48
  _globals['_TURNONWATERPUMPREQUEST']._serialized_end=72
  _globals['_TURNOFFWATERPUMPREQUEST']._serialized_start=74
  _globals['_TURNOFFWATERPUMPREQUEST']._serialized_end=99
  _globals['_STATUS']._serialized_start=101
  _globals['_STATUS']._serialized_end=126
  _globals['_WATERPUMPSERVICE']._serialized_start=129
  _globals['_WATERPUMPSERVICE']._serialized_end=331
# @@protoc_insertion_point(module_scope)
