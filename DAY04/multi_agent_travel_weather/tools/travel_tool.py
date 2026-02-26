## ============================================================
##          구조화된 도구(Tools) 생성
## ============================================================
## -> 특정 작업(여행지 추천, 날씨 조회)에 특화된 역할을 수행
## ============================================================
from langchain_core.tools import StructuredTool
from schemas.travel_schema import TravelInput


## ---------------------------------
##
## ---------------------------------
def get_travel_info(location: str) -> str:
    recommendations = {"서울": "경복궁, 명동", "부산": "해운대, 광안리"}
    return recommendations.get(location, f"{location}에 대한 정보가 아직 없습니다.")


## ---------------------------------
## 
## ---------------------------------
travel_tool = StructuredTool.from_function(
    func=get_travel_info,
    name="get_travel_recommendation",
    description="특정 지역의 인기 여행 명소를 추천합니다.",
    args_schema=TravelInput
)
