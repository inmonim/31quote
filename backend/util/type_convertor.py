from model import Base
from pydantic import BaseModel
from typing import TypeVar, Type

T = TypeVar("T", bound=BaseModel)
BM_T = TypeVar("BM_T", bound=Base)

def dto_to_model(dto: BaseModel, model : Type[BM_T]) -> BM_T:
    """
    pydantic BaseModel 타입인 dto를 sqlalchemy Declarative 클래스 모델로 변환하는 함수
    
    모델 인스턴스를 생성한 뒤, dto.model_dump()는 dto의 데이터를 dict로 바꾸고, hasattr로 포착된 컬럼에 setattr로 데이터를 넣어 반환한다.
    
    Args:
        dto (BaseModel): BaseModel을 상속한 세부 DTO 클래스 인스턴스 객체
        model (DeclarativeBase): sqlachemy로 선언한 모델 클래스
        
    Returns:
        return_type : 두 번째 인자인 model로 주입한 클래스의 인스턴스 객체
    """
    model_instance = model()
    for field, value in dto.model_dump().items():
        if hasattr(model_instance, field):
            setattr(model_instance, field, value)
    return model_instance


def _to_dict(model_instance: Base) -> dict:
    """
    Column의 유무를 확인하고, 해당 컬럼에 할당된 값을 dict 타입으로 변환시킴.
    
    model -> dto, model -> Json으로 사용가능하며, 두 함수의 내부 함수로만 쓰인다.
    """
    dict_response = {}
    for column in model_instance.__table__.columns:
        if getattr(model_instance, column.name):
            if isinstance(column, Base):
                dict_response[column.name] = _to_dict(column)
            else:
                dict_response[column.name] = getattr(model_instance, column.name)
    return dict_response


def model_to_dto(model_instance: Base, dto: Type[T]) -> T:
    """
    sqlalchemy Declarative 클래스 모델을 pydantic BaseModel의 하위 타입인 DTO로 변환하는 함수
    
    BaseModel의 model_validate는 dict값을 통해 dto를 자동으로 생성함.
    """
    x = _to_dict(model_instance)
    return dto.model_validate(x)


def model_to_json(model_instance: Base, dto: BaseModel) -> dict:
    """
    model 객체를 딕셔너리로 바꾼 뒤, JSONResponse로 반환 가능한 dict 타입의 json 형식(모든 키 밸류 str, int, bool로 지정)으로 변환하는 함수
    """
    x = _to_dict(model_instance)
    return dto.model_validate(x).model_dump(mode="json")