import discord

from constants import *
from strings import title, content
from utility import update_status, sleep_like_human, get_tagids_by_forum
from toast_notification import show_toast
from gpt import check_job_post

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

        # @self.client.event
        # async def on_message(message: discord.Message):
        #     if message.author.id != self.client.user.id: # type: ignore
        #         await self._handle_message(message)

        # @self.client.event
        # async def on_thread_create(thread: discord.Thread):
        #     if isinstance(thread.parent, discord.ForumChannel):
        #         update_status(f"New forum post detected!")

        #         # Fetch the first message in the thread
        #         try:
        #             first_message = await thread.fetch_message(thread.id)  # The first message ID = thread ID
        #             if first_message.author.id == self.client.user.id:
        #                 update_status("Post author is self. Ignoring.")
        #                 return
        #         except Exception as e:
        #             update_status(f"Failed to fetch first message: {e}", "error")
        #             return

        #         channel_name = thread.parent.name  # Forum name
        #         title = thread.name  # Thread title
        #         content = first_message.content  # Thread first message content
        #         url = first_message.jump_url

        #         if check_job_post(content):
        #             await send_message_to_tg(f"{title}\n{content}\n{url}")
        #             show_toast(
        #                 title=title,
        #                 message=f"{channel_name}\n{content[0:30]}{'...' if len(content) > 30 else ''}",
        #                 position="top-center",
        #                 toast_type="info",
        #                 url=url
        #             )

    def _is_good_for_me(self, message: discord.Message) -> bool:

        if self.client.user in message.mentions:
            return True

        if self.client.user.name.lower() in message.content.lower(): # type: ignore
            return True
        
        return check_job_post(message.content)

    async def _handle_message(self, message: discord.Message):        
        if isinstance(message.channel, discord.Thread):
            thread = message.channel

            if thread.id in self.active_threads:
                if isinstance(thread.parent, discord.ForumChannel):
                    forum_name = thread.parent.name
                    thread_title = thread.name
                    content = message.content

                    await send_message_to_tg(f"{content}\n{message.jump_url}")
                    show_toast(
                        title=f"New reply in {thread_title}",
                        message=f"{forum_name}\n{content[0:30]}{'...' if len(content) > 30 else ''}",
                        position="top-center",
                        toast_type="info",
                        url=message.jump_url
                    )
                    return

        if self._is_good_for_me(message):
            update_status(f"Job Message - ```{message.content[:30]}{'...' if len(message.content) > 30 else ''}```\n{message.jump_url}\n")
            await send_message_to_tg(f"{message.content}\n{message.jump_url}")
            show_toast(
                title="New Message!",
                message=message.content[:30] + ("..." if len(message.content) > 30 else ""),
                position="top-center",
                toast_type="info",
                url=message.jump_url
            )

    async def _schedule_manage(self):
        await self.client.wait_until_ready()

        while not self.client.is_closed():
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

    async def _scheduled_chat_post(self, channel):
        if channel:
            try:
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
