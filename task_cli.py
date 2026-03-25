import sys
import json
import os
from datetime import datetime

# JSON file to store tasks
TASK_FILE = "tasks.json"

# Load tasks from JSON


def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Save tasks to JSON


def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Generate unique ID


def generate_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

# Add a new task


def add_task(description):
    tasks = load_tasks()
    task = {
        "id": generate_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task['id']})")

# Update existing task


def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    print(f"Task {task_id} not found")

# Delete task


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Task {task_id} not found")
    else:
        save_tasks(new_tasks)
        print(f"Task {task_id} deleted successfully")

# Mark task in-progress


def mark_in_progress(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as in-progress")
            return
    print(f"Task {task_id} not found")

# Mark task done


def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as done")
            return
    print(f"Task {task_id} not found")

# List tasks


def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status]
    if not tasks:
        print("No tasks found")
        return
    for task in tasks:
        print(f"[{task['id']}] {task['description']} - {task['status']} "
              f"(Created: {task['createdAt']}, Updated: {task['updatedAt']})")

# Main CLI handling


def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return

    command = sys.argv[1]

    try:
        if command == "add":
            description = " ".join(sys.argv[2:])
            if not description:
                print("Error: Task description required")
                return
            add_task(description)

        elif command == "update":
            task_id = int(sys.argv[2])
            description = " ".join(sys.argv[3:])
            if not description:
                print("Error: Task description required")
                return
            update_task(task_id, description)

        elif command == "delete":
            task_id = int(sys.argv[2])
            delete_task(task_id)

        elif command == "mark-in-progress":
            task_id = int(sys.argv[2])
            mark_in_progress(task_id)

        elif command == "mark-done":
            task_id = int(sys.argv[2])
            mark_done(task_id)

        elif command == "list":
            if len(sys.argv) == 3:
                status = sys.argv[2].lower()
                if status not in ["todo", "in-progress", "done"]:
                    print("Error: Invalid status. Use todo, in-progress, or done")
                    return
                list_tasks(status)
            else:
                list_tasks()

        else:
            print(f"Unknown command: {command}")

    except IndexError:
        print("Error: Missing arguments")
    except ValueError:
        print("Error: Invalid task ID")


if __name__ == "__main__":
    main()
