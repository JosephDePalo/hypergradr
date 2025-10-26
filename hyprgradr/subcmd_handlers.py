import argparse

from .submission import Submission
from .appconfig import AppConfig


def download_submission(**kwargs):
    student_name = kwargs["args"].student_name
    student_id = kwargs["students"][student_name]
    submission = Submission(kwargs["config"], student_id, student_name)
    submission.get_student_submissions()
    if submission.has_eb():
        print("Student has EB!")
