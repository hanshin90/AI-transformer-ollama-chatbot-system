from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(..., description="검색 질의")
