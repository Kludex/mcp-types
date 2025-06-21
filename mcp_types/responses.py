from __future__ import annotations as _annotations
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field

from mcp_types.jsonrpc import JSONRPCResponse
from mcp_types.requests import Role, TextResourceContents, BlobResourceContents

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


class AudioContent(BaseModel):
    """An audio content."""

    type: Literal["audio"] = "audio"
    """The type of content."""
    data: str
    """Base64 encoded audio data."""
    mime_type: Annotated[str, Field(alias="mimeType")]


ContentBlock = TextContent | ImageContent | AudioContent
StopReason = Literal["endTurn", "stopSequence", "maxTokens"]


class Resource(BaseModel):
    """A known resource that the server is capable of reading."""

    uri: str
    """The URI of this resource."""
    name: str
    """The name of the resource."""
    title: str | None = None
    """The title of the resource."""
    description: str | None = None
    """A description of what this resource represents."""
    mime_type: Annotated[str | None, Field(alias="mimeType")] = None
    """The MIME type of this resource, if known."""
    size: int | None = None
    """The size of the resource in bytes."""
    _meta: dict[str, Any] | None = None


class ResourceTemplate(BaseModel):
    """A template description for resources available on the server."""

    uri_template: Annotated[str, Field(alias="uriTemplate")]
    """A URI template that can be used to construct resource URIs."""
    name: str
    """The name of the template."""
    title: str | None = None
    """The title of the template."""
    description: str | None = None
    """A description of what this template is for."""
    mime_type: Annotated[str | None, Field(alias="mimeType")] = None
    """The MIME type for all resources that match this template."""
    _meta: dict[str, Any] | None = None


class ListResourcesResult(BaseResult):
    """The server's response to a resources/list request from the client."""

    resources: list[Resource]
    """List of resources available."""
    next_cursor: Annotated[str | None, Field(alias="nextCursor")] = None
    """An opaque token for pagination."""


class ListResourceTemplatesResult(BaseResult):
    """The server's response to a resources/templates/list request from the client."""

    resource_templates: Annotated[list[ResourceTemplate], Field(alias="resourceTemplates")]
    """List of resource templates available."""
    next_cursor: Annotated[str | None, Field(alias="nextCursor")] = None
    """An opaque token for pagination."""


class ReadResourceResult(BaseResult):
    """The server's response to a resources/read request from the client."""

    contents: list[TextResourceContents | BlobResourceContents]
    """The contents of the resource."""


class CreateMessageSamplingResult(BaseModel):
    """The client's response to a sampling/create_message request from the server."""

    role: Role
    content: TextContent | ImageContent | AudioContent
    model: str
    """The name of the model that generated the message."""
    stop_reason: Annotated[StopReason | None, Field(alias="stopReason")] = None
    """The reason why sampling stopped, if known."""


class Tool(BaseModel):
    """Definition for a tool the client can call."""

    name: str
    """The name of the tool."""
    title: str | None = None
    """The title of the tool."""
    description: str | None = None
    """A description of the tool."""
    input_schema: Annotated[dict[str, Any], Field(alias="inputSchema")]
    """A JSON Schema object defining the expected parameters for the tool."""
    output_schema: Annotated[dict[str, Any] | None, Field(alias="outputSchema")] = None
    """An optional JSON Schema object defining the structure of the tool's output."""
    _meta: dict[str, Any] | None = None


class ListToolsResult(BaseResult):
    """The server's response to a tools/list request from the client."""

    tools: list[Tool]
    """List of tools available."""
    next_cursor: Annotated[str | None, Field(alias="nextCursor")] = None
    """An opaque token for pagination."""


class CallToolResult(BaseResult):
    """The server's response to a tool call."""

    content: list[ContentBlock]
    """A list of content objects that represent the unstructured result of the tool call."""
    is_error: Annotated[bool | None, Field(alias="isError")] = None
    """Whether the tool call ended in an error."""
    structured_content: Annotated[dict[str, Any] | None, Field(alias="structuredContent")] = None
    """An optional JSON object that represents the structured result of the tool call."""


