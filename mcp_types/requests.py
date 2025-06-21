from __future__ import annotations as _annotations

from typing import Any, Literal, NotRequired
from pydantic import BaseModel, Discriminator
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

    protocol_version: Literal["2025-06-18"]
    """The latest version of the Model Context Protocol that the client supports."""
    capabilities: ClientCapabilities
    clientInfo: Implementation


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
    mimeType: str
    """The MIME type of the image."""


class AudioContent(TypedDict):
    """An audio content."""

    type: Literal["audio"]
    """The type of content."""
    data: str
    """Base64 encoded audio data."""
    mimeType: str
    """The MIME type of the audio."""


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
    cost_priority: NotRequired[float]
    """How important is minimizing costs? Higher values prefer cheaper models."""
    speed_priority: NotRequired[float]
    """How important is low latency? Higher values prefer faster models."""
    intelligence_priority: NotRequired[float]
    """How important are advanced capabilities? Higher values prefer more capable models."""

    hints: NotRequired[list[ModelHint]]


class CreateMessageSamplingRequestParams(TypedDict):
    """Parameters for creating a message."""

    messages: list[SamplingMessage]
    model_preferences: ModelPreferences
    """The server's preferences for which model to select.

    The client MAY ignore these preferences.

    See more on <https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#model-preferences>.
    """
    system_prompt: NotRequired[str]
    """An optional system prompt the server wants to use for sampling."""
    temperature: NotRequired[float]
    max_tokens: int
    """The maximum number of tokens to sample, as requested by the server."""
    stop_sequences: NotRequired[list[str]]


class GetPromptRequestParams(TypedDict):
    """Parameters for getting a message."""

    name: str
    """The name of the message to get."""

    arguments: NotRequired[dict[str, str]]
    """Arguments to use for templating the message."""


class PingRequestParams(TypedDict):
    """A ping, issued by either the server or the client, to check that the other party is still alive.

    The receiver must promptly respond, or else may be disconnected.
    """


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

ClientNotification = InitializedNotification
ClientRequest = InitializeRequest | PingRequest
ServerRequest = PingRequest
