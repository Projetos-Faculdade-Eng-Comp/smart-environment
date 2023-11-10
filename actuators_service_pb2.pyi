from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LigarLampadaRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DesligarLampadaRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class AirConditionerRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TurnOnWaterPumpRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TurnOffWaterPumpRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Status(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
