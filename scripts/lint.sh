#!/bin/bash

export MYPYPATH="$(cd "$(dirname "$0")/../username_checker/stubs" && pwd)"

poetry run ruff check .
poetry run mypy . --exclude username_checker/stubs