# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: actuators_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17\x61\x63tuators_service.proto\x12\x11\x61\x63tuators_service\"\x0f\n\rTurnOnRequest\"\x10\n\x0eTurnOffRequest\"\x19\n\x06Status\x12\x0f\n\x07message\x18\x01 \x01(\t2\xa6\x01\n\x10\x41\x63tuatorsService\x12G\n\x06turnOn\x12 .actuators_service.TurnOnRequest\x1a\x19.actuators_service.Status\"\x00\x12I\n\x07turnOff\x12!.actuators_service.TurnOffRequest\x1a\x19.actuators_service.Status\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'actuators_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_TURNONREQUEST']._serialized_start=46
  _globals['_TURNONREQUEST']._serialized_end=61
  _globals['_TURNOFFREQUEST']._serialized_start=63
  _globals['_TURNOFFREQUEST']._serialized_end=79
  _globals['_STATUS']._serialized_start=81
  _globals['_STATUS']._serialized_end=106
  _globals['_ACTUATORSSERVICE']._serialized_start=109
  _globals['_ACTUATORSSERVICE']._serialized_end=275
# @@protoc_insertion_point(module_scope)
