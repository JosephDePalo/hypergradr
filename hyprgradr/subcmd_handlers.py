from .submission import Submission


def download_submission(args):
    api_token = open(args.tokenfile).read().strip()
    submission = Submission(args.courseid, args.assignmentid, args.studentid, api_token)
    print(args)
    submission.get_student_submissions()
