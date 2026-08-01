"""Models used for representing an entire episode, or metadata/summaries of a TV episode."""

from pydantic import Field

from compuglobal.models.base import BaseCompuGlobalModel

from .subtitle import Subtitle


class EpisodeMetadata(BaseCompuGlobalModel):
    """The metadata for an episode of a TV show.

    Attributes
    ----------
    id : int
        The unique identifier of the episode
    key : str
        The episode key (S01E01)
    season : int
        The season number
    episode_number : int
        The episode number
    title : str
        The title of the episode.
    director : str
        The director of the episode.
    writer : str
        The writer(s) of the episode.
    original_air_date : str
        The original air date of the episode (yyyy-mm-dd)
    wiki_link : str
        The wikipedia link for the episode
    video_width : int
        The width of the video in pixels
    video_height : int
        The height of the video in pixels

    """

    id: int = Field(alias="Id")
    key: str = Field(alias="Key")
    season: int = Field(alias="Season", ge=0)
    episode_number: int = Field(alias="EpisodeNumber")
    title: str = Field(alias="Title")
    director: str = Field(alias="Director")
    writer: str = Field(alias="Writer")
    original_air_date: str = Field(alias="OriginalAirDate")
    wiki_link: str = Field(alias="WikiLink")
    video_width: int = Field(alias="VideoWidth", ge=0, default=480)
    video_height: int = Field(alias="VideoHeight", ge=0, default=360)


class EpisodeSummary(BaseCompuGlobalModel):
    """A summary of an episode of a TV show.

    Attributes
    ----------
    key : str
        The episode key (S01E01)
    season : int
        The season number
    episode_number : int
        The episode number
    title : str
        The title of the episode
    original_air_date : str
        The original air date of the episode (yyyy-mm-dd)
    frames : list[int]
        A list of 20 frame IDs distributed throughout the episode.

    """

    key: str = Field(alias="Key")
    season: int = Field(alias="Season")
    episode_number: int = Field(alias="EpisodeNumber")
    title: str = Field(alias="Title")
    original_air_date: str = Field(alias="OriginalAirDate")
    frames: list[int] = Field(alias="Frames")


class Episode(BaseCompuGlobalModel):
    """An entire episode of a TV show.

    Attributes
    ----------
    episode : EpisodeMetadata
        The metadata of the episode
    subtitles : list[Subtitle]
        A list of subtitles for the entire episode

    """

    episode: EpisodeMetadata = Field(alias="Episode")
    subtitles: list[Subtitle] = Field(alias="Subtitles")
