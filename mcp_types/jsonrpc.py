from __future__ import annotations as _annotations

from typing import Any, Generic, Literal, TypeVar
from typing_extensions import TypedDict, NotRequired


class JSONRPCMessage(TypedDict):
    """A JSON RPC message."""

    jsonrpc: Literal["2.0"]
    """The JSON RPC version."""

    id: int | str | None
    """The request id."""


MethodT = TypeVar("MethodT", bound=str)
ParamsT = TypeVar("ParamsT", default=None)


class JSONRPCRequest(JSONRPCMessage, Generic[MethodT, ParamsT]):
    """A JSON RPC request."""

    method: MethodT
    """The method to call."""

    params: NotRequired[ParamsT]
    """The parameters to pass to the method."""


CodeT = TypeVar("CodeT", bound=int)
MessageT = TypeVar("MessageT", bound=str)


class JSONRPCError(TypedDict, Generic[CodeT, MessageT]):
    """A JSON RPC error."""

    code: CodeT
    message: MessageT
    # TODO(Marcelo): Should it be really Any?
    data: NotRequired[Any]


ResultT = TypeVar("ResultT")
ErrorT = TypeVar("ErrorT", bound=JSONRPCError[Any, Any])


class JSONRPCResponse(JSONRPCMessage, Generic[ResultT, ErrorT]):
    """A JSON RPC response."""

    result: NotRequired[ResultT]
    error: NotRequired[ErrorT]
