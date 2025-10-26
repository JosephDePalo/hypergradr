import os
import mimetypes
from datetime import datetime, timedelta
from pathlib import Path

import requests

BASE_URL = "https://sit.instructure.com"
EB_DAYS = 2


class Submission:
    def __init__(self, course_id, assignment_id, student_id, api_token) -> None:
        self.course_id = course_id
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def upload_file_for_student(self, file_path):
        # Initiate upload
        init_url = (
            f"{BASE_URL}/api/v1/courses/{self.course_id}/assignments/"
            f"{self.assignment_id}/submissions/{self.student_id}/comments/files"
        )

        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        init_data = {
            "name": file_name,
            "size": file_size,
            "content_type": mimetypes.guess_type(file_path)[0],
        }

        init_resp = requests.post(init_url, headers=self.headers, data=init_data)
        init_resp.raise_for_status()
        init_info = init_resp.json()

        upload_url = init_info["upload_url"]
        upload_params = init_info["upload_params"]

        # Upload file to upload_url
        with open(file_path, "rb") as f:
            upload_files = {"file": (file_name, f)}
            upload_resp = requests.post(
                upload_url, data=upload_params, files=upload_files
            )

        if upload_resp.status_code in (301, 302):
            confirm_url = upload_resp.headers["location"]
        elif upload_resp.status_code == 201:
            confirm_url = upload_resp.json().get("location")
        else:
            confirm_url = upload_resp.url

        # Get file ID
        confirm_resp = requests.post(confirm_url, headers=self.headers)
        confirm_resp.raise_for_status()
        file_info = confirm_resp.json()
        file_id = file_info["id"]

        return file_id

    def update_submission(self, text, file_ids, grade):
        comment_url = (
            f"{BASE_URL}/api/v1/courses/{self.course_id}/assignments/"
            f"{self.assignment_id}/submissions/{self.student_id}"
        )
        comment_data = {
            "comment[text_comment]": text,
            "comment[file_ids][]": file_ids,
            "submission[posted_grade]": grade,
        }

        comment_resp = requests.put(
            comment_url, headers=self.headers, data=comment_data
        )
        comment_resp.raise_for_status()

    def get_student_submissions(self):
        submission_url = f"{BASE_URL}/api/v1/courses/{self.course_id}/assignments/{self.assignment_id}/submissions/{self.student_id}"
        resp = requests.get(submission_url, headers=self.headers)
        resp.raise_for_status()
        submission = resp.json()

        attachments = submission.get("attachments", [])
        submission_dir_path = Path(f"./{self.student_id}")
        if attachments:
            submission_dir_path.mkdir()
        for att in attachments:
            file_name = att["filename"]
            file_url = att["url"]
            print(f"Downloading {file_name}...")

            file_resp = requests.get(file_url, headers=self.headers)
            file_resp.raise_for_status()

            with open(submission_dir_path / file_name, "wb") as f:
                f.write(file_resp.content)

    def has_eb(self, days_before_deadline=EB_DAYS):
        submission_url = f"{BASE_URL}/api/v1/courses/{self.course_id}/assignments/{self.assignment_id}/submissions/{self.student_id}"
        resp = requests.get(submission_url, headers=self.headers)
        resp.raise_for_status()
        submission = resp.json()

        submitted_at = submission.get("submitted_at")
        submitted_dt = datetime.fromisoformat(submitted_at.replace("Z", "+00:00"))

        assignment_url = f"{BASE_URL}/api/v1/courses/{self.course_id}/assignments/{self.assignment_id}"
        resp = requests.get(assignment_url, headers=self.headers)
        resp.raise_for_status()
        assignment = resp.json()

        due_at = assignment.get("due_at")
        due_dt = datetime.fromisoformat(due_at.replace("Z", "+00:00"))

        time_diff = due_dt - submitted_dt

        return time_diff > timedelta(days=days_before_deadline)
