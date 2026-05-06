from pydantic import BaseModel, Field


class Subtitle(BaseModel):
    id: int = Field(alias="Id")
    representative_timestamp: int = Field(alias="RepresentativeTimestamp")
    key: str = Field(alias="Episode")
    start_timestamp: int = Field(alias="StartTimestamp", ge=0)
    end_timestamp: int = Field(alias="EndTimestamp", ge=0)
    content: str = Field(alias="Content")
    language: str = Field(alias="Language")
