"""
Gemini AI integration with MCP tools for AI tutor responses.
"""

import json

from fastmcp import Client
from google import genai

from app.core.settings import settings

# --- 1️⃣ Create Gemini Client (initialized once per process)
# Uses the Gemini API key from your environment or settings module.
gemini_client = genai.Client(api_key=settings.gemini_key)


# --- 2️⃣ Helper to get a configured MCP Client
def get_mcp_client() -> Client:
    """Return a configured FastMCP client instance."""
    return Client(settings.mcp_server)


# --- Helper function to read files and build file content dict
async def read_course_files(
    file_ids: list,
    user_id: int,
) -> dict:
    """
    Read all files for a course and return a dict of file_id: content.

    Args:
        file_ids: List of Google Drive file IDs
        user_id: User ID for authentication

    Returns:
        dict: Dictionary mapping file_id to file content
    """
    client = get_mcp_client()
    files_content = {}

    async with client:
        for file_id in file_ids:
            try:
                result = await client.call_tool(
                    "gdrive_read_file",
                    {"file_id": file_id, "user_id": user_id},
                )

                raw_text = result.content[0].text  # pyright: ignore[reportAttributeAccessIssue]
                parsed = json.loads(raw_text)
                files_content[file_id] = parsed.get("content", "")

            except Exception as e:  # noqa: BLE001
                files_content[file_id] = f"Error reading file: {e!s}"

    return files_content


# --- 3️⃣ Function that generates AI Tutor responses via Gemini + MCP
async def generate_ai_response_with_mcp(
    message: str,
    chat_history: dict,
    file_list: list,
    user_id: int,
) -> str:
    """
    Uses Gemini and MCP tools to generate AI Tutor responses.

    This function reads all course files and includes their content in the prompt.
    """
    # Read all course files
    files_content = await read_course_files(file_list, user_id)
    file_content_str = "\n\n".join(
        [
            f"File ID: {fid}\nContent:\n{content}"
            for fid, content in files_content.items()
        ],
    )
    system_prompt = (
        "You are a smart, knowledgeable AI tutor assistant. You have access to course materials "
        "that have been provided to you. Use these materials when appropriate to enhance your responses "
        "and provide the best learning experience possible. "
        "Always explain concepts clearly and adapt your teaching style to the student's level of understanding."
    )

    # Build the message for Gemini with file content
    file_content_str = "\n\n".join(
        [
            f"File ID: {fid}\nContent:\n{content}"
            for fid, content in files_content.items()
        ],
    )

    user_message = f"""
Course Materials:
{file_content_str}

Student's question: {message}

Chat history: {chat_history}

Use the course materials above to help answer the student's question.
Respond clearly and educationally, around 100-200 words.
Use Markdown with code blocks for examples."""

    try:
        # Call Gemini model
        response = await gemini_client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {"role": "user", "parts": [{"text": system_prompt}]},
                {"role": "user", "parts": [{"text": user_message}]},
            ],
        )
        if response.text is None:
            return "Gemini broke sorry my friend"
        return response.text  # pyright: ignore[reportReturnType] # noqa: TRY300

    except Exception as e:  # noqa: BLE001
        return f"Failed to generate AI Tutor response: {e!s}"
