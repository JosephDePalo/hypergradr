# hypergradr

A CLI utility for interacting with the Canvas LMS API.

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

## config.toml Format
```toml
course_id = "12345"
assignment_id = "123456"
token_file = ".secrets/canvas_api_token"
eb_days = 2
base_url = "https://myschool.instructure.com"
eb_mult = 1.02
cache_path = ".students.cache"
eb_due_date = "2025-10-23T03:59:59Z" # UTC
```

## Usage

```bash
  poetry run python -m hyprgradr --config config.toml -s "Doe, John" update \
    -C \ # Enter a comment interactively. Terminate with Ctrl+D.
    -G \ # Enter a grade interactively.
    -f "report1.txt" \ # Specify a file to be uploaded.
    -f "report2.txt"
```
