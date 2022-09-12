import click
import yaml
import os

from pathlib import Path


DATA = Path(__file__).parent.joinpath("data")

def gather(**kwargs):
    tokens = dict()

    for key, arg in kwargs.items():

        conf_file = os.getenv(key, DATA.joinpath(f"{arg}.yml"))

        try:
            with Path(conf_file).open() as f:
                conf = yaml.safe_load(f)
        except FileNotFoundError():
            raise

        tokens[arg] = conf

    print(tokens)

    return tokens
