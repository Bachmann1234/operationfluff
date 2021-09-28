#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
poetry run black --check operation_fluff tests
poetry run isort --check operation_fluff tests
poetry run mypy operation_fluff tests
poetry run pytest tests -v
