from datetime import datetime, time as dtime, timezone
import discord

from constants import *
from utility import get_promo, update_status, sleep_like_human, get_tagids_by_forum

from telegram_bot import send_message_to_tg

class SelfBot:
    def __init__(self, token: str, chat_channel_ids: list[int], forum_channel_ids: list[int]):
        update_status("Initializing self-bot...", "info")
        self.token = token
        self.chat_channel_ids = chat_channel_ids
        self.forum_channel_ids = forum_channel_ids

        # Initialize client
        self.active_threads = set()
        self.client = discord.Client(message_cache_size=1000)
        self._register_events()

    def _register_events(self):
        @self.client.event
        async def on_ready():
            update_status(f"Logged in as ```{self.client.user} (ID: {self.client.user.id})```", "success") # type: ignore
            await send_message_to_tg("Hello, I am ready to work!")
            self.client.loop.create_task(self._schedule_manage())

    async def _schedule_manage(self):
        await self.client.wait_until_ready()

        while not self.client.is_closed():
            now = datetime.now(timezone.utc).time()
            start_time = dtime(5, 0)
            end_time = dtime(22, 0)

            if start_time <= now <= end_time:
                msg_res, forum_res = None, None
                
                if len(self.forum_channel_ids) > 0:
                    for forum_channel_id in self.forum_channel_ids:
                        if not msg_res == False:
                            await sleep_like_human()
                        msg_res = await self._scheduled_forum_post(forum_channel_id)

                if len(self.chat_channel_ids) > 0:
                    channels = [self.client.get_channel(cid) for cid in self.chat_channel_ids]
                    for channel in channels:
                        if channel:
                            if not forum_res == False:
                                await sleep_like_human()
                            await self._scheduled_chat_post(channel)
            else:
                update_status(f"Sleeping from {now.strftime('%H:%M:%S')} to 22:00:00 UTC", "info")
                await sleep_like_human(60, 60, log=False)

    async def _scheduled_chat_post(self, channel):
        if channel:
            try:
                _, content = get_promo()
                msg = await channel.send(content)
                await send_message_to_tg(f"Posted to {channel.name}\n{msg.content}\n{msg.jump_url}")
                update_status("Success to send message", "success")
                return True
            except discord.HTTPException as e:
                self.chat_channel_ids.remove(channel.id)
                update_status(f"Failed to send message to {channel.id}", "error")
                return False

    async def _scheduled_forum_post(self, forum_channel_id):
        forum = self.client.get_channel(forum_channel_id)  # ForumChannel
        if isinstance(forum, discord.ForumChannel):
            try:
                TAG_ID = get_tagids_by_forum(str(forum_channel_id))
                if not TAG_ID:
                    update_status("Failed to forum post - ```Missed Tag Ids```", "warning")
                    return False

                title, content = get_promo()
                
                available_tags = [tag for tag in forum.available_tags if tag.id in TAG_ID]
                thread = await forum.create_thread(
                    name=title,
                    content=content,
                    applied_tags=available_tags
                )
                self.active_threads.add(thread.thread.id)
                await send_message_to_tg(f"Posted to {forum.name}\n{title}\n{content}\n{thread.thread.jump_url}")
                update_status(f"Success to post: {thread.thread.id}", "success")
                return True
            except Exception as e:
                self.forum_channel_ids.remove(forum_channel_id)
                update_status(f"Failed to post forum to ```{forum_channel_id}```", "error")
                return False
        else:
            update_status("Channel is not a forum!", "warning")

    def run(self):
        # Start the bot
        try:
            self.client.run(self.token)
        except KeyboardInterrupt:
            update_status("Detected exit signal. Closing...", "warning")
            try:
                loop = self.client.loop
                loop.run_until_complete(self.close())
            except Exception as e:
                update_status(f"Error during close: {e}", "error")

    async def close(self):
        update_status("Closing self-bot...", "info")
        await self.client.close()


if __name__ == "__main__":
    update_status("Starting self-bot...", "success")

    with open("chat_channel_ids.cfg", "r") as f:
        chat_channel_ids = [int(line.strip()) for line in f.readlines()]
    update_status(f"Loaded {len(chat_channel_ids)} chat channel IDs", "success")

    with open("forum_channel_ids.cfg", "r") as f:
        forum_channel_ids = [int(line.strip()) for line in f.readlines()]
    update_status(f"Loaded {len(forum_channel_ids)} forum channel IDs", "success")

    bot = SelfBot(
        token=DISCORD_AUTH_TOKEN,
        chat_channel_ids=chat_channel_ids,
        forum_channel_ids=forum_channel_ids
    )
    bot.run()
