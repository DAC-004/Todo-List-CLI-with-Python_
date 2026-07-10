# SPECS.md — Todo List CLI Technical Specification

## 1. Scope

Implement a Python command-line Todo List app using only the Python standard library.

The build must follow three source files:

- `Challenge.txt`
- `need.png`
- `evaluate.png`

The app must satisfy the challenge brief, the implementation checklist, and the evaluation rubric. The required behavior is intentionally small. Do not expand beyond it.

---

## 2. Required Files

The final repository should include:

```text
todo.py
test_todo.py
README.md
PRD.md
SPECS.md
Challenge.txt
need.png
evaluate.png
```

The app generates:

```text
todos.csv
```

---

## 3. Required Function Names

The following names and signatures are mandatory:

```python
def add_one_task(title):
    ...

def print_list():
    ...

def delete_task(number_to_delete):
    ...

def save_todos():
    ...

def load_todos():
    ...
```

Do not rename these functions.

Do not require parameters for:

- `print_list()`
- `save_todos()`
- `load_todos()`

The evaluator may import these functions directly.

---

## 4. Module-Level State

Use one active in-memory list:

```python
tasks = []
```

Use one file path constant:

```python
TODO_FILE = "todos.csv"
```

All required functions must operate on the module-level `tasks` list.

---

## 5. Function Specifications

### 5.1 `add_one_task(title)`

#### Purpose

Add one new task title to the active in-memory task list.

#### Input

- `title`: expected to be a string.

#### Behavior

- Convert input to string if necessary.
- Strip leading/trailing whitespace.
- If the cleaned title is empty, do not append it.
- If valid, append the title to `tasks`.

#### Output

- No required return value.
- May print a confirmation message.

#### Required examples

```python
tasks.clear()
add_one_task("Call carrier")
assert tasks == ["Call carrier"]

add_one_task(" Confirm pickup ")
assert tasks == ["Call carrier", "Confirm pickup"]
```

---

### 5.2 `print_list()`

#### Purpose

Print all pending tasks with numeric positions.

#### Behavior

- Print tasks in current order.
- Use 1-based positions.
- Do not mutate `tasks`.
- If the list is empty, print a clear empty-list message.

#### Required example

Given:

```python
tasks[:] = ["Call carrier", "Confirm pickup"]
```

Output must be equivalent to:

```text
1. Call carrier
2. Confirm pickup
```

The exact wording around headers may vary, but the numeric positions and task titles must be clear.

---

### 5.3 `delete_task(number_to_delete)`

#### Purpose

Remove one task using the user-facing numeric list position.

#### Input

- `number_to_delete`: expected to represent a 1-based task position.

#### Behavior

- Convert input to integer safely.
- Treat `1` as the first task.
- Delete only the intended task.
- If the value is invalid, non-numeric, too small, or too large:
  - Do not crash.
  - Do not modify the list.
  - Print a clear error message.

#### Required example

```python
tasks[:] = ["Call carrier", "Confirm pickup", "Send update"]
delete_task(2)
assert tasks == ["Call carrier", "Send update"]
```

---

### 5.4 `save_todos()`

#### Purpose

Persist current tasks to `todos.csv`.

#### Behavior

- Use the Python standard library `csv` module.
- Open the file with `newline=""`.
- Write a header row.
- Write one task per row.
- Overwrite the file with current `tasks`.
- Preserve task order.

#### Required CSV format

```csv
title
Call carrier
Confirm pickup
```

#### Required example

```python
tasks[:] = ["Call carrier", "Confirm pickup"]
save_todos()
```

Expected result:

- A file named `todos.csv` exists.
- It contains a header named `title`.
- It contains two task rows.

---

### 5.5 `load_todos()`

#### Purpose

Reconstruct the active task list from `todos.csv`.

#### Behavior

- Use the Python standard library `csv` module.
- If `todos.csv` does not exist:
  - Do not crash.
  - Leave the active list empty or unchanged according to the implementation decision below.
- Recommended implementation decision:
  - If the file is missing, clear `tasks` and print a clear message.
- If the file exists:
  - Replace `tasks` with the file contents.
  - Preserve row order.
  - Ignore blank rows.

#### Required example

Given `todos.csv`:

```csv
title
Call carrier
Confirm pickup
```

Then:

```python
tasks.clear()
load_todos()
assert tasks == ["Call carrier", "Confirm pickup"]
```

---

## 6. CLI Specification

### 6.1 Entry point

Use:

```python
if __name__ == "__main__":
    main()
```

### 6.2 Main loop

Implement a `main()` function with a loop.

Suggested menu:

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

### 6.3 Menu behavior

| Option | Action |
|---|---|
| `1` | Prompt for task title, call `add_one_task(title)` |
| `2` | Call `print_list()` |
| `3` | Prompt for task number, call `delete_task(number)` |
| `4` | Call `save_todos()` |
| `5` | Call `load_todos()` |
| `6` | Exit loop |
| Other | Print invalid option message and continue |

### 6.4 Add-many requirement

The loop must not exit after adding a task. A user must be able to add as many tasks as needed in the same run.

### 6.5 No editing

Do not include:

```text
Edit task
Update task
Rename task
Modify task
```

