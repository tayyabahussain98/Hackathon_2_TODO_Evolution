"""Rich-based UI formatting for CLI Todo Application."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.models import Task


console = Console()

# Icons
ICON_SUCCESS = "\u2705"  # ✅
ICON_ERROR = "\u274c"    # ❌
ICON_LIST = "\U0001f4cb" # 📋
ICON_COMPLETED = "\u2611"  # ☑
ICON_PENDING = "\u2610"    # ☐


def display_error(message: str) -> None:
    """Display an error message with red formatting.

    Args:
        message: The error message to display.
    """
    console.print(f"{ICON_ERROR} [bold red]Error:[/bold red] {message}")


def display_success(message: str) -> None:
    """Display a success message with green formatting.

    Args:
        message: The success message to display.
    """
    console.print(f"{ICON_SUCCESS} [bold green]{message}[/bold green]")


def display_help() -> None:
    """Display the help/usage information."""
    help_text = f"""{ICON_LIST} [bold blue]Todo CLI[/bold blue] - Manage your tasks from the command line

[bold]Commands:[/bold]
  add "<description>"      Add a new task
  list                     Show all tasks
  complete <id>            Toggle task completion
  update <id> "<desc>"     Update task description
  delete <id>              Remove a task

[bold]Examples:[/bold]
  uv run main.py add "Buy groceries"
  uv run main.py list
  uv run main.py complete 1
  uv run main.py update 1 "Buy organic groceries"
  uv run main.py delete 1"""
    console.print(help_text)


def display_task_table(tasks: list[Task], title: str | None = None) -> None:
    """Display tasks in a formatted table.

    Args:
        tasks: List of Task objects to display.
        title: Optional title for the table.
    """
    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", justify="right", style="cyan", width=6)
    table.add_column("Description", justify="left", style="white")
    table.add_column("Status", justify="center", width=8)

    for task in tasks:
        status_icon = ICON_COMPLETED if task.completed else ICON_PENDING
        status_style = "green" if task.completed else "white"
        table.add_row(
            str(task.id),
            task.description,
            f"[{status_style}]{status_icon}[/{status_style}]"
        )

    if title:
        console.print(f"\n{title}")
    console.print(table)


def display_add_success(task: Task) -> None:
    """Display success message after adding a task.

    Args:
        task: The newly added Task object.
    """
    display_success("Task added successfully!")
    display_task_table([task])


def display_add_error() -> None:
    """Display error message for empty description on add command."""
    display_error("Description cannot be empty.")
    console.print("Usage: uv run main.py add \"<description>\"")


def display_task_list(tasks: list[Task]) -> None:
    """Display the full task list with header.

    Args:
        tasks: List of Task objects to display.
    """
    console.print(f"{ICON_LIST} [bold blue]Your Tasks[/bold blue]")

    if not tasks:
        console.print("No tasks yet! Add one with: uv run main.py add \"<description>\"")
        return

    display_task_table(tasks)


def display_complete_success(task: Task) -> None:
    """Display success message after toggling task completion.

    Args:
        task: The updated Task object.
    """
    if task.completed:
        display_success("Task marked as complete!")
    else:
        display_success("Task marked as pending!")
    display_task_table([task])


def display_task_not_found(task_id: int) -> None:
    """Display error message when task is not found.

    Args:
        task_id: The ID that was not found.
    """
    display_error(f"Task with ID {task_id} not found.")
    console.print("Use 'uv run main.py list' to see all tasks.")


def display_invalid_id(command: str) -> None:
    """Display error message for invalid ID format.

    Args:
        command: The command name for usage hint.
    """
    display_error("ID must be a positive integer.")
    console.print(f"Usage: uv run main.py {command} <id>")


def display_update_success(old_description: str, task: Task) -> None:
    """Display success message after updating a task.

    Args:
        old_description: The previous description before update.
        task: The updated Task object.
    """
    display_success("Task updated successfully!")
    console.print(f"  [dim]Before:[/dim] {old_description}")
    console.print(f"  [dim]After:[/dim]  {task.description}")
    display_task_table([task])


def display_delete_success(task: Task) -> None:
    """Display success message after deleting a task.

    Args:
        task: The deleted Task object.
    """
    display_success("Task deleted successfully!")
    console.print(f"  [dim]Removed:[/dim] {task.description}")
