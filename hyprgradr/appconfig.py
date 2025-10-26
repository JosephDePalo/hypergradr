import tomllib
import argparse

from pydantic import BaseModel, FilePath, ValidationError


class AppConfig(BaseModel):
    course_id: int
    assignment_id: int
    token_file: FilePath
    eb_days: int
    base_url: str
    eb_mult: float
    cache_path: FilePath

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "AppConfig":
        config = {}
        if args.config:
            with open(args.config, "rb") as f:
                config = tomllib.load(f)

        return cls(**config)
