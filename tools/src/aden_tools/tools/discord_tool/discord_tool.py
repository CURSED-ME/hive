"""
Discord Tool - Interact with Discord servers via bot API.

Supports:
- Sending messages to channels
- Reading channel history
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import httpx
from fastmcp import FastMCP

if TYPE_CHECKING:
    from aden_tools.credentials import CredentialStoreAdapter

DISCORD_API_BASE = "https://discord.com/api/v10"


def register_tools(
    mcp: FastMCP,
    credentials: CredentialStoreAdapter | None = None,
) -> None:
    """Register Discord tools with the MCP server."""

    def _get_token() -> str | None:
        """Get Discord bot token from credential manager or environment."""
        if credentials is not None:
            token = credentials.get("discord")
            if token is not None and not isinstance(token, str):
                raise TypeError(
                    f"Expected string from credentials.get('discord'), got {type(token).__name__}"
                )
            return token
        return os.getenv("DISCORD_BOT_TOKEN")

    def _get_headers() -> dict[str, str] | dict[str, str]:
        """Get headers for Discord API requests."""
        token = _get_token()
        if not token:
            return {
                "error": "Discord credentials not configured",
                "help": "Set DISCORD_BOT_TOKEN environment variable",
            }
        return {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": "Aden/1.0",
        }

    def _handle_response(response: httpx.Response) -> dict[str, Any]:
        """Handle Discord API response."""
        if response.status_code == 401:
            return {"error": "Invalid Discord bot token"}
        if response.status_code == 403:
            return {"error": "Forbidden - Bot lacks permissions or is not in the server"}
        if response.status_code == 404:
            return {"error": "Resource not found (check channel ID)"}
        if response.status_code == 429:
            return {"error": "Rate limited by Discord API"}

        try:
            data = response.json()
        except Exception:
            data = {}

        if response.status_code >= 400:
            return {"error": f"Discord API error (HTTP {response.status_code}): {data}"}

        return {"success": True, "data": data}

    @mcp.tool()
    def discord_send_message(
        channel_id: str,
        content: str,
    ) -> dict:
        """
        Send a message to a Discord channel.

        Args:
            channel_id: The ID of the channel to send the message to
            content: The message content (text)

        Returns:
            Dict with message details or error
        """
        if not content:
            return {"error": "Message content cannot be empty"}

        headers = _get_headers()
        if "error" in headers:
            return headers

        try:
            response = httpx.post(
                f"{DISCORD_API_BASE}/channels/{channel_id}/messages",
                headers=headers,  # type: ignore
                json={"content": content},
                timeout=30.0,
            )
            return _handle_response(response)
        except httpx.TimeoutException:
            return {"error": "Request timed out"}
        except httpx.RequestError as e:
            return {"error": f"Network error: {str(e)}"}

    @mcp.tool()
    def discord_read_history(
        channel_id: str,
        limit: int = 50,
    ) -> dict:
        """
        Read message history from a Discord channel.

        Args:
            channel_id: The ID of the channel to read from
            limit: Maximum number of messages to return (1-100, default 50)

        Returns:
            Dict with list of messages or error
        """
        headers = _get_headers()
        if "error" in headers:
            return headers

        limit = max(1, min(100, limit))

        try:
            response = httpx.get(
                f"{DISCORD_API_BASE}/channels/{channel_id}/messages",
                headers=headers,  # type: ignore
                params={"limit": limit},
                timeout=30.0,
            )
            return _handle_response(response)
        except httpx.TimeoutException:
            return {"error": "Request timed out"}
        except httpx.RequestError as e:
            return {"error": f"Network error: {str(e)}"}
