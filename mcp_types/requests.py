from __future__ import annotations as _annotations

from typing import Any, Literal, NotRequired
from pydantic import BaseModel, Discriminator, Field
from typing_extensions import Annotated, TypedDict
from mcp_types.jsonrpc import JSONRPCRequest


class RootsCapability(TypedDict, total=False):
    """Ability to provide filesystem roots.

    See more on <https://modelcontextprotocol.io/specification/2025-06-18/client/roots>.
    """

    list_changed: bool
    """indicates whether the client will emit notifications when the list of roots changes."""


class SamplingCapability(TypedDict):
    """Support for LLM sampling requests.

    See more on <https://modelcontextprotocol.io/specification/2025-06-18/client/sampling>.
    """


class ElicitationCapability(BaseModel):
    """Capability for elicitation operations.

    See more on <https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation>.
    """


class ClientCapabilities(TypedDict):
    """Capabilities a client may support.

    Known capabilities are defined here, in this schema, but this is not a closed set:
    any client can define its own, additional capabilities.
    """

    roots: NotRequired[RootsCapability]
    """Ability to provide filesystem roots.

    See more on <https://modelcontextprotocol.io/specification/2025-06-18/client/roots>.
    """

    sampling: NotRequired[SamplingCapability]
    """Support for LLM sampling requests.

    See more on <https://modelcontextprotocol.io/specification/2025-06-18/client/sampling>.
    """

    elicitation: NotRequired[ElicitationCapability]
    """Support for elicitation requests.

    See more on <https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation>.
    """

    experimental: NotRequired[dict[str, dict[str, Any]]]
    """Experimental, non-standard capabilities that the client supports."""


class Implementation(BaseModel):
    name: str
    title: str | None = None
    version: str


class InitializeRequestParams(TypedDict):
    """Parameters for the initialize request."""

    protocol_version: Annotated[Literal["2025-06-18"], Field(alias="protocolVersion")]
    """The latest version of the Model Context Protocol that the client supports."""

    capabilities: ClientCapabilities

    client_info: Annotated[Implementation, Field(alias="clientInfo")]


class TextContent(TypedDict):
    """A text content."""

    type: Literal["text"]
    """The type of content."""

    text: str
    """The text content."""


class ImageContent(TypedDict):
    """An image content."""

    type: Literal["image"]
    """The type of content."""

    data: str
    """Base64 encoded image data."""

    mime_type: Annotated[str, Field(alias="mimeType")]
    """The MIME type of the image."""


class AudioContent(TypedDict):
    """An audio content."""

    type: Literal["audio"]
    """The type of content."""

    data: str
    """Base64 encoded audio data."""

    mime_type: Annotated[str, Field(alias="mimeType")]
    """The MIME type of the audio."""


class TextResourceContents(TypedDict):
    """Text resource contents."""

    uri: str
    """The URI of this resource."""

    text: str
    """The text content of the resource."""

    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    """The MIME type of this resource, if known."""


class BlobResourceContents(TypedDict):
    """Binary resource contents."""

    uri: str
    """The URI of this resource."""

    blob: str
    """A base64-encoded string representing the binary data."""

    mime_type: Annotated[NotRequired[str], Field(alias="mimeType")]
    """The MIME type of this resource, if known."""


class EmbeddedResource(TypedDict):
    """An embedded resource."""

    type: Literal["resource"]
    """The type of resource."""

    resource: TextResourceContents | BlobResourceContents


Role = Literal["user", "assistant"]
Content = Annotated[TextContent | ImageContent | AudioContent | EmbeddedResource, Discriminator("type")]


class SamplingMessage(TypedDict):
    role: Role
    content: Content


class ModelHint(TypedDict):
    """A hint for the model to use."""

    name: str
    """The name of the model."""


class ModelPreferences(TypedDict):
    """The server's preferences for which model to select."""

    cost_priority: Annotated[NotRequired[float], Field(alias="costPriority")]
    """How important is minimizing costs? Higher values prefer cheaper models."""

    speed_priority: Annotated[NotRequired[float], Field(alias="speedPriority")]
    """How important is low latency? Higher values prefer faster models."""

    intelligence_priority: Annotated[NotRequired[float], Field(alias="intelligencePriority")]
    """How important are advanced capabilities? Higher values prefer more capable models."""

    hints: NotRequired[list[ModelHint]]


