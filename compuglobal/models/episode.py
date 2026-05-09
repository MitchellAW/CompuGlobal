from pydantic import BaseModel, Field


class Episode(BaseModel, frozen=True):
    """An episode of a TV show.

    Attributes
    ----------
    id: int
        The unique identifier of the episode
    key: str
        The episode key (S01E01)
    season: int
        The season number
    episode_number: int
        The episode number
    title: str
        The title of the episode.
    director: str
        The director of the episode.
    writer: str
        The writer(s) of the episode.
    original_air_data: str
        The original air date of the episode (yyyy-mm-dd)
    wiki_link: str
        The wikipedia link for the episode
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
