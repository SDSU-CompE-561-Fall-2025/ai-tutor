from pydantic import BaseModel, ConfigDict


class CourseBase(BaseModel):
    name: str


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
