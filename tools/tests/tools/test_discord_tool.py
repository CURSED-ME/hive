"""Tests for Discord tool."""

import httpx
import pytest
from fastmcp import FastMCP

from aden_tools.tools.discord_tool import register_tools


class DummyResponse:
    """Simple mock response for httpx."""

    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict:
        return self._payload


@pytest.fixture
def discord_tools(mcp: FastMCP):
    """Register and return the discord tool functions."""
    register_tools(mcp)
    return mcp._tool_manager._tools


class TestDiscordSendMessage:
    """Tests for discord_send_message tool."""

    def test_send_message_success(self, discord_tools, monkeypatch):
        """Send message successfully."""
        monkeypatch.setenv("DISCORD_BOT_TOKEN", "test-token")

        captured: dict = {}

        def mock_post(url: str, headers=None, json=None, timeout=30.0):
            captured["url"] = url
            captured["headers"] = headers
            captured["json"] = json
            return DummyResponse(
                200,
                {
                    "id": "12345",
                    "channel_id": "98765",
                    "content": "Hello",
                },
            )

        monkeypatch.setattr(httpx, "post", mock_post)

        result = discord_tools["discord_send_message"].fn(
            channel_id="98765", content="Hello"
        )

        assert result["success"] is True
        assert result["data"]["id"] == "12345"
        assert captured["url"] == "https://discord.com/api/v10/channels/98765/messages"
        assert captured["headers"]["Authorization"] == "Bot test-token"
        assert captured["json"]["content"] == "Hello"

    def test_send_message_empty_content(self, discord_tools, monkeypatch):
        """Error on empty content."""
        monkeypatch.setenv("DISCORD_BOT_TOKEN", "test-token")
        result = discord_tools["discord_send_message"].fn(channel_id="123", content="")
        assert "error" in result
        assert "content cannot be empty" in result["error"]

    def test_send_message_401(self, discord_tools, monkeypatch):
        """Error on invalid token."""
        monkeypatch.setenv("DISCORD_BOT_TOKEN", "invalid-token")

        def mock_post(url, **kwargs):
            return DummyResponse(401, {"message": "401: Unauthorized"})

        monkeypatch.setattr(httpx, "post", mock_post)

        result = discord_tools["discord_send_message"].fn(
            channel_id="123", content="Hi"
        )
        assert "error" in result
        assert "Invalid Discord bot token" in result["error"]


class TestDiscordReadHistory:
    """Tests for discord_read_history tool."""

    def test_read_history_success(self, discord_tools, monkeypatch):
        """Read history successfully."""
        monkeypatch.setenv("DISCORD_BOT_TOKEN", "test-token")

        captured: dict = {}

        def mock_get(url: str, headers=None, params=None, timeout=30.0):
            captured["url"] = url
            captured["params"] = params
            return DummyResponse(
                200,
                [
                    {"id": "1", "content": "Msg 1"},
                    {"id": "2", "content": "Msg 2"},
                ],
            )

        monkeypatch.setattr(httpx, "get", mock_get)

        result = discord_tools["discord_read_history"].fn(
            channel_id="98765", limit=5
        )

        assert result["success"] is True
        assert len(result["data"]) == 2
        assert captured["url"] == "https://discord.com/api/v10/channels/98765/messages"
        assert captured["params"]["limit"] == 5

    def test_read_history_403(self, discord_tools, monkeypatch):
        """Error on forbidden access."""
        monkeypatch.setenv("DISCORD_BOT_TOKEN", "test-token")

        def mock_get(url, **kwargs):
            return DummyResponse(403, {"message": "Missing Access"})

        monkeypatch.setattr(httpx, "get", mock_get)

        result = discord_tools["discord_read_history"].fn(channel_id="123")
        assert "error" in result
        assert "Forbidden" in result["error"]
