"""The configuration for a CGHMC API (title + font)."""

from dataclasses import dataclass, field

from compuglobal.models.overlay import OverlayFormat


@dataclass
class CompuGlobalAPIConfig:
    """The configuration for a CompuGlobal API."""

    #: The title of the API
    title: str

    #: The default formatting to use in all stream/comic overlays (subtitles)
    default_format: OverlayFormat = field(default_factory=OverlayFormat)
