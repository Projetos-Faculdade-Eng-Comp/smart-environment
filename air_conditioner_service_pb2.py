# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: air_conditioner_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1d\x61ir_conditioner_service.proto\x12\x17\x61ir_conditioner_service\"\x17\n\x15\x41irConditionerRequest\"\x19\n\x06Status\x12\x0f\n\x07message\x18\x01 \x01(\t2\xac\x03\n\x15\x41irConditionerService\x12g\n\x14turnOnAirConditioner\x12..air_conditioner_service.AirConditionerRequest\x1a\x1f.air_conditioner_service.Status\x12h\n\x15turnOffAirConditioner\x12..air_conditioner_service.AirConditionerRequest\x1a\x1f.air_conditioner_service.Status\x12_\n\x0c\x61umentarTemp\x12..air_conditioner_service.AirConditionerRequest\x1a\x1f.air_conditioner_service.Status\x12_\n\x0c\x64iminuirTemp\x12..air_conditioner_service.AirConditionerRequest\x1a\x1f.air_conditioner_service.Statusb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, 'air_conditioner_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_AIRCONDITIONERREQUEST']._serialized_start = 58
    _globals['_AIRCONDITIONERREQUEST']._serialized_end = 81
    _globals['_STATUS']._serialized_start = 83
    _globals['_STATUS']._serialized_end = 108
    _globals['_AIRCONDITIONERSERVICE']._serialized_start = 111
    _globals['_AIRCONDITIONERSERVICE']._serialized_end = 539
# @@protoc_insertion_point(module_scope)
