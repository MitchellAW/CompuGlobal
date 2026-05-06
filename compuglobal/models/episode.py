from pydantic import BaseModel, Field


class Episode(BaseModel):
    id: int = Field(alias="Id")
    key: str = Field(alias="Key")
    season: int = Field(alias="Season", ge=0)
    episode_number: int = Field(alias="EpisodeNumber")
    title: str = Field(alias="Title")
    director: str = Field(alias="Director")
    writer: str = Field(alias="Writer")
    original_air_date: str = Field(alias="OriginalAirDate")
    wiki_link: str = Field(alias="WikiLink")
