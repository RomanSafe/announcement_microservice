# Contains Pydantic data classes, used by Lambda functions
from pydantic import BaseModel, Field
from typing import Optional


class NewAnnouncement(BaseModel):
    title: str = Field(alias="title", min_length=4, max_length=2048)
    description: str = Field(alias="description", min_length=4)


class Pagination(BaseModel):
    """I used dash as word separator in attribute names here to get
    possibility parse query parameters which have url format.
    """
    title: str = Field(
        alias="title",
        description="title attribute of 'LastEvaluatedKey'",
        min_length=4,
        max_length=2048,
    )
    date_time: str = Field(
        alias="date-time",
        description="date-time attribute of 'LastEvaluatedKey'",
        min_length=32,
        max_length=32,
    )
    next_page_number: int = Field(alias="next-page-number", ge=2)


class PositiveResponse(BaseModel):
    page: int = Field(alias="page", description="Current page number", ge=1)
    announcements: list = Field(
        alias="announcements", description="List of announcements"
    )
    next_page: Optional[str] = Field(
        alias="next_page",
        description="URL of the next page if not all results shown on the current page",
    )
