"""Discord credentials."""

from .base import CredentialSpec

DISCORD_CREDENTIALS = {
    "discord": CredentialSpec(
        env_var="DISCORD_BOT_TOKEN",
        tools=[
            "discord_send_message",
            "discord_read_history",
        ],
        required=True,
        help_url="https://discord.com/developers/applications",
        description="Bot Token for Discord API",
        credential_id="discord",
        credential_key="bot_token",
    ),
}
