from twitchio.ext import commands
import cv2

from pathlib import Path
from typing import Union
import logging


class VideoCog(commands.Cog):
    # TODO: This should be the class that creates commands based on the entries in videos.yml

    def __init__(self, bot):
        # Poplate video commands
        self.bot = bot

    @commands.Cog.event()
    async def event_message(self, message):
        if message.echo:
            return
        logging.info(f"{__file__} is loaded!")
    
    @commands.command()
    async def lmgtfy(self, ctx, *search):
	    await ctx.send(f"https://lmgtfy.app/?s=d&q={'+'.join(search)}")

    @commands.command(aliases=("ddg",))
    async def duck(self, ctx, *search):
	    await ctx.send(f"https://duckduckgo.com/?q={'+'.join(search)}")

    @commands.command()
    async def play_video(self, video_url: Union[str, Path]):
        # Play videos using openCV
        pass
    
    @commands.command()
    async def play_sound(self, sound_url: Union[str, Path]):
        # Play sounds using openCV or VLC or other?
        pass
    
def prepare(bot: commands.Bot):
    bot.add_cog(VideoCog(bot))
    