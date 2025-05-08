# SelfBot for Discord

A Discord self-bot for managing automated promotional posts in chat and forum channels, with Telegram notification support. This bot automatically deletes previous posts before sending new ones and monitors DMs and forum thread replies.

> **Note:** This project is for personal use and educational purposes. Be sure to follow Discord's [Terms of Service](https://discord.com/terms).

---

## Features

* Automated posting in specified chat channels and forum channels
* Deletes previous posts before sending new ones
* Monitors DMs and replies to your forum threads
* Sends real-time notifications via Telegram
* Human-like sleeping behavior between actions

---

## Requirements

* Python 3.10+
* A Discord account with access to the target channels/forums
* Telegram Bot Token and Chat ID for notifications

---

## Setup

1. **Clone this repository:**

```bash
git clone https://github.com/yourusername/selfbot.git
cd selfbot
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Edit the configuration files:**

* `chat_channel_ids.cfg`: Each line should contain a Discord chat channel ID.
* `forum_channel_ids.cfg`: Each line should contain a Discord forum channel ID.

Example `chat_channel_ids.cfg`:

```
123456789012345678
987654321098765432
```

4. **Add .env file:**
```sh
DISCORD_AUTH_TOKEN=YOUR_AUTHORIZATION
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_CHATID
```

5. **Edit promo.txt file** The file has to follow bellow format:

```sh
title
---
content
```

6. **Run the bot:**

```bash
python main.py
```

---

## Notes

* The bot only operates between **05:00 - 22:00 UTC**.
* Any failed channels are removed from the posting loop to avoid repeated errors.
* The bot uses a message cache for lightweight memory management.

---

## License

MIT License

---

## Disclaimer

Using self-bots violates Discord's ToS. This bot is for **educational** and **personal** use only. Use it at your own risk.
