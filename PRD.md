# PRD.md — Todo List CLI in Python

## 1. Product Summary

Build a lightweight **Python command-line Todo List CLI** for a small logistics company. Operations coordinators currently track pending tasks in chat messages and sticky notes, which causes shift handoff gaps and missed follow-ups. The tool must allow users to add tasks, view pending tasks, delete completed tasks by list position, save tasks locally, and load them again later.

This is a **terminal-only internal tool**. It must be simple, dependable, and easy to test.

---

## 2. Source Materials That Must Drive the Build

Cursor must treat these three source files as the build authority:

| Source file | Purpose in build |
|---|---|
| `Challenge.txt` | Business context, functional brief, required behavior, and out-of-scope rules |
| `need.png` | Implementation checklist: required functions, CLI expectations, standard-library-only constraint |
| `evaluate.png` | Grading/evaluation checklist: exact function behavior, file persistence, and required CLI flow |

The implementation must explicitly satisfy all three sources. Do not build features outside their scope.

---

## 3. Business Context

The user scenario is an internal tools request from a logistics company. Coordinators need a fast terminal workflow to manage pending tasks during daily operations. The first version is intended for testing by the operations team this week.

The tool must help users:

1. Register new tasks as they come in.
2. Review the full pending list at any time.
3. Remove completed tasks by selecting the task’s numeric position.
4. Save tasks to a local CSV file.
5. Reload tasks after closing and reopening the terminal.

---

## 4. Product Goals

### Primary goals

- Provide a working command-line task tracker.
- Keep the active task list in memory during the current run.
- Persist tasks to `todos.csv`.
- Restore tasks from `todos.csv`.
- Use the exact required function names:
  - `add_one_task(title)`
  - `print_list()`
  - `delete_task(number_to_delete)`
  - `save_todos()`
  - `load_todos()`
- Allow users to add as many tasks as needed in one run.
- Keep CLI behavior consistent with the required flow: **create, list, delete, save, load**.

### Quality goals

- Use only Python standard library modules.
- Keep the code easy to read.
- Keep business logic testable without relying on interactive input.
- Include robust automated tests using `unittest`.
- Avoid unhandled exceptions during normal CLI use.

---

## 5. Non-Goals / Out of Scope

The following must not be implemented in this version:

- Task editing or update-in-place.
- User accounts.
- Authentication.
- Cloud sync.
- Database storage.
- Web interface.
- GUI.
- External packages.
- Priority, due date, tags, assignment, or status fields.
- JSON persistence unless only used internally for tests; final app persistence must be `todos.csv`.

Users should delete and recreate a task if they need to change it.

---

## 6. Users

### Primary user

**Operations Coordinator**

- Works in a terminal or Codespaces-like environment.
- Needs to quickly add and remove daily follow-up tasks.
- Needs task positions to be clear so completed tasks can be deleted accurately.
- May close and reopen the terminal during the day.

### Secondary user

**Product Manager / Evaluator**

- Verifies exact required function names and behavior.
- Checks whether `todos.csv` is written in a reusable format.
- Checks whether tasks reload correctly.
- Checks whether the CLI supports the required flow.

---

## 7. Functional Requirements

### FR-1 — Add one task

**Function:** `add_one_task(title)`

**Requirement:**

- Appends one task to the active in-memory list.
- Accepts a task title as input.
- Stores the title as a string.
- Should strip leading/trailing whitespace.
- Should reject an empty title after stripping.

**Acceptance criteria:**

- Calling `add_one_task("Call carrier")` adds `"Call carrier"` to the active list.
- Calling it multiple times appends tasks in the same order.
- Empty or whitespace-only titles do not create blank tasks.

---

### FR-2 — Print task list

**Function:** `print_list()`

**Requirement:**

- Displays all pending tasks in order.
- Each task must have a clear numeric position users can reference.
- Positions must be **1-based**, not 0-based.

**Acceptance criteria:**

Given tasks:

1. `Call carrier`
2. `Confirm pickup`
3. `Send update`

`print_list()` should display positions similar to:

```text
1. Call carrier
2. Confirm pickup
3. Send update
```

If there are no tasks, it should print a clear empty-list message, such as:

```text
No tasks found.
```

---

### FR-3 — Delete task by numeric position

**Function:** `delete_task(number_to_delete)`

**Requirement:**

- Removes one task using the user-facing numeric list position.
- Must delete the intended task.
- Must update the active list correctly after deletion.
- Uses 1-based indexing from the user’s perspective.

**Acceptance criteria:**

Given:

```text
1. Call carrier
2. Confirm pickup
3. Send update
```

Calling `delete_task(2)` removes `Confirm pickup`.

Result:

```text
1. Call carrier
2. Send update
```

Invalid delete positions should not crash the program. They should leave the list unchanged and show a clear message.

---

### FR-4 — Save tasks to CSV

**Function:** `save_todos()`

**Requirement:**

- Writes current tasks to `todos.csv`.
- Uses Python standard library file I/O and the `csv` module.
- Stores tasks in a reusable format.
- Should overwrite the file with the current active task list.

**CSV schema:**

Use a simple header row:

```csv
title
Call carrier
Confirm pickup
Send update
```

