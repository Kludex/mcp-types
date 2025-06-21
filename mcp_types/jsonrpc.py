"""This module contains the JSON RPC types for the MCP.

The request types are `TypedDict`s, while the response types are `BaseModel`s.

This not only provides the best developer experience, but also conceptually, there's no
need to validate the request types using a type checker. On the other hand, you need to
make sure the data that you receive in the response is valid.
"""

from __future__ import annotations as _annotations

from typing import Annotated, Any, Generic, Literal, TypeVar
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, NotRequired

RequestId = Annotated[int | str, Field(union_mode="left_to_right")]


MethodT = TypeVar("MethodT", bound=str)
ParamsT = TypeVar("ParamsT", default=None)


class JSONRPCRequest(TypedDict, Generic[MethodT, ParamsT]):
    """A JSON RPC request."""

    jsonrpc: Literal["2.0"]
    """The JSON RPC version."""

    id: RequestId

    method: MethodT
    """The method to call."""

    params: NotRequired[ParamsT]
    """The parameters to pass to the method."""


CodeT = TypeVar("CodeT", bound=int)
MessageT = TypeVar("MessageT", bound=str, default=str)


class ErrorData(BaseModel, Generic[CodeT, MessageT]):
    """A JSON RPC error."""

    code: CodeT
    message: MessageT
    data: Any = None


ResultT = TypeVar("ResultT", bound=BaseModel)


class _BaseJSONRPCResponse(BaseModel):
    """A base class for JSON RPC responses."""

    jsonrpc: Literal["2.0"]
    """The JSON RPC version."""

    id: RequestId


class JSONRPCResponse(_BaseJSONRPCResponse, Generic[ResultT]):
    """A JSON RPC response."""

    result: ResultT


ErrorT = TypeVar("ErrorT")


class JSONRPCError(_BaseJSONRPCResponse, Generic[CodeT, MessageT]):
    """A JSON RPC response that indicates an error occurred."""

    error: ErrorData[CodeT, MessageT]
