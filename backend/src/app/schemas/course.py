from pydantic import BaseModel, ConfigDict, Field, field_validator


class CourseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    description: str = Field(default="", max_length=100)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, course_name: str) -> str:
        if not course_name.strip():
            msg = "Course name cannot be blank"
            raise ValueError(msg)
        return course_name.strip()

class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
