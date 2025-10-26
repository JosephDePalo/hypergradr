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

    grade = args.grade
    if args.interactive_grade:
        grade = float(input("Input the base grade: "))
    if submission.has_eb():
        grade *= kwargs["config"].eb_mult
        print("EB applied")

    file_ids = []
    if args.file:
        for file in args.file:
            print(f"Uploaded {file}")
            file_ids.append(submission.upload_file_for_student(file))

    comment = args.comment
    if args.interactive_comment:
        print("--- BEGIN COMMENT ---")
        comment = sys.stdin.read()
        print("--- END COMMENT ---")

    submission.update_submission(comment, file_ids, grade)
    print("Submission updated")
