from __future__ import annotations
from pathlib import Path

import pyglet

from handler import gather


def load_media(media_kwargs):
    media = dict()

    for i, (name, attributes) in enumerate(media_kwargs.items()):
        names = [name]
        if "alias" in attributes:
            names.extend(attributes["alias"])
        location = Path(attributes["location"]).expanduser()

        # This is kind of dumb but OK
        for n in names:
            media[n] = location

    return media


def play_sound(url: os.PathLike | Path):
    
    if not Path(url).exists():
        return

    print(f"Playing {url}")

    media = pyglet.media.load(url)
    media.play()
    pyglet.app.run()


if __name__ == "__main__":
    configurations = dict(MEDIACONF="media")

    media = gather(**configurations)["media"]

    for m in set(load_media(media).values()):
        print(m)
        play_sound(m)
