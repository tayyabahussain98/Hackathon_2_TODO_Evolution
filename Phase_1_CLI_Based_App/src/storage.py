"""JSON storage operations for tasks persistence."""

import json
from pathlib import Path

from src.models import Task


TASKS_FILE = Path("tasks.json")


def load_tasks() -> list[Task]:
    """Load tasks from the JSON storage file.

    Returns:
        A list of Task objects. Returns empty list if file doesn't exist
        or contains invalid JSON.

    Raises:
        ValueError: If the JSON file is corrupted or contains invalid data.
    """
    if not TASKS_FILE.exists():
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        tasks = []
        for item in data:
            task = Task(
                id=item["id"],
                description=item["description"],
                completed=item["completed"]
            )
            tasks.append(task)
        return tasks

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in tasks file: {e}") from e
    except (KeyError, TypeError) as e:
        raise ValueError(f"Invalid task data format: {e}") from e


def save_tasks(tasks: list[Task]) -> None:
    """Save tasks to the JSON storage file.

    Args:
        tasks: List of Task objects to persist.

    The file is overwritten on each save operation.
    """
    data = [
        {
            "id": task.id,
            "description": task.description,
            "completed": task.completed
        }
        for task in tasks
    ]

    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
