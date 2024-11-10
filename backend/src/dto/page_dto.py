from pydantic import BaseModel, Field

class NextPageMetaDTO(BaseModel):
    last_id: int
    limit: int
    has_more: bool = Field(default=False)