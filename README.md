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

## Usage

```bash
  poetry run python -m hyprgradr --config config.toml -s "Doe, John" update \
    -C \ # Enter a comment interactively. Terminate with Ctrl+D.
    -G \ # Enter a grade interactively.
    -f "report1.txt" \ # Specify a file to be uploaded.
    -f "report2.txt"
```