class CreateMessageSamplingRequestParams(TypedDict):
    """Parameters for creating a message."""

    messages: list[SamplingMessage]

    model_preferences: Annotated[NotRequired[ModelPreferences], Field(alias="modelPreferences")]
    """The server's preferences for which model to select.

    The client MAY ignore these preferences.

    See more on <https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#model-preferences>.
    """
    system_prompt: Annotated[NotRequired[str], Field(alias="systemPrompt")]
    """An optional system prompt the server wants to use for sampling."""

    temperature: NotRequired[float]
    """The temperature to use for sampling."""

    max_tokens: Annotated[int, Field(alias="maxTokens")]
    """The maximum number of tokens to sample, as requested by the server."""

    stop_sequences: Annotated[NotRequired[list[str]], Field(alias="stopSequences")]
    """Stop sequences for sampling."""


class GetPromptRequestParams(TypedDict):
    """Parameters for getting a message."""

    name: str
    """The name of the message to get."""

    arguments: NotRequired[dict[str, str]]
    """Arguments to use for templating the message."""


class ListResourcesRequestParams(TypedDict, total=False):
    """Parameters for listing resources."""

    cursor: str
    """An opaque token representing the current pagination position."""


class ReadResourceRequestParams(TypedDict):
    """Parameters for reading a resource."""

    uri: str
    """The URI of the resource to read."""


class ListResourceTemplatesRequestParams(TypedDict, total=False):
    """Parameters for listing resource templates."""

    cursor: str
    """An opaque token representing the current pagination position."""


class SubscribeRequestParams(TypedDict):
    """Parameters for subscribing to resource updates."""

    uri: str
    """The URI of the resource to subscribe to."""


class UnsubscribeRequestParams(TypedDict):
    """Parameters for unsubscribing from resource updates."""

    uri: str
    """The URI of the resource to unsubscribe from."""


class ListPromptsRequestParams(TypedDict, total=False):
    """Parameters for listing prompts."""

    cursor: str
    """An opaque token representing the current pagination position."""


class ListToolsRequestParams(TypedDict, total=False):
    """Parameters for listing tools."""

    cursor: str
    """An opaque token representing the current pagination position."""


class CallToolRequestParams(TypedDict):
    """Parameters for calling a tool."""

    name: str
    """The name of the tool to call."""

    arguments: NotRequired[dict[str, Any]]
    """Arguments to pass to the tool."""


class SetLevelRequestParams(TypedDict):
    """Parameters for setting logging level."""

    level: str
    """The logging level to set."""


class CompleteRequestParams(TypedDict):
    """Parameters for completion request."""

    ref: dict[str, Any]
    """Reference to the resource being completed."""

    argument: dict[str, str]
    """The argument information for completion."""

    context: NotRequired[dict[str, Any]]
    """Additional context for completion."""


class PingRequestParams(TypedDict):
    """A ping, issued by either the server or the client, to check that the other party is still alive.

    The receiver must promptly respond, or else may be disconnected.
    """


class CreateMessageRequestParams(TypedDict):
    """Parameters for creating a message."""

    messages: list[SamplingMessage]
    """The messages to send to the LLM."""

    max_tokens: Annotated[int, Field(alias="maxTokens")]
    """The maximum number of tokens to sample."""

    model_preferences: Annotated[NotRequired[ModelPreferences], Field(alias="modelPreferences")]
    """The server's preferences for which model to select."""

    system_prompt: Annotated[NotRequired[str], Field(alias="systemPrompt")]
    """An optional system prompt the server wants to use for sampling."""

    temperature: NotRequired[float]
    """The temperature to use for sampling."""

    stop_sequences: Annotated[NotRequired[list[str]], Field(alias="stopSequences")]
    """Stop sequences for sampling."""

    include_context: Annotated[NotRequired[str], Field(alias="includeContext")]
    """A request to include context from MCP servers."""

    metadata: NotRequired[dict[str, Any]]
    """Optional metadata to pass through to the LLM provider."""


