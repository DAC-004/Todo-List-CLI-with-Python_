# Todo List CLI in Python

A lightweight command-line task tracker for a small logistics company's internal operations team. Coordinators use it to manage pending follow-ups between shifts. Tasks are kept in memory during a session and can be saved to a local CSV file and reloaded later.

## Source references

This project follows three source files in `docs/`:

- **`Challenge.txt`** — business context and functional brief
- **`need.png`** — implementation checklist and standard-library-only constraint
- **`evaluate.png`** — evaluator rubric and required function behavior

## Features

- Add task
- List tasks with numeric positions
- Delete task by position
- Save to `todos.csv`
- Load from `todos.csv`

## Out of scope

- No task editing or update-in-place (delete and recreate instead)

## How to run

```bash
python todo.py
```

## How to test

```bash
python -m py_compile todo.py test_todo.py
python -m unittest -v
```

## CSV format

```csv
title
Example task
```

## Dependencies

No external packages are required. The app uses only the Python standard library.
