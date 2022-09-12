from __future__ import annotations

import asyncio
import logging

from twitchio.ext import commands, routines
import loguru
import pydantic

from handler import gather


class Bot(commands.Bot):

    token: str
    prefix = "?"
    channels = []
    nick = ""
    persist = False
    be_loud = True

    def __init__(self, configurations: dict):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...

        config = gather(**configurations)["tokens"]
        self.persist = config["persist"]
        self.nick = config["nick"]

        super().__init__(
            token=config["token"],
            prefix=config["prefix"],
            initial_channels=config["initial_channels"],
        )

    async def _channel_send(self, channel, message):
        chan = self.get_channel(channel)
        loop = asyncio.get_event_loop()
        loop.create_task(chan.send(message))

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...

        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")
        if self.nick:
            print(f"{self.nick} is online!")

        await self._channel_send(
            "NordsofMorrow", f"/me (or rather {self.nick}) has landed!"
        )
        print("Let's make some magic!")
        self.keep_alive.start("NordsofMorrow")

    @routines.routine(seconds=10)
    async def keep_alive(self, channel):
        msg = "/me is staying alive!"

        logging.warning(msg)
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
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)


if __name__ == "__main__":
    configurations = dict(TWITCHCONF="tokens", VIDEOCONF="videos")

    bot = Bot(configurations)
    bot.run()
    # bot.run() is blocking and will stop execution of any below code here until stopped or closed.