**Acceptance criteria:**

- After adding tasks and calling `save_todos()`, `todos.csv` exists.
- Each task appears as one CSV row.
- The file can be read by spreadsheet tools.
- The file can be loaded back by `load_todos()`.

---

### FR-5 — Load tasks from CSV

**Function:** `load_todos()`

**Requirement:**

- Reads tasks from `todos.csv`.
- Reconstructs the active in-memory list.
- Replaces the current active list with the file contents.
- Uses Python standard library file I/O and the `csv` module.

**Acceptance criteria:**

- If `todos.csv` contains saved tasks, calling `load_todos()` restores them in the original order.
- If `todos.csv` does not exist, the app should not crash.
- If `todos.csv` is empty or only has a header, the active list should become empty.

---

### FR-6 — CLI menu flow

**Requirement:**

The app must run from the command line and behave like the required preview flow:

1. Add/create a task.
2. List tasks.
3. Delete task by position.
4. Save tasks.
5. Load tasks.
6. Quit/exit.

The user must be able to add as many tasks as needed in the same run.

**Suggested menu:**

```text
Todo List CLI
1. Add task
2. List tasks
3. Delete task
4. Save tasks
5. Load tasks
6. Quit
Choose an option:
```

**Acceptance criteria:**

- Running `python todo.py` starts the CLI.
- The menu loops until the user chooses quit.
- Invalid menu options do not crash the app.
- Non-numeric delete input does not crash the app.

---

## 8. Data Requirements

### Active in-memory task list

Use one module-level list:

```python
tasks = []
```

Each item is a task title string.

### Persistence file

Use:

```text
todos.csv
```

### CSV format

Use:

```csv
title
Task one
Task two
```

Rules:

- One task per row.
- Header row is required.
- Load should ignore completely blank rows.
- Preserve task order.

---

## 9. Technical Requirements

- Language: Python 3.
- Runtime target: GitHub Codespaces.
- External dependencies: none.
- Required standard library modules:
  - `csv`
  - `os` or `pathlib` if needed
  - `unittest` for tests
  - `io` and `contextlib` for testing printed output if useful
  - `unittest.mock` for patching input/output/file path during tests if useful

---

## 10. Required Repository Structure

Recommended minimal structure:

```text
.
├── Challenge.txt
├── need.png
├── evaluate.png
├── PRD.md
├── SPECS.md
├── README.md
├── todo.py
├── test_todo.py
└── todos.csv              # generated by the app; may be ignored or included only as sample
```

Optional:

```text
└── .gitignore
```

Recommended `.gitignore`:

```gitignore
__pycache__/
*.pyc
.coverage
```

Do not ignore `todos.csv` if the assignment evaluator expects to inspect persistence output. If unsure, leave `todos.csv` unignored but do not rely on it being pre-existing.

---

## 11. Testing Requirements

Testing must use Python standard library only.

Required automated tests in `test_todo.py`:

1. `add_one_task(title)` appends one task.
2. Multiple added tasks preserve order.
3. `print_list()` displays 1-based numeric positions.
4. `delete_task(number_to_delete)` deletes the intended task.
5. Deleting an invalid position does not alter the list.
6. `save_todos()` creates a valid CSV file.
7. `load_todos()` reconstructs tasks from `todos.csv`.
8. Save followed by load round-trips data correctly.
9. Loading a missing CSV file does not crash.
10. Empty titles are rejected.

Test command:

```bash
python -m unittest -v
```

Syntax check:

```bash
python -m py_compile todo.py test_todo.py
```

Manual CLI smoke test:

```bash
python todo.py
```

Then manually verify:

1. Add two tasks.
2. List tasks.
3. Delete task 1.
4. List tasks again.
5. Save.
6. Quit.
7. Re-run `python todo.py`.
8. Load.
9. List tasks.

---

## 12. Acceptance Criteria / Rubric Traceability

| Rubric item | Implementation requirement |
|---|---|
| `add_one_task(title)` correctly appends new tasks to the active list | Implement exact function name and append sanitized title |
| `print_list()` outputs tasks in order with positions users can reference | Use 1-based printed positions |
| `delete_task(number_to_delete)` removes the intended task and updates list correctly | Convert 1-based input to 0-based internal index safely |
| `save_todos()` writes current tasks into `todos.csv` in reusable format | Use CSV header `title` and one task per row |
| `load_todos()` reconstructs tasks from `todos.csv` correctly | Replace active list with CSV contents in order |
| CLI behavior is consistent with create, list, delete, save, and load | Implement looping terminal menu |
| Task editing is out of scope | Do not implement edit/update menu option |
| Standard library only | Do not install or import external packages |

---

## 13. Definition of Done

The project is complete when:

- `todo.py` exists and runs from the command line.
- The exact required functions exist.
- `python -m py_compile todo.py test_todo.py` passes.
- `python -m unittest -v` passes.
- CLI can add, list, delete, save, and load tasks.
- `todos.csv` is generated in the required reusable format.
- No external packages are required.
- No task editing flow exists.
- `Challenge.txt`, `need.png`, and `evaluate.png` have been reviewed and their requirements are reflected in the final build.
