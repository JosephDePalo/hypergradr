from .submission import Submission


def download_submission(args, config):
    api_token = open(config.token_file).read().strip()
    submission = Submission(
        config.course_id, config.assignment_id, args.student_id, api_token
    )
    submission.get_student_submissions()
