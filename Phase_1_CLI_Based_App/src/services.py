"""Business logic services for the CLI Todo Application."""

from src.models import Task
from src.storage import load_tasks, save_tasks


def add_task(description: str) -> Task:
    """Add a new task with the given description.

    Args:
        description: The task description (must be non-empty after stripping).

    Returns:
        The newly created Task object.

    Raises:
        ValueError: If description is empty or whitespace only.
    """
    description = description.strip()
    if not description:
        raise ValueError("Description cannot be empty")

    tasks = load_tasks()

    # Generate next ID (max existing + 1, or 1 if empty)
    next_id = max((task.id for task in tasks), default=0) + 1

    new_task = Task(id=next_id, description=description, completed=False)
    tasks.append(new_task)
    save_tasks(tasks)

    return new_task


def list_tasks() -> list[Task]:
    """Get all tasks.

    Returns:
        List of all Task objects.
    """
    return load_tasks()


def complete_task(task_id: int) -> Task:
    """Toggle the completion status of a task.

    Args:
        task_id: The ID of the task to toggle.

    Returns:
        The updated Task object.

    Raises:
        ValueError: If task_id is not a positive integer.
        KeyError: If no task with the given ID exists.
    """
    if task_id <= 0:
        raise ValueError("ID must be a positive integer")

    tasks = load_tasks()

    for task in tasks:
        if task.id == task_id:
            task.completed = not task.completed
            save_tasks(tasks)
            return task

    raise KeyError(f"Task with ID {task_id} not found")


def update_task(task_id: int, description: str) -> tuple[str, Task]:
    """Update the description of a task.

    Args:
        task_id: The ID of the task to update.
        description: The new description (must be non-empty after stripping).

    Returns:
        A tuple of (old_description, updated_task).

    Raises:
        ValueError: If task_id is not positive or description is empty.
        KeyError: If no task with the given ID exists.
    """
    if task_id <= 0:
        raise ValueError("ID must be a positive integer")

    description = description.strip()
    if not description:
        raise ValueError("Description cannot be empty")

    tasks = load_tasks()

    for task in tasks:
        if task.id == task_id:
            old_description = task.description
            task.description = description
            save_tasks(tasks)
            return old_description, task

    raise KeyError(f"Task with ID {task_id} not found")


def delete_task(task_id: int) -> Task:
    """Delete a task by ID.

    Args:
        task_id: The ID of the task to delete.

    Returns:
        The deleted Task object.

    Raises:
        ValueError: If task_id is not a positive integer.
        KeyError: If no task with the given ID exists.
    """
    if task_id <= 0:
        raise ValueError("ID must be a positive integer")

    tasks = load_tasks()

    for i, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(i)
            save_tasks(tasks)
            return deleted_task

    raise KeyError(f"Task with ID {task_id} not found")