class ListRootsRequestParams(TypedDict, total=False):
    """Parameters for listing roots."""


class ElicitRequestParams(TypedDict):
    """Parameters for elicitation requests."""

    message: str
    """The message to present to the user."""
    requested_schema: Annotated[dict[str, Any], Field(alias="requestedSchema")]
    """A restricted subset of JSON Schema."""


InitializeRequest = JSONRPCRequest[Literal["initialize"], InitializeRequestParams]
"""This request is sent from the client to the server when it first connects, asking it to begin initialization."""

PingRequest = JSONRPCRequest[Literal["ping"], PingRequestParams]
"""A ping, issued by either the server or the client, to check that the other party is still alive.

The receiver must promptly respond, or else may be disconnected.
"""

InitializedNotification = JSONRPCRequest[Literal["notifications/initialized"]]
"""his notification is sent from the client to the server after initialization has finished."""

ListRootsRequest = JSONRPCRequest[Literal["roots/list"]]
"""Retrieve the list of filesystem roots."""

ListChangedRootsNotification = JSONRPCRequest[Literal["notifications/roots/list_changed"]]
"""A notification that the list of filesystem roots has changed."""

CreateMessageSamplingRequest = JSONRPCRequest[Literal["sampling/createMessage"], CreateMessageSamplingRequestParams]

GetPromptRequest = JSONRPCRequest[Literal["prompts/get"], GetPromptRequestParams]

ListResourcesRequest = JSONRPCRequest[Literal["resources/list"], ListResourcesRequestParams]
"""Sent from the client to request a list of resources the server has."""

ReadResourceRequest = JSONRPCRequest[Literal["resources/read"], ReadResourceRequestParams]
"""Sent from the client to the server, to read a specific resource URI."""

ListResourceTemplatesRequest = JSONRPCRequest[Literal["resources/templates/list"], ListResourceTemplatesRequestParams]
"""Sent from the client to request a list of resource templates the server has."""

SubscribeRequest = JSONRPCRequest[Literal["resources/subscribe"], SubscribeRequestParams]
"""Sent from the client to request resources/updated notifications from the server."""

UnsubscribeRequest = JSONRPCRequest[Literal["resources/unsubscribe"], UnsubscribeRequestParams]
"""Sent from the client to request cancellation of resources/updated notifications."""

ListPromptsRequest = JSONRPCRequest[Literal["prompts/list"], ListPromptsRequestParams]
"""Sent from the client to request a list of prompts and prompt templates the server has."""

ListToolsRequest = JSONRPCRequest[Literal["tools/list"], ListToolsRequestParams]
"""Sent from the client to request a list of tools the server has."""

CallToolRequest = JSONRPCRequest[Literal["tools/call"], CallToolRequestParams]
"""Used by the client to invoke a tool provided by the server."""

SetLevelRequest = JSONRPCRequest[Literal["logging/setLevel"], SetLevelRequestParams]
"""A request from the client to the server, to enable or adjust logging."""

CompleteRequest = JSONRPCRequest[Literal["completion/complete"], CompleteRequestParams]
"""A request from the client to the server, to ask for completion options."""


CreateMessageRequest = JSONRPCRequest[Literal["sampling/createMessage"], CreateMessageRequestParams]
"""A request from the server to sample an LLM via the client."""

ListRootsRequest = JSONRPCRequest[Literal["roots/list"], ListRootsRequestParams]
"""Sent from the server to request a list of root URIs from the client."""

ElicitRequest = JSONRPCRequest[Literal["elicitation/create"], ElicitRequestParams]
"""A request from the server to elicit additional information from the user via the client."""

ClientNotification = InitializedNotification | ListChangedRootsNotification
ClientRequest = (
    InitializeRequest
    | PingRequest
    | ListResourcesRequest
    | ListResourceTemplatesRequest
    | ReadResourceRequest
    | SubscribeRequest
    | UnsubscribeRequest
    | ListPromptsRequest
    | GetPromptRequest
    | ListToolsRequest
    | CallToolRequest
    | SetLevelRequest
    | CompleteRequest
)
ServerRequest = PingRequest | CreateMessageRequest | ListRootsRequest | ElicitRequest
