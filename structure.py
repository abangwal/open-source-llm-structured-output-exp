from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage
from typing import List, Dict, Annotated, TypedDict, Sequence, Optional
import operator


class KeyPointsSchema(BaseModel):
    """Key points to consider while doing the given OBJECTIVE"""

    steps: List[str] = Field(
        description="Points to consider while completing given OBJECTIVE, points should be in correct order"
    )


class Data(BaseModel):
    """Year on year data of a field"""

    data: Dict[str, str] = Field(
        description="A dictionary of year on year data of a field, where keys are the year and values are the data for that year"
    )


# to convert to gbnf get beack to basics not schema in schema
class ExecutorSchema(BaseModel):
    """Result of the completing TASK"""

    points: List[str] = Field(
        description="Bullet points of Result after completing the TASK, points should be in correct order"
    )
    summary: str = Field(
        description="summary of the result of TASK, should be not repetative as bullet points"
    )

    field_data: Dict[str, Data] = Field(
        description="A dictinory of year-on-year data of different fields, keys of dictionary is the strings of the fileds and values are year on year data for that fields. The keys that are fields should be well descriptive."
    )


class SimpleExecutorSchema(BaseModel):
    """Result of the completing TASK"""

    points: List[str] = Field(
        description="Bullet points of Result after completing the TASK, points should be in correct order"
    )
    summary: str = Field(
        description="summary of the result of TASK, should be not repetative as bullet points"
    )

    field_data: Dict[str, str] = Field(
        description="A nested dictinory of year-on-year data of different fields, where keys of outer dictionary is the strings of the fileds and values of outer dictionary are year on year data for that fields. The keys of inner dictionary are the strings of years and values are data for that year. The keys that are fields should be well descriptive."
    )
