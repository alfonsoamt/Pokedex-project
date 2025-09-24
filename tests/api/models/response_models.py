from typing import List, Literal, Union, Annotated
from pydantic import BaseModel, Field, HttpUrl, RootModel

class Generation(BaseModel):
    """Model for a generation object."""
    id: int
    name: str

class PokemonData(BaseModel):
    """Model for the data of a 'pokemon' type event."""
    id: int = Field(gt=0)
    name: str
    sprite: HttpUrl
    types: List[str] = Field(min_length=1, max_length=2)

class PaginationData(BaseModel):
    """Model for the data of a 'pagination' type event."""
    total_items: int
    total_pages: int
    current_page: int

class DoneData(BaseModel):
    """Model for the data of a 'done' type event."""
    message: str

class PaginationEvent(BaseModel):
    """Model for the 'pagination' event."""
    type: Literal["pagination"]
    data: PaginationData

class PokemonEvent(BaseModel):
    """Model for the 'pokemon' event."""
    type: Literal["pokemon"]
    data: PokemonData

class DoneEvent(BaseModel):
    """Model for the 'done' event."""
    type: Literal["done"]
    data: DoneData

# This tells Pydantic to look at the 'type' field to decide which model to use
StreamEvent = Annotated[
    Union[PaginationEvent, PokemonEvent, DoneEvent],
    Field(discriminator="type"),
]

class StreamEvents(RootModel):
    """
    A root model to validate a list of stream events using the discriminated union.
    """
    root: List[StreamEvent]