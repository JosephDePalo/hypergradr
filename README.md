# hypergradr

A CLI utility for interacting with the Canvas LMS API.

## Features

- Automatically download all of a student's submissions.
- Auto calculate EB credit
- Interactively enter grades and comments
- Enter grades, comments, and files as command arguments
- Quickly grade a list of people with `grade_people.sh`
- Cache student names for quicker submission downloads

## Setup

In order to run this project you will need the [poetry](https://python-poetry.org/)
dependency management system.

```bash
git clone https://github.com/JosephDePalo/hypergradr
cd hypergradr
mkdir .secrets
chmod 700 .secrets
vim .secrets/canvas_api_token # Store API token in a protected file.
poetry install
vim config.toml # Define the configurations for the project.
poetry env activate
```

### Getting a Canvas API Token

Navigate to `Account>Settings` and scroll down to `Approved Integrations`.
Click on `New Access Token`, give it a name, and copy the token to a protected
file.

## config.toml Format

`course_id` and `assignment_id` for a specific assignment can be retrieved from
the URl of the assignment's page.

```toml
course_id = "12345"
assignment_id = "123456"
token_file = ".secrets/canvas_api_token"
base_url = "https://myschool.instructure.com"
eb_days = 2
eb_mult = 1.02
eb_due_date = "2025-10-23T03:59:59Z" # UTC
cache_path = ".students.cache"
```

## Usage

### Downloading Submissions

```bash
poetry run python -m hypergradr --config config.toml -s "Doe, John" download
```

### Updating Submissions

Interactively enter grades and comments:

```bash
  poetry run python -m hypergradr --config config.toml -s "Doe, John" update \
    -C \ # Enter a comment interactively. Terminate with Ctrl+D.
    -G \ # Enter a grade interactively.
    -f "report1.txt" \ # Specify a file to be uploaded.
    -f "report2.txt"
```

Provide comments and grades as an argument:

```bash
  poetry run python -m hypergradr --config config.toml -s "Doe, John" update \
    -f "report1.txt" \ # Specify a file to be uploaded.
    -g 72.4 \
    -c "$(cat <<EOF
    This is my multi-line comment.
    It is very cool.
    EOF")

```

### `grade_people.sh`

Create a file with the sortable names of students:

```text
Smith, John
Shmoe, Joe
Doe, Jane
```

Modify the arguments within the loop as needed. The `namecode` variable
contains a squashed version of each name (e.g. `Smith, John -> smithjohn`).

```bash
bash grade_people.sh names.txt
```
