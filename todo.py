import csv

tasks = []
TODO_FILE = "todos.csv"


def add_one_task(title):
    title = str(title).strip()
    if not title:
        print("Task title cannot be empty.")
        return
    tasks.append(title)
    print(f"Added: {title}")


def print_list():
    if not tasks:
        print("No tasks found.")
        return
    for index, title in enumerate(tasks, start=1):
        print(f"{index}. {title}")


def delete_task(number_to_delete):
    try:
        position = int(number_to_delete)
    except (TypeError, ValueError):
        print("Invalid task number.")
        return

    if position < 1 or position > len(tasks):
        print("Invalid task number.")
        return

    removed = tasks.pop(position - 1)
    print(f"Deleted: {removed}")


def save_todos():
    with open(TODO_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["title"])
        for title in tasks:
            writer.writerow([title])
    print(f"Saved {len(tasks)} task(s) to {TODO_FILE}.")


def load_todos():
    try:
        with open(TODO_FILE, newline="") as file:
            reader = csv.DictReader(file)
            loaded = [row["title"].strip() for row in reader if row.get("title", "").strip()]
    except FileNotFoundError:
        print(f"{TODO_FILE} not found.")
        return

    tasks[:] = loaded
    print(f"Loaded {len(tasks)} task(s) from {TODO_FILE}.")


def main():
    print("Todo List CLI")
    while True:
        print("\n1. Add task")
        print("2. List tasks")
        print("3. Delete task")
        print("4. Save tasks")
        print("5. Load tasks")
        print("6. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Enter task title: ")
            add_one_task(title)
        elif choice == "2":
            print_list()
        elif choice == "3":
            number = input("Enter task number to delete: ")
            delete_task(number)
        elif choice == "4":
            save_todos()
        elif choice == "5":
            load_todos()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
