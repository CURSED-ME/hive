# Discord Tool

Interact with Discord servers using a Bot Token.

## Features

- **Send Messages**: Post text messages to specific channels.
- **Read History**: keyRetrieve recent messages from a channel.

## Prerequisites

1. Create a Discord Application at [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a Bot user for the application.
3. Invite the bot to your server using OAuth2 URL generator (scopes: `bot`, permissions: `Send Messages`, `Read Messages`, `View Channels`).
4. Get the **Bot Token** from the Bot page.

## Configuration

Set the environment variable:

```bash
export DISCORD_BOT_TOKEN="your-bot-token-here"
```

## Usage

```python
# Send a message
result = discord_send_message(channel_id="123456789", content="Hello from Aden!")

# Read history
history = discord_read_history(channel_id="123456789", limit=10)
```
