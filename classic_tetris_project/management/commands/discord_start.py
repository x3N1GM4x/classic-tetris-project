from django.core.management.base import BaseCommand, CommandError
from asgiref.sync import sync_to_async
import discord
from ...env import env
from ...commands.command_context import DiscordCommandContext

"""
The discord.py library uses asyncio coroutines for all event handlers and blocking API calls. That's
nice, but for now we don't want that to leak into the rest of our application, where blocking
synchronous functions (e.g. Django's ORM operations) will interfere with the event loop.

Instead, we've decided to write our application synchronously. This involves dispatching events in a
new thread and re-entering the event loop when calling async discord.py functions.

Some useful background on this approach is discussed in this article:
https://www.aeracode.org/2018/02/19/python-async-simplified/
"""
class Command(BaseCommand):
    def handle(self, *args, **options):
        client = discord.Client()

        @client.event
        async def on_message(message):
            if DiscordCommandContext.is_command(message.content):
                context = DiscordCommandContext(message)
                await sync_to_async(context.dispatch)()

        client.run(env("DISCORD_TOKEN"))

