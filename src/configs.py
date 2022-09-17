import click
import yaml
import os
import logging

from pathlib import Path


CONFIGS = dict(TOKENCONF="token", MEDIACONF="media")
DATA = Path(__file__).parent.joinpath("data")


def gather(**kwargs):
    configs = dict()

    if not kwargs:
        kwargs = CONFIGS

    for key, arg in kwargs.items():
        found_file = os.getenv(key, DATA.joinpath(f"{arg}.yml"))

        try:
            with Path(found_file).open() as f:
                conf = yaml.safe_load(f)
        except FileNotFoundError():
            raise

        configs[arg] = conf

    for config in configs:
        logging.info("Gathered {config}.")
    return configs


def load_media(media_kwargs):
    media = dict()
    media["video"] = []
    media["sound"] = []

    for i, (name, attributes) in enumerate(media_kwargs.items()):
        names = [name]
        if "alias" in attributes:
            names.extend(attributes["alias"])
        location = Path(attributes["location"]).expanduser()

        for n in names:
            media[n] = location

    return media
