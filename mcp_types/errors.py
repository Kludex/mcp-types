from __future__ import annotations as _annotations

from typing import Literal
from mcp_types.jsonrpc import JSONRPCError

MethodNotFoundCode = Literal[-32601]
InternalErrorCode = Literal[-32603]

ListRootNotFound = JSONRPCError[MethodNotFoundCode]
ListRootInternalError = JSONRPCError[InternalErrorCode]
