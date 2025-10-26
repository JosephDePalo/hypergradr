import sys

from .submission import Submission


def download_submission(**kwargs):
    student_name = kwargs["args"].student_name
    student_id = kwargs["students"][student_name]
    submission = Submission(kwargs["config"], student_id, student_name)
    submission.get_student_submissions()
    if submission.has_eb():
        print("Student has EB!")


def update_submission(**kwargs):
    args = kwargs["args"]
    student_name = args.student_name
    student_id = kwargs["students"][student_name]
    submission = Submission(kwargs["config"], student_id, student_name)

    comment = args.comment
    if args.interactive_comment:
        print("--- BEGIN COMMENT ---")
        comment = sys.stdin.read()
        print("--- END COMMENT ---")

    file_id = None
    if args.file:
        print(f"Uploaded {args.file}")
        file_id = submission.upload_file_for_student(args.file)

    grade = args.grade
    try:
        if submission.has_eb():
            grade *= kwargs["config"].eb_mult
            print("EB applied")
    except Exception as _:
        pass

    submission.update_submission(comment, file_id, grade)
    print("Submission updated")
