from pydantic import BaseModel, ConfigDict, Field


class VideoGenerationRequest(BaseModel):
    # Allow clients to send either `fileId` (camelCase) or `file_id` (snake_case).
    file_id: str | None = Field(None, alias="fileId")
    title: str | None = "AI Tutor Video"
    template_name: str | None = "mc-template.mp4"

    # Pydantic v2 configuration: allow validation/population by field name when
    # aliases are used (clients may send `fileId` while server uses `file_id`).
    model_config = ConfigDict(validate_by_name=True)


class VideoGenerationResponse(BaseModel):
    video_id: str
    video_url: str
    status: str
