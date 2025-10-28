import time
import uuid
from pathlib import Path

from elevenlabs.client import ElevenLabs
from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip
from openai import OpenAI

from app.core.settings import settings
from app.services.google_drive import GoogleDriveService


class VideoGenerationService:
    """Service for generating educational videos with AI voiceover."""

    def __init__(self) -> None:
        self.client = ElevenLabs(api_key=settings.eleven_key)
        self.voice_id = "tnSpp4vdxKPjI9w0GnoV"
        self.openAiClient = OpenAI(api_key=settings.openai_key)

        self.project_root = Path(__file__).parent.parent.parent.parent
        self.templates_dir = self.project_root / "assets" / "templates"
        self.outputs_dir = self.project_root / "assets" / "outputs"
        self.temp_dir = self.project_root / "assets" / "temp"

        # Ensure directories exist
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    async def generate_audio(
        self,
        text: str,
        output_path: Path | None = None,
    ) -> Path:
        """Generate audio from text using ElevenLabs."""
        if output_path is None:
            output_path = self.temp_dir / f"audio_{uuid.uuid4().hex}.mp3"

        # audio generation starts here

        audio = self.client.text_to_speech.convert(
            voice_id=self.voice_id,
            model_id="eleven_multilingual_v2",
            text=text,
            output_format="mp3_44100_128",
        )
        # writing into audio file

        with open(output_path, "wb") as f:  # noqa: ASYNC230, PTH123
            for chunk in audio:  # noqa: FURB122
                f.write(chunk)

        return output_path

    async def create_video(
        self,
        fileid: str,
        userid: int,
        template_name: str = "mc-template.mp4",
        title: str = "AI Tutor Video",
        output_filename: str | None = None,
    ) -> Path:
        """Create a video with audio and captions."""

        # Generate text dialogue
        text = await self.create_text(fileid, userid)

        # Generate audio
        audio_path = await self.generate_audio(text)

        # Load template video
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            msg = f"Template video not found: {template_path}"
            raise FileNotFoundError(msg)

        # Load video and audio
        video = VideoFileClip(str(template_path)).without_audio()
        audio = AudioFileClip(str(audio_path))

        # Calculate duration
        duration = min(video.duration, audio.duration)

        # Prepare video clip
        video = video.subclipped(0, duration).with_audio(audio)

        # Create caption
        caption = (
            TextClip(
                text=title,
                font="Arial.ttf",
                font_size=50,
                color="white",
            )
            .with_duration(duration)
            .with_position(("center", "center"))
        )

        final = CompositeVideoClip([video, caption])

        if output_filename is None:
            output_filename = f"{userid}_video_{uuid.uuid4().hex}.mp4"

        output_path = self.outputs_dir / output_filename

        final.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            fps=30,
        )

        audio_path.unlink()

        return output_path

    def get_video_url(self, video_path: Path) -> str:
        """Get the URL for serving the video."""
        # This would be used with your FastAPI static file serving
        relative_path = video_path.relative_to(self.project_root)
        return f"/assets/outputs/{relative_path.name}"

    def cleanup_old_videos(self, max_age_hours: int = 24) -> None:
        """Clean up old generated videos."""

        current_time = time.time()
        max_age_seconds = max_age_hours * 3600

        for video_file in self.outputs_dir.glob("*.mp4"):
            if current_time - video_file.stat().st_mtime > max_age_seconds:
                video_file.unlink()

    async def create_text(self, fileid: str, userid: int) -> str:
        # use openai Client to summarize a google drive video
        result = await GoogleDriveService.read_file(userid, fileid)
        # Handle both dict and object styles safely
        if isinstance(result, dict):
            extracted_text = result.get("content", "")
        else:
            extracted_text = getattr(result, "content", str(result))

        if not isinstance(extracted_text, str):
            extracted_text = str(extracted_text)
        try:
            response = self.openAiClient.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "First grasp the content of the google doc that was provided in the user content"
                            "You are an AI tutor who creates short, engaging educational scripts for Instagram Reels-style videos. "
                            "Your task is to summarize the user's Google Doc content into a spoken dialogue script — no narration instructions or scene descriptions, only the spoken text itself. "
                            "The tone should be friendly, concise, and helpful, like a teacher explaining something interesting and easy to understand. "
                            "Keep the dialogue under 30 seconds of speech (aim for less than 70 words). "
                            "Make sure it flows naturally when read aloud, as the text will be converted directly into an AI voiceover. "
                            "If the topic is technical, use simple analogies or examples to make it relatable."
                        ),
                    },
                    {"role": "user", "content": extracted_text},
                ],
            )
            generated_text = response.choices[0].message.content
        except Exception as e:  # noqa: BLE001
            generated_text = f"Error {e}"
        return generated_text
