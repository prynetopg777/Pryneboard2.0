"""
youtube_server.py

MCP server exposing YouTube video analysis tools (transcript and comments).
"""

import asyncio
import os
import sys
import json
from pathlib import Path

# Add odysseus(Pryne) to sys.path so we can import services.youtube
sys.path.append(os.path.join(os.getcwd()))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from services.youtube.youtube_handler import (
    is_youtube_url, extract_youtube_id, extract_transcript_async,
    fetch_youtube_comments, format_transcript_for_context, format_comments_for_context,
    YOUTUBE_INSTRUCTION_PROMPT, init_youtube
)

server = Server("youtube")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="analyze_youtube_video",
            description="Extract transcript, fetch comments, and provide a structured summary of a YouTube video URL.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The full YouTube video URL (e.g., https://www.youtube.com/watch?v=...)"
                    }
                },
                "required": ["url"],
            },
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name != "analyze_youtube_video":
        raise ValueError(f"Unknown tool: {name}")

    url = arguments.get("url", "").strip()
    if not url:
        return [TextContent(type="text", text="Error: YouTube URL is required.")]

    if not is_youtube_url(url):
        return [TextContent(type="text", text=f"Error: Invalid YouTube URL: {url}")]

    video_id = extract_youtube_id(url)
    if not video_id:
        return [TextContent(type="text", text=f"Error: Could not extract video ID from URL: {url}")]

    # Ensure initialized
    init_youtube()

    # Fetch transcript and comments in parallel
    transcript_task = extract_transcript_async(url, video_id)
    comments_task = fetch_youtube_comments(video_id)
    
    transcript_data, comments_data = await asyncio.gather(
        transcript_task, comments_task
    )

    title = comments_data.get("title", "")
    channel = comments_data.get("channel", "")

    transcript_ctx = format_transcript_for_context(transcript_data, url, title, channel)
    comments_ctx = format_comments_for_context(comments_data, url)

    full_context = f"{YOUTUBE_INSTRUCTION_PROMPT}\n\n{transcript_ctx}\n\n{comments_ctx}"

    result = {
        "success": True,
        "title": title,
        "channel": channel,
        "video_id": video_id,
        "transcript_available": transcript_data.get("success", False),
        "comments_available": comments_data.get("success", False),
        "data": full_context
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]

async def run():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(run())
