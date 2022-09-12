from __future__ import annotations

from twitchio.ext import commands
import cv2


class VideoCog(commands.Cog):
    # TODO: This should be the class that creates commands based on the entries in videos.yml


    def __init__(self, media_token):
        # Poplate video commands
        self.generate_command(media_token)
        pass
    
    @classmethod
    def generate_command(cls, media_token):
        # This creates the commands themselves
        pass

    async def play_video(self, video_url: str | Path):
        # Play videos using openCV
        pass
    
    async def play_sound(self, sound_url: str | Path):
        # Play sounds using openCV or VLC or other?
        pass
    