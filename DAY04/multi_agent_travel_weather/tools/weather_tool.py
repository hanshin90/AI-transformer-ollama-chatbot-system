
from langchain_core.tools import StructuredTool
from schemas.weather_schema import WeatherInput

def get_weather_info(city: str) -> str:
    return f"{city}의 현재 날씨는 '맑음'이며 온도는 22도입니다."

weather_tool = StructuredTool.from_function(
    func=get_weather_info,
    name="get_current_weather",
    description="특정 도시의 실시간 날씨 정보를 조회합니다.",
    args_schema=WeatherInput
)
