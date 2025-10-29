import traceback
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import FileResponse

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.video_generation import VideoGenerationRequest, VideoGenerationResponse
from app.services.video_generation import VideoGenerationService

api_router = APIRouter(
    prefix="/video",
    tags=["Video"],
)


@api_router.post("/generate", response_model=VideoGenerationResponse)
async def generate_video(  # noqa: ANN201
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    query: Annotated[str | None, Query()] = None,
):
    """Generate a video with AI voiceover directly from a Google Drive file."""
    if not query:
        raise HTTPException(
            status_code=400,
            detail="Missing Google Drive file ID (query parameter)",
        )

    try:
        service = VideoGenerationService()

        # Generate unique filename for output
        video_filename = f"video_{request.title.replace(' ', '_').lower()}.mp4"  # pyright: ignore[reportOptionalMemberAccess]

        video_path = await service.create_video(
            fileid=query,
            userid=current_user.id,  # pyright: ignore[reportArgumentType]
            template_name=request.template_name,  # pyright: ignore[reportArgumentType]
            title=request.title,  # pyright: ignore[reportArgumentType]
            output_filename=video_filename,
        )

        # Schedule old video cleanup in background
        background_tasks.add_task(service.cleanup_old_videos)

        # Return structured response
        return VideoGenerationResponse(
            video_id=video_path.stem,
            video_url=service.get_video_url(video_path),
            status="completed",
        )

    except FileNotFoundError as e:
        raise e from HTTPException(status_code=404, detail=str(e))
    except Exception as e:  # noqa: BLE001
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Video generation failed: {e}")  # noqa: B904


@api_router.get("/{filename}")
async def serve_video(filename: str) -> FileResponse | HTTPException:
    """Serve generated video files."""
    service = VideoGenerationService()
    video_path = service.outputs_dir / filename

    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(path=str(video_path), media_type="video/mp4", filename=filename)


@api_router.get("/templates/list")
async def list_templates() -> dict:
    """List available video templates."""
    service = VideoGenerationService()
    templates = []

    for template_file in service.templates_dir.glob("*.mp4"):
        templates.append(  # noqa: PERF401
            {
                "name": template_file.name,
                "size": template_file.stat().st_size,
                "created": template_file.stat().st_mtime,
            },
        )

    return {"templates": templates}


@api_router.delete("/cleanup")
async def cleanup_videos() -> dict:
    """Manually trigger cleanup of old videos."""
    service = VideoGenerationService()
    service.cleanup_old_videos()
    return {"message": "Cleanup completed"}
