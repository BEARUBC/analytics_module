# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: sgcp.proto
# Protobuf Python Version: 5.27.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 27, 0, "", "sgcp.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import analytics.protobuf.bms_pb2 as bms__pb2
import analytics.protobuf.emg_pb2 as emg__pb2
import analytics.protobuf.maestro_pb2 as maestro__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\nsgcp.proto\x12\x04sgcp\x1a\tbms.proto\x1a\temg.proto\x1a\rmaestro.proto"\xc6\x01\n\x07Request\x12 \n\x08resource\x18\x01 \x01(\x0e\x32\x0e.sgcp.Resource\x12\x10\n\x08taskCode\x18\x02 \x01(\t\x12%\n\x07\x62msData\x18\x03 \x01(\x0b\x32\x12.sgcp.bms.TaskDataH\x00\x12%\n\x07\x65mgData\x18\x04 \x01(\x0b\x32\x12.sgcp.emg.TaskDataH\x00\x12-\n\x0bmaestroData\x18\x05 \x01(\x0b\x32\x16.sgcp.maestro.TaskDataH\x00\x42\n\n\x08taskData"/\n\x08Response\x12\x12\n\nstatusCode\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t*B\n\x08Resource\x12\x17\n\x13UNDEFINED_COMPONENT\x10\x00\x12\x07\n\x03\x42MS\x10\x01\x12\x07\n\x03\x45MG\x10\x02\x12\x0b\n\x07MAESTRO\x10\x03\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "sgcp_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_RESOURCE"]._serialized_start = 307
    _globals["_RESOURCE"]._serialized_end = 373
    _globals["_REQUEST"]._serialized_start = 58
    _globals["_REQUEST"]._serialized_end = 256
    _globals["_RESPONSE"]._serialized_start = 258
    _globals["_RESPONSE"]._serialized_end = 305
# @@protoc_insertion_point(module_scope)