class PromptArgument(BaseModel):
    """Describes an argument that a prompt can accept."""

    name: str
    """The name of the argument."""
    title: str | None = None
    """The title of the argument."""
    description: str | None = None
    """A description of the argument."""
    required: bool | None = None
    """Whether this argument must be provided."""


class Prompt(BaseModel):
    """A prompt or prompt template that the server offers."""

    name: str
    """The name of the prompt."""
    title: str | None = None
    """The title of the prompt."""
    description: str | None = None
    """An optional description of what this prompt provides."""
    arguments: list[PromptArgument] | None = None
    """A list of arguments to use for templating the prompt."""
    _meta: dict[str, Any] | None = None


class PromptMessage(BaseModel):
    """Describes a message returned as part of a prompt."""

    role: Role
    """The role of the message sender."""
    content: ContentBlock
    """The content of the message."""


class ListPromptsResult(BaseResult):
    """The server's response to a prompts/list request from the client."""

    prompts: list[Prompt]
    """List of prompts available."""
    next_cursor: Annotated[str | None, Field(alias="nextCursor")] = None
    """An opaque token for pagination."""


class GetPromptResult(BaseResult):
    """The server's response to a prompts/get request from the client."""

    description: str | None = None
    """An optional description for the prompt."""
    messages: list[PromptMessage]
    """The messages that make up the prompt."""


class CompleteResult(BaseResult):
    """The server's response to a completion/complete request."""

    completion: dict[str, Any]
    """The completion information."""


class Root(BaseModel):
    """Represents a root directory or file that the server can operate on."""

    uri: str
    """The URI identifying the root."""
    name: str | None = None
    """An optional name for the root."""
    _meta: dict[str, Any] | None = None


class ListRootsResult(BaseResult):
    """The client's response to a roots/list request from the server."""

    roots: list[Root]
    """List of root directories or files."""


class ElicitResult(BaseResult):
    """The client's response to an elicitation request."""

    action: Literal["accept", "decline", "cancel"]
    """The user action in response to the elicitation."""
    content: dict[str, str | int | bool] | None = None
    """The submitted form data, only present when action is 'accept'."""


class CreateMessageResult(BaseResult):
    """The client's response to a sampling/createMessage request from the server."""

    role: Role
    """The role of the message."""
    content: ContentBlock
    """The content of the message."""
    model: str
    """The name of the model that generated the message."""
    stop_reason: Annotated[str | None, Field(alias="stopReason")] = None
    """The reason why sampling stopped, if known."""


InitializeResponse = JSONRPCResponse[InitializeResult]
ListResourcesResponse = JSONRPCResponse[ListResourcesResult]
ListResourceTemplatesResponse = JSONRPCResponse[ListResourceTemplatesResult]
ReadResourceResponse = JSONRPCResponse[ReadResourceResult]
ListPromptsResponse = JSONRPCResponse[ListPromptsResult]
GetPromptResponse = JSONRPCResponse[GetPromptResult]
ListToolsResponse = JSONRPCResponse[ListToolsResult]
CallToolResponse = JSONRPCResponse[CallToolResult]
CompleteResponse = JSONRPCResponse[CompleteResult]
ListRootsResponse = JSONRPCResponse[ListRootsResult]
ElicitResponse = JSONRPCResponse[ElicitResult]
CreateMessageResponse = JSONRPCResponse[CreateMessageResult]

ClientResponse = CreateMessageResponse | ListRootsResponse | ElicitResponse

ServerResponse = (
    InitializeResponse
    | ListResourcesResponse
    | ListResourceTemplatesResponse
    | ReadResourceResponse
    | ListPromptsResponse
    | GetPromptResponse
    | ListToolsResponse
    | CallToolResponse
    | CompleteResponse
)
