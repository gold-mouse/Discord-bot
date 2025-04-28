# Discord-bot

Auto posting & watch group bot with customized Windows notifications for Discord forums and chats.

---

## Overview

This Discord self-bot automatically posts predefined messages to specified chat and forum channels, monitors new messages and forum posts, and displays Windows toast notifications for relevant updates, such as new job postings. It also uses OpenAI GPT to detect job-related messages and filters messages accordingly.

---

## Features

- Auto posting scheduled messages to multiple chat and forum channels.
- Monitors forum threads and messages for job posts using AI content detection.
- Displays Windows toast notifications for new relevant messages and forum replies.
- Supports filtering and ignoring own posts.
- Configurable delay times between posts.
- Uses Discord API and OpenAI GPT-3.5 Turbo for message classification.

---

## Technologies

- Python 3.8+
- discord.py library
- OpenAI GPT API (GPT-3.5 Turbo)
- colorama for terminal coloring
- Windows toast notifications (via `toast_notification` module)
- dotenv for environment variable management

---

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/gold-mouse/Discord-bot.git
   cd Discord-bot
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your credentials:

   ```env
   DISCORD_AUTH_TOKEN=your_discord_auth_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   MIN_DELAY=60        # minimum delay in minutes between posts
   MAX_DELAY=90        # maximum delay in minutes between posts
   ```

   - **Getting your Discord token:**  
     *Warning:* Using user tokens may violate Discord Terms of Service. Proceed with caution and at your own risk. You can obtain it from your browser’s developer tools after logging into Discord web.
   
   - **Getting your OpenAI API key:**  
     Visit [OpenAI API Keys](https://platform.openai.com/account/api-keys) to create a new key.

5. Prepare channel ID files:

   - `chat_channel_ids.cfg`: List Discord channel IDs for auto posting in chats (one per line).
   - `forum_channel_ids.cfg`: List Discord forum channel IDs for posting in forums (one per line).

---

## Usage

Run the bot with:

```sh
python main.py
```

The bot will:

- Automatically send scheduled posts to the configured chat and forum channels.
- Listen to new messages and threads.
- Show Windows toast notifications for relevant posts mentioning the bot or detected as job posts.
- Use OpenAI GPT to classify if a message is a job-related post.

---

## Configuration

- `title` and `content` variables (in `strings.py`) define the message posted to forums.
- Delay between posts is randomized between `MIN_DELAY` and `MAX_DELAY` minutes.
- Tags applied to forum posts are mapped in `constants.py` (`TAG_ID_BY_FORUM_CHANNEL`).

---

## Important Notes

- This is a **self-bot**: it uses a user token, which is against Discord’s Terms of Service and can result in account termination. Use at your own risk.
- Requires Windows OS for toast notifications.
- Make sure your OpenAI API key has access to GPT-3.5 Turbo.

---

## License

This project is open source. Use and modify as you wish.
