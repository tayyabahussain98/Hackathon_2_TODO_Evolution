"""Data models for the CLI Todo Application."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique positive integer identifier, auto-assigned by the system.
        description: Non-empty string describing the task.
        completed: Boolean flag indicating whether the task is done (default: False).
    """
    id: int
    description: str
    completed: bool = False
