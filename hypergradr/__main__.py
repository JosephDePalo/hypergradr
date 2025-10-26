import argparse
from pathlib import Path
import json


from pydantic import ValidationError
import requests

from . import subcmd_handlers as hndl
from .appconfig import AppConfig


def build_parser():
    parser = argparse.ArgumentParser(
        description="A CLI utility for interacting with the Canvas LMS API.1"
    )
    parser.add_argument("--config", required=True)
    parser.add_argument("-s", "--student-name")

    subparsers = parser.add_subparsers(dest="command", required=True)

    download_parser = subparsers.add_parser(
        "download", help="Download student submissions"
    )
    download_parser.set_defaults(func=hndl.download_submission)

    update_parser = subparsers.add_parser(
        "update", help="Update a student's submission details"
    )
    update_parser.add_argument("-g", "--grade", type=float)
    update_parser.add_argument("-G", "--interactive-grade", action="store_true")
    update_parser.add_argument("-c", "--comment")
    update_parser.add_argument(
        "-C", "--interactive-comment", action="store_true"
    )
    update_parser.add_argument("-f", "--file", action="append")
    update_parser.set_defaults(func=hndl.update_submission)

    return parser


def get_all_students(config):
    api_token = open(config.token_file, "r").read().strip()
    url = f"{config.base_url}/api/v1/courses/{config.course_id}/enrollments"
    params = {"type[]": "StudentEnrollment", "per_page": 1000}
    headers = {"Authorization": f"Bearer {api_token}"}

    students = []
    next_url = url
    while next_url:
        resp = requests.get(next_url, headers=headers, params=params)
        resp.raise_for_status()
        students.extend(resp.json())

        next_url = resp.links.get("next", {}).get("url")

    return {s["user"]["sortable_name"]: s["user"]["id"] for s in students}


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        config = AppConfig.from_args(args)
    except (ValidationError, ValueError) as e:
        parser.error(f"Configuration error:\n{e}")

    cache_path = Path(config.cache_path)
    if cache_path.exists():
        with open(cache_path, "r") as f:
            students = json.load(f)
    else:
        students = get_all_students(config)
        with open(cache_path, "w") as f:
            json.dump(students, f)

    args.func(args=args, config=config, students=students)


if __name__ == "__main__":
    main()
