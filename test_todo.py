import csv
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import todo


class TestTodo(unittest.TestCase):
    def setUp(self):
        todo.tasks.clear()
        self._original_todo_file = todo.TODO_FILE

    def tearDown(self):
        todo.TODO_FILE = self._original_todo_file

    def test_add_one_task_appends_valid_task(self):
        with redirect_stdout(io.StringIO()):
            todo.add_one_task("Call carrier")
        self.assertEqual(todo.tasks, ["Call carrier"])

    def test_add_one_task_preserves_order(self):
        with redirect_stdout(io.StringIO()):
            todo.add_one_task("Call carrier")
            todo.add_one_task("Confirm pickup")
        self.assertEqual(todo.tasks, ["Call carrier", "Confirm pickup"])

    def test_add_one_task_rejects_empty_or_whitespace_titles(self):
        with redirect_stdout(io.StringIO()):
            todo.add_one_task("")
            todo.add_one_task("   ")
        self.assertEqual(todo.tasks, [])

    def test_print_list_outputs_1_based_positions(self):
        todo.tasks[:] = ["Call carrier", "Confirm pickup"]
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            todo.print_list()
        output = buffer.getvalue()
        self.assertIn("1. Call carrier", output)
        self.assertIn("2. Confirm pickup", output)

    def test_print_list_handles_empty_list(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            todo.print_list()
        self.assertIn("No tasks found.", buffer.getvalue())

    def test_delete_task_removes_intended_task(self):
        todo.tasks[:] = ["Call carrier", "Confirm pickup", "Send update"]
        with redirect_stdout(io.StringIO()):
            todo.delete_task(2)
        self.assertEqual(todo.tasks, ["Call carrier", "Send update"])

    def test_delete_task_invalid_positions_do_not_mutate_list(self):
        todo.tasks[:] = ["Call carrier", "Confirm pickup"]
        original = todo.tasks.copy()

        for invalid_value in (0, -1, 99, "abc"):
            with redirect_stdout(io.StringIO()):
                todo.delete_task(invalid_value)
            self.assertEqual(todo.tasks, original)

    def test_save_todos_writes_reusable_csv(self):
        todo.tasks[:] = ["Call carrier", "Confirm pickup"]

        with tempfile.TemporaryDirectory() as tmpdir:
            todo.TODO_FILE = str(Path(tmpdir) / "todos.csv")
            with redirect_stdout(io.StringIO()):
                todo.save_todos()

            self.assertTrue(os.path.exists(todo.TODO_FILE))
            with open(todo.TODO_FILE, newline="") as file:
                rows = list(csv.reader(file))
            self.assertEqual(rows[0], ["title"])
            self.assertEqual(rows[1:], [["Call carrier"], ["Confirm pickup"]])

    def test_load_todos_reconstructs_tasks_in_order(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            todo.TODO_FILE = str(Path(tmpdir) / "todos.csv")
            with open(todo.TODO_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title"])
                writer.writerow(["Call carrier"])
                writer.writerow(["Confirm pickup"])

            with redirect_stdout(io.StringIO()):
                todo.load_todos()

            self.assertEqual(todo.tasks, ["Call carrier", "Confirm pickup"])

    def test_save_and_load_round_trip(self):
        with redirect_stdout(io.StringIO()):
            todo.add_one_task("Call carrier")
            todo.add_one_task("Confirm pickup")

        with tempfile.TemporaryDirectory() as tmpdir:
            todo.TODO_FILE = str(Path(tmpdir) / "todos.csv")
            with redirect_stdout(io.StringIO()):
                todo.save_todos()
            todo.tasks.clear()
            with redirect_stdout(io.StringIO()):
                todo.load_todos()
            self.assertEqual(todo.tasks, ["Call carrier", "Confirm pickup"])

    def test_load_todos_handles_missing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            todo.TODO_FILE = str(Path(tmpdir) / "missing.csv")
            with redirect_stdout(io.StringIO()):
                todo.load_todos()
            self.assertEqual(todo.tasks, [])

    def test_save_todos_writes_header_only_for_empty_list(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            todo.TODO_FILE = str(Path(tmpdir) / "todos.csv")
            with redirect_stdout(io.StringIO()):
                todo.save_todos()

            self.assertTrue(os.path.exists(todo.TODO_FILE))
            with open(todo.TODO_FILE, newline="") as file:
                rows = list(csv.reader(file))
            self.assertEqual(rows, [["title"]])


if __name__ == "__main__":
    unittest.main()
