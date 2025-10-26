import argparse

# from hyprgradr import subcmd_handlers as hndl
from . import subcmd_handlers as hndl


def build_parser():
    parser = argparse.ArgumentParser(
        description="A CLI utility for interacting with the Canvas LMS API.1"
    )
    parser.add_argument("-c", "--courseid", required=True)
    parser.add_argument("-a", "--assignmentid", required=True)
    parser.add_argument("-t", "--tokenfile", required=True)
    student_group = parser.add_mutually_exclusive_group(required=True)
    student_group.add_argument("-s", "--studentid")
    student_group.add_argument("-n", "--studentname")

    subparsers = parser.add_subparsers(dest="command", required=True)

    download_parser = subparsers.add_parser(
        "download", help="Download student submissions"
    )
    download_parser.set_defaults(func=hndl.download_submission)

    return parser


def main():
    args = build_parser().parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
