# How to Get a Discord Bot Token

Follow these steps to create a bot and get your token for testing.

## 1. Create Application
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** (top right).
3. Name it (e.g., "HiveBot") and click **Create**.

## 2. Create Bot User
1. In the left menu, click **Bot**.
2. Click **Reset Token** (yes, do it now to see it).
3. **COPY THIS TOKEN NOW**. This is your `DISCORD_BOT_TOKEN`. You won't see it again.
4. Scroll down and disable "Public Bot" (optional, for security).
5. Enable **Message Content Intent** (toggle it ON) -> **Save Changes**.

## 3. Invite Bot to Server
1. In the left menu, click **OAuth2** > **URL Generator**.
2. Under **Scopes**, check `bot`.
3. Under **Bot Permissions**, check:
   - `Send Messages`
   - `Read Messages/View Channels`
   - `Read Message History`
4. Copy the **Generated URL** at the bottom.
5. Paste it in a new browser tab.
6. Select your server and click **Authorize**.

## 4. Get Channel ID
1. Open Discord app/web.
2. Go to **User Settings** > **Advanced**.
3. Enable **Developer Mode**.
4. Right-click the channel you want the bot to use.
5. Click **Copy Channel ID**.

Now you have the **Token** and **Channel ID** to run the test script!
