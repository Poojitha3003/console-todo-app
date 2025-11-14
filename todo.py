"""
todo.py - Console To-Do List with:
  - persistent storage (tasks.json)
  - mark complete / unmark
  - colored console (colorama)
  - due date & time
  - priority (High / Medium / Low)
  - search tasks
  - sorting options
"""

import json
import os
from datetime import datetime
from colorama import init as colorama_init, Fore, Style

colorama_init(autoreset=True)

TASK_FILE = "tasks.json"
DATE_FORMAT = "%Y-%m-%d %H:%M"


# --------------------------
# Helper Functions
# --------------------------
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    try:
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def color(text, c):
    return f"{c}{text}{Style.RESET_ALL}"


def parse_dt(text):
    if not text:
        return None
    try:
        return datetime.strptime(text, DATE_FORMAT)
    except:
        return None


def format_dt(dt):
    return dt.strftime(DATE_FORMAT) if dt else "No due date"


# --------------------------
# Core Features
# --------------------------
def view_tasks(tasks):
    if not tasks:
        print(color("\nNo tasks available.\n", Fore.YELLOW))
        return

    print("\n" + "-" * 45)
    print(color("YOUR TASKS", Fore.CYAN))
    print("-" * 45)

    for i, t in enumerate(tasks, start=1):
        status = "[✔]" if t["completed"] else "[ ]"
        status_col = color(status, Fore.GREEN) if t["completed"] else color(status, Fore.YELLOW)

        title = t["title"]
        due = format_dt(parse_dt(t["due"]))
        priority = t.get("priority") or "None"

        pri_COLOR = {
            "High": Fore.RED,
            "Medium": Fore.YELLOW,
            "Low": Fore.CYAN
        }.get(priority, Fore.WHITE)

        print(f"{i}. {status_col} {title} | Due: {due} | Priority: {color(priority, pri_COLOR)}")

    print("-" * 45 + "\n")


def add_task(tasks):
    title = input("Enter task title: ").strip()
    if not title:
        print(color("Task title cannot be empty.\n", Fore.RED))
        return

    due_in = input(f"Enter due date & time ({DATE_FORMAT}) or leave blank: ").strip()
    due_dt = parse_dt(due_in)
    if due_in and not due_dt:
        print(color(f"Invalid date format! Use: {DATE_FORMAT}\n", Fore.RED))
        return

    print("Select priority: (1) High  (2) Medium  (3) Low  (Enter for none)")
    choice = input("Choice: ").strip()
    priority = {"1": "High", "2": "Medium", "3": "Low"}.get(choice, None)

    task = {
        "title": title,
        "completed": False,
        "due": due_dt.strftime(DATE_FORMAT) if due_dt else None,
        "priority": priority,
        "created_at": datetime.now().strftime(DATE_FORMAT)
    }

    tasks.append(task)
    save_tasks(tasks)
    print(color("Task added successfully!\n", Fore.GREEN))


def remove_task(tasks):
    if not tasks:
        print(color("No tasks to remove.\n", Fore.YELLOW))
        return

    view_tasks(tasks)

    try:
        num = int(input("Enter task number to remove: "))
        if not (1 <= num <= len(tasks)):
            raise Exception
    except:
        print(color("Invalid task number.\n", Fore.RED))
        return

    removed = tasks.pop(num - 1)
    save_tasks(tasks)
    print(color(f"Removed task: {removed['title']}\n", Fore.GREEN))


def mark_task(tasks):
    if not tasks:
        print(color("No tasks to mark.\n", Fore.YELLOW))
        return

    view_tasks(tasks)

    try:
        num = int(input("Enter task number to mark completed: "))
        if not (1 <= num <= len(tasks)):
            raise Exception
    except:
        print(color("Invalid number.\n", Fore.RED))
        return

    tasks[num - 1]["completed"] = True
    save_tasks(tasks)
    print(color("Task marked completed!\n", Fore.GREEN))


def unmark_task(tasks):
    if not tasks:
        print(color("No tasks to unmark.\n", Fore.YELLOW))
        return

    view_tasks(tasks)

    try:
        num = int(input("Enter task number to unmark: "))
        if not (1 <= num <= len(tasks)):
            raise Exception
    except:
        print(color("Invalid number.\n", Fore.RED))
        return

    tasks[num - 1]["completed"] = False
    save_tasks(tasks)
    print(color("Task unmarked.\n", Fore.GREEN))


def search_task(tasks):
    query = input("Search: ").lower().strip()
    results = [t for t in tasks if query in t["title"].lower()]

    if not results:
        print(color("No matching tasks.\n", Fore.YELLOW))
        return

    print(color(f"\nFound {len(results)} task(s):", Fore.CYAN))
    view_tasks(results)


def sort_tasks(tasks):
    print("Sort by:")
    print("1. Due date")
    print("2. Priority (High → Low)")
    print("3. Alphabetical (A → Z)")
    print("4. Created time (Oldest first)")

    ch = input("Choice: ").strip()

    if ch == "1":
        tasks.sort(key=lambda t: (t["due"] is None, parse_dt(t["due"]) or datetime.max))
        print(color("Sorted by due date.\n", Fore.GREEN))

    elif ch == "2":
        pr_val = {"High": 1, "Medium": 2, "Low": 3, None: 4}
        tasks.sort(key=lambda t: pr_val[t["priority"]])
        print(color("Sorted by priority.\n", Fore.GREEN))

    elif ch == "3":
        tasks.sort(key=lambda t: t["title"].lower())
        print(color("Sorted alphabetically.\n", Fore.GREEN))

    elif ch == "4":
        tasks.sort(key=lambda t: parse_dt(t["created_at"]))
        print(color("Sorted by created time.\n", Fore.GREEN))

    else:
        print(color("Invalid choice.\n", Fore.RED))
        return

    save_tasks(tasks)


# --------------------------
# Main Program Loop
# --------------------------
def main():
    tasks = load_tasks()

    while True:
        print(color("=== TO-DO LIST MENU ===", Fore.MAGENTA))
        print("1. View tasks")
        print("2. Add task")
        print("3. Remove task")
        print("4. Mark task as completed")
        print("5. Unmark task")
        print("6. Search tasks")
        print("7. Sort tasks")
        print("8. Exit")

        choice = input("Choose (1-8): ").strip()

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            mark_task(tasks)
        elif choice == "5":
            unmark_task(tasks)
        elif choice == "6":
            search_task(tasks)
        elif choice == "7":
            sort_tasks(tasks)
        elif choice == "8":
            print(color("Goodbye!", Fore.CYAN))
            break
        else:
            print(color("Invalid option.\n", Fore.RED))


if __name__ == "__main__":
    main()
