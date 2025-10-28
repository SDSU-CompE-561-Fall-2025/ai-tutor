from pydantic import BaseModel


class VideoGenerationRequest(BaseModel):
    title: str | None = "AI Tutor Video"
    template_name: str | None = "mc-template.mp4"


class VideoGenerationResponse(BaseModel):
    video_id: str
    video_url: str
    status: str
