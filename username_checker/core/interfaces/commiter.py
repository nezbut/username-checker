from typing import Protocol


class Commiter(Protocol):

    """A protocol for committing changes."""

    async def commit(self) -> None:
        """Commits changes."""
        ...
