import argparse
import tomllib

from pydantic import BaseModel, FilePath
from typing import Optional

from . import subcmd_handlers as hndl


def build_parser():
    parser = argparse.ArgumentParser(
        description="A CLI utility for interacting with the Canvas LMS API.1"
    )
    parser.add_argument("--config", required=True)
    student_group = parser.add_mutually_exclusive_group(required=True)
    student_group.add_argument("-s", "--student-id")
    student_group.add_argument("-n", "--student-name")

    subparsers = parser.add_subparsers(dest="command", required=True)

    download_parser = subparsers.add_parser(
        "download", help="Download student submissions"
    )
    download_parser.set_defaults(func=hndl.download_submission)

    return parser


class Config(BaseModel):
    course_id: int
    assignment_id: int
    token_file: FilePath
    eb_days: int
    base_url: str

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "Config":
        config = {}
        if args.config:
            with open(args.config, "rb") as f:
                config = tomllib.load(f)

        return cls(**config)


def main():
    args = build_parser().parse_args()
    config = Config.from_args(args)

    args.func(args, config)


if __name__ == "__main__":
    main()
