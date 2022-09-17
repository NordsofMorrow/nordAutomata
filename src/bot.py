from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import loguru
import pydantic
from twitchio.ext import commands, routines

from configs import gather


logging.basicConfig(level="INFO")


class Bot(commands.Bot):

    token: str
    prefix = "?"
    channels = []
    nick = ""
    persist = False
    be_loud = True

    def __init__(self, configurations: dict | None = None):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...

        config = gather()["token"]
        self.persist = config["persist"]
        self.nick = config["nick"]

        super().__init__(
            token=config["token"],
            prefix=config["prefix"],
            initial_channels=config["initial_channels"],
        )

        # Add found cogs
        for file in sorted(Path(__file__).parent.joinpath("cogs").iterdir()):
            if file.suffix == ".py":
                self.load_module(f"cogs.{file.stem}")

    async def _channel_send(self, channel, message):
        chan = self.get_channel(channel)
        loop = asyncio.get_event_loop()
        loop.create_task(chan.send(message))

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...

        logging.info(f"Logged in as | {self.nick}")
        logging.info(f"User id is | {self.user_id}")
        if self.nick:
            print(f"{self.nick}Bot is online!")

        await self._channel_send(
            "NordsofMorrow", f"/me (or rather {self.nick}) has landed!"
        )
        print("Let's make some magic!")
        self.hydrate.start("NordsofMorrow")

    @routines.routine(minutes=10)
    async def hydrate(self, channel):
        if not self.hydrate.completed_iterations:
            logging.info(f"hydrate routine started at {self.hydrate.start_time}")
        else:
            msg = "/me should be drinking water!"
            logging.warning(msg.replace("/me", "I"))
            await self._channel_send(channel, msg)

    # @commands.command(aliases=("doit",))
    # async def make_it_happen(self, ctx):

    #     if ctx.name == "NordsofMorrow":
    #         # ctx.send(f"Making it happen!")
    #         super().add_cog(NordoBot())

    @commands.command(aliases=("ohio",))
    async def ohhi(self, ctx, *, user: str = None):
        if not ctx.author.is_mod:
            await ctx.send(f"Hello, {ctx.author.name}!")
        else:
            print(ctx)

            if ctx.name == "NordsofMorrow":
                await ctx.send("Get outta here!")
            elif ctx.author.is_mod:
                await ctx.send(f"Oh hi, {ctx.author.name}!")

    async def event_message(self, message):
        if message.echo:
            return

        print(message.content)

        await self.handle_commands(message)


if __name__ == "__main__":
    bot = Bot()
    bot.run()
    # bot.run() is blocking and will stop execution of any below code here until stopped or closed.
