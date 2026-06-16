"""The configuration for a CGHMC API (title + font)."""

import dataclasses
import logging
from dataclasses import dataclass, field

from compuglobal.models.font import FontFamily
from compuglobal.models.overlay import OverlayFormat

log = logging.getLogger(__name__)


@dataclass
class CompuGlobalAPIConfig:
    """The configuration for a CompuGlobal API."""

    #: The title of the API
    title: str

    #: The allowed fonts for this API
    allowed_fonts: list[FontFamily] = field(default_factory=FontFamily.universal_fonts)

    #: The default formatting to use in all stream/comic overlays (subtitles)
    default_format: OverlayFormat = field(default_factory=OverlayFormat)

    def __post_init__(self) -> None:
        """Validate font family is allowed in API. If not allowed, use IMPACT font."""
        if self.default_format.font_family not in self.allowed_fonts:
            log.warning("Chosen font is not allowed for this API. Using IMPACT font instead.")
            self.default_format = dataclasses.replace(self.default_format, font_family=FontFamily.IMPACT)
