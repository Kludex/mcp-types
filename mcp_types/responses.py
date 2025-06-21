from __future__ import annotations as _annotations
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field

from mcp_types.jsonrpc import JSONRPCResponse
from mcp_types.requests import Role

PROTOCOL_VERSION = "2025-06-18"


class BaseResult(BaseModel):
    """Base result for all responses."""

    _meta: dict[str, Any] | None = None
    """See [specification/2025-06-18/basic/index#general-fields] for notes on _meta usage."""


class CompletionsCapability(BaseModel, extra="allow"): ...


class LoggingCapability(BaseModel, extra="allow"): ...


class PromptsCapability(BaseModel):
    """Present if the server offers any prompt templates."""

    list_changed: Annotated[bool | None, Field(alias="listChanged")] = None
    """Whether this server supports notifications for changes to the prompt list."""


class ResourcesCapability(BaseModel):
    """Present if the server offers any resources to read."""

    list_changed: Annotated[bool | None, Field(alias="listChanged")] = None
    """Whether this server supports notifications for changes to the resource list."""

    subscribe: bool | None = None
    """Whether this server supports subscribing to resource updates."""


class ToolsCapability(BaseModel):
    """Present if the server offers any tools to call."""

    list_changed: Annotated[bool | None, Field(alias="listChanged")] = None
    """Whether this server supports notifications for changes to the tool list."""


class ServerCapabilities(BaseModel):
    """Capabilities that a server may support.

    Known capabilities are defined here, in this schema, but this is not a closed set:
    any server can define its own, additional capabilities.
    """

    completions: CompletionsCapability | None = None
    """Present if the server supports argument autocompletion suggestions."""

    logging: LoggingCapability | None = None
    """Present if the server supports sending log messages to the client."""

    prompts: PromptsCapability | None = None
    """Present if the server offers any prompt templates."""

    resources: ResourcesCapability | None = None
    """Present if the server offers any resources to read."""

    tools: ToolsCapability | None = None
    """Present if the server offers any tools to call."""

    experimental: dict[str, dict[str, Any]] | None = None
    """Experimental, non-standard capabilities that the server supports."""


class Implementation(BaseModel):
    name: str
    title: str | None = None
    version: str


class InitializeResult(BaseResult):
    """After receiving an initialize request from the client, the server sends this response."""

    capabilities: ServerCapabilities
    """Capabilities that a server may support.

    Known capabilities are defined here, in this schema, but this is not a closed set:
    any server can define its own, additional capabilities.
    """

    instructions: str | None = None
    """Instructions describing how to use the server and its features.

    This can be used by clients to improve the LLM's understanding of available tools,
    resources, etc. It can be thought of like a "hint" to the model. For example, this
    information MAY be added to the system prompt.
    """

    protocol_version: Annotated[str, Field(alias="protocolVersion")] = PROTOCOL_VERSION
    """The version of the Model Context Protocol that the server wants to use.

    This may not match the version that the client requested. If the client cannot support
    this version, it MUST disconnect.
    """

    server_info: Annotated[Implementation, Field(alias="serverInfo")]
    """Describes the name and version of an MCP implementation, with an optional title for UI representation."""


class TextContent(BaseModel):
    """A text content."""

    type: Literal["text"] = "text"
    """The type of content."""
    text: str


class ImageContent(BaseModel):
    """An image content."""

    type: Literal["image"] = "image"
    """The type of content."""
    data: str
    """Base64 encoded image data."""
    mime_type: Annotated[str, Field(alias="mimeType")]


StopReason = Literal["endTurn", "stopSequence", "maxTokens"]


class CreateMessageSamplingResult(BaseModel):
    """The client's response to a sampling/create_message request from the server."""

    role: Role
    content: TextContent | ImageContent
    model: str
    """The name of the model that generated the message."""
    stop_reason: StopReason | None = None
    """The reason why sampling stopped, if known."""


InitializeResponse = JSONRPCResponse[InitializeResult]