Editing is explicitly out of scope.

---

## 7. Error Handling Rules

The app must not crash for normal invalid user input.

### Required handling

| Scenario | Expected behavior |
|---|---|
| Empty task title | Do not add; print message |
| Whitespace-only task title | Do not add; print message |
| Delete non-numeric value | Do not crash; print message |
| Delete `0` | Do not crash; list unchanged |
| Delete negative number | Do not crash; list unchanged |
| Delete number greater than list length | Do not crash; list unchanged |
| Save empty list | Create valid CSV with header only |
| Load missing file | Do not crash |
| Load empty CSV | Result should be an empty task list |
| Load CSV with blank rows | Ignore blank rows |

---

## 8. Standard Library Only

Allowed imports include:

```python
import csv
from pathlib import Path
```

For tests:

```python
import csv
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
```

Do not use:

```python
click
typer
rich
pandas
pytest
questionary
prompt_toolkit
```

No external package is required or allowed.

---

## 9. Testing Specification

Create `test_todo.py` using `unittest`.

### 9.1 Test isolation

Each test must reset the module-level task list:

```python
import todo

def setUp(self):
    todo.tasks.clear()
```

Use `tempfile.TemporaryDirectory()` and patch `todo.TODO_FILE` for file tests so tests do not pollute the real project directory.

Example:

```python
with tempfile.TemporaryDirectory() as tmpdir:
    todo.TODO_FILE = str(Path(tmpdir) / "todos.csv")
```

If assigning directly to `todo.TODO_FILE`, restore it in `tearDown()`.

---

### 9.2 Required tests

Implement tests for all rubric items.

#### Test 1 — Add one task

```python
todo.add_one_task("Call carrier")
self.assertEqual(todo.tasks, ["Call carrier"])
```

#### Test 2 — Add multiple tasks in order

```python
todo.add_one_task("Call carrier")
todo.add_one_task("Confirm pickup")
self.assertEqual(todo.tasks, ["Call carrier", "Confirm pickup"])
```

#### Test 3 — Reject empty title

```python
todo.add_one_task("   ")
self.assertEqual(todo.tasks, [])
```

#### Test 4 — Print list positions

Capture stdout and verify:

- `1. Call carrier`
- `2. Confirm pickup`

#### Test 5 — Delete intended task

Start with:

```python
["Call carrier", "Confirm pickup", "Send update"]
```

Call:

```python
delete_task(2)
```

Expect:

```python
["Call carrier", "Send update"]
```

#### Test 6 — Invalid delete does not mutate list

Test:

- `0`
- `-1`
- `99`
- `"abc"`

#### Test 7 — Save writes reusable CSV

Verify:

- File exists.
- Header equals `["title"]`.
- Rows equal saved task titles.

#### Test 8 — Load reconstructs from CSV

Write a CSV test fixture manually, call `load_todos()`, verify task list.

#### Test 9 — Save/load round trip

Add tasks, save, clear memory, load, verify restored list.

#### Test 10 — Load missing file does not crash

Patch `TODO_FILE` to a missing path, call `load_todos()`, assert no exception.

---

## 10. Test Commands

Run all tests:

```bash
python -m unittest -v
```

Compile check:

```bash
python -m py_compile todo.py test_todo.py
```

Run app manually:

```bash
python todo.py
```

Optional combined verification:

```bash
python -m py_compile todo.py test_todo.py && python -m unittest -v
```

---

## 11. Manual Acceptance Test

Run:

```bash
python todo.py
```

Then perform this sequence:

1. Choose `1`, add `Call carrier`.
2. Choose `1`, add `Confirm pickup`.
3. Choose `2`, confirm:
   - `1. Call carrier`
   - `2. Confirm pickup`
4. Choose `3`, delete `1`.
5. Choose `2`, confirm:
   - `1. Confirm pickup`
6. Choose `4`, save.
7. Choose `6`, quit.
8. Run `python todo.py` again.
9. Choose `5`, load.
10. Choose `2`, confirm:
    - `1. Confirm pickup`

---

## 12. README Requirements

Create or update `README.md` with:

- Project name.
- Short description.
- Source references:
  - `Challenge.txt`
  - `need.png`
  - `evaluate.png`
- Features.
- How to run.
- How to test.
- File format for `todos.csv`.
- Out-of-scope note: no task editing.

---

## 13. Rubric Compliance Checklist

Before final commit, verify:

- [ ] `Challenge.txt` has been read and followed.
- [ ] `need.png` has been read and followed.
- [ ] `evaluate.png` has been read and followed.
- [ ] `add_one_task(title)` exists and appends valid tasks.
- [ ] `print_list()` exists and prints 1-based positions.
- [ ] `delete_task(number_to_delete)` exists and deletes the intended task.
- [ ] `save_todos()` exists and writes `todos.csv`.
- [ ] `load_todos()` exists and reconstructs tasks from `todos.csv`.
- [ ] CLI supports create, list, delete, save, load.
- [ ] Users can add many tasks in one run.
- [ ] No edit/update task feature exists.
- [ ] Standard library only.
- [ ] `python -m py_compile todo.py test_todo.py` passes.
- [ ] `python -m unittest -v` passes.
