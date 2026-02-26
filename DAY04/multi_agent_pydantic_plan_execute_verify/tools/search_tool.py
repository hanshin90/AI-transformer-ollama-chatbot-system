from langchain_core.tools import StructuredTool
from schemas.search_schema import SearchInput

def _search(query: str) -> str:
    return f"[SEARCH RESULT] {query} 관련 문서 요약"

search_tool = StructuredTool.from_function(
    name="search",
    description="사내 문서 검색 도구",
    args_schema=SearchInput,
    func=_search,
)
