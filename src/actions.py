from __future__ import annotations

from pathlib import Path

import pyglet

from configs import gather


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
