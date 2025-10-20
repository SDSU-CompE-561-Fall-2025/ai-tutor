import asyncio
import json

from dotenv import load_dotenv
from fastmcp import Client

load_dotenv()
USERID = "1"
client = Client("http://127.0.0.1:8000/mcp")


def mcp_client() -> Client:
    return Client("http://127.0.0.1:8000/mcp")


async def main() -> None:
    async with client:
        # Call gdrive_search
        result = await client.call_tool(
            "gdrive_search",
            {"query": "test", "user_id": USERID},
        )

        raw_text = result.content[0].text  # type: ignore  # noqa: PGH003
        parsed = json.loads(raw_text)
        files = parsed["files"]
        for f in files:
            print("ID:", f["id"])
            print("Name:", f["name"])
            print("Type:", f["mime_type"])
            print("Link:", f["web_view_link"])
            print("-----")

        # call gdrive_read_file -- currently calling with a hardcoded file_id
        output = await client.call_tool(
            "gdrive_read_file",
            {
                "file_id": "1C37Gzd5IQs8E3BmTWRbqUrX2b1Y6tT-EjEJdahpuldg",
                "user_id": USERID,
            },
        )

        raw_text = output.content[0].text  # type: ignore
        parsed = json.loads(raw_text)

        doc_id = parsed["metadata"]["id"]
        doc_name = parsed["metadata"]["name"]
        doc_link = parsed["metadata"]["webViewLink"]
        doc_content = parsed["content"]

        print("Doc ID:", doc_id)
        print("Doc Name:", doc_name)
        print("Doc Link:", doc_link)
        print("Extracted Content:", doc_content)


async def find_all(user_id):
    try:
        async with client:
            result = await client.call_tool(
                "gdrive_search",
                {"query": "", "user_id": user_id},
            )
            return result.content
    except Exception as e:
        print(f"Unexpected: {e}")


async def find_query(user_id, query):
    try:
        async with client:
            result = await client.call_tool(
                "grdive_search",
                {"query": query, "user_id": user_id},
            )
            return result.content
    except Exception as e:
        print(f"Unexpected {e}")


if __name__ == "__main__":
    asyncio.run(main())
