from typing import Literal, NotRequired
from pydantic import Discriminator
from typing_extensions import Annotated, TypedDict
from mcp_types.jsonrpc import JSONRPCError, JSONRPCRequest, JSONRPCResponse

MethodNotFoundCode = Literal[-32601]
InternalErrorCode = Literal[-32603]


class RootsCapability(TypedDict, total=False):
    """Ability to provide filesystem roots.

    See more on <https://modelcontextprotocol.io/specification/2025-03-26/client/roots>.
    """

    list_changed: bool
    """indicates whether the client will emit notifications when the list of roots changes."""


class SamplingCapability(TypedDict):
    """Support for LLM sampling requests.

    See more on <https://modelcontextprotocol.io/specification/2025-03-26/client/sampling>.
    """


class ClientCapabilities(TypedDict):
    roots: RootsCapability
    """Ability to provide filesystem roots.

    See more on <https://modelcontextprotocol.io/specification/2025-03-26/client/roots>.
    """

    sampling: SamplingCapability
    """Support for LLM sampling requests.

    See more on <https://modelcontextprotocol.io/specification/2025-03-26/client/sampling>.
    """


class InitializeRequestParams(TypedDict):
    """Parameters for the initialize request."""

    protocol_version: Literal["2024-11-05"]
    """The latest version of the Model Context Protocol that the client supports."""
    capabilities: ClientCapabilities
    clientInfo: Implementation


class _Root(TypedDict):
    uri: str
    """Unique identifier for the root. This MUST be a file:// URI in the current specification."""
    name: NotRequired[str]
    """Optional human-readable name for display purposes."""


class ListRootResult(TypedDict):
    """The result of the list roots request."""

    roots: list[_Root]


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


Role = Literal["user", "assistant"]
Content = Annotated[TextContent | ImageContent | AudioContent, Discriminator("type")]


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

    See more on <https://modelcontextprotocol.io/specification/2025-03-26/client/sampling#model-preferences>.
    """
    system_prompt: NotRequired[str]
    """An optional system prompt the server wants to use for sampling."""
    temperature: NotRequired[float]
    max_tokens: int
    """The maximum number of tokens to sample, as requested by the server."""
    stop_sequences: NotRequired[list[str]]


StopReason = Literal["endTurn", "stopSequence", "maxTokens"]


class CreateMessageSamplingResult(TypedDict):
    """The client's response to a sampling/create_message request from the server."""

    role: Role
    content: TextContent | ImageContent
    model: str
    """The name of the model that generated the message."""
    stop_reason: NotRequired[StopReason]
    """The reason why sampling stopped, if known."""


ListRootNotFound = JSONRPCError[MethodNotFoundCode, Literal["Roots not supported"]]
ListRootInternalError = JSONRPCError[InternalErrorCode, Literal["Internal error"]]

InitializeRequest = JSONRPCRequest[Literal["initialize"]]

ListRootsRequest = JSONRPCRequest[Literal["roots/list"]]
"""Retrieve the list of filesystem roots."""

ListRootsResponse = JSONRPCResponse[ListRootResult, ListRootNotFound | ListRootInternalError]
"""The result of the list roots request."""

ListChangedRootsNotification = JSONRPCRequest[Literal["notifications/roots/list_changed"]]
"""A notification that the list of filesystem roots has changed."""

CreateMessageSamplingRequest = JSONRPCRequest[Literal["sampling/createMessage"], CreateMessageSamplingRequestParams]
CreateMessageSamplingResponse = JSONRPCResponse[CreateMessageSamplingResult, ListRootInternalError]
