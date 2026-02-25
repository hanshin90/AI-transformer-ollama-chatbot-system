## 모듈 로딩
from typing import Optional
from pydantic import BaseModel, EmailStr

## ========================
## 사용자 클래스 정의 
## ========================
class User(BaseModel):
    id: int
    name: str = 'Anonymous'     # 기본값 설정
    age: Optional[int] = None   # 선택적 필드

class User2(BaseModel):
    id: int
    name: str
    email: EmailStr  # 이메일 형식이 아닌 데이터는 오류 발생

## ========================
## 인스턴스 생성 및 정보 출력
## ========================
## => 단순 정보 출력
user = User(id=2)
print(user)


## => 예외 처리 
try:
    user = User2(id=1, name='Jane Doe', email='invalid-email')
except ValueError as e:
    print(e)


from pydantic import BaseModel, Field

class Input(BaseModel):
    a: int = Field(description="양의 정수")

class Input(BaseModel):
    a: int = Field(description="양의 정수")