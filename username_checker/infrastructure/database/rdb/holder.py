from username_checker.infrastructure.database.rdb.dao.user import UserDAO
from username_checker.infrastructure.database.rdb.tm import TransactionManager


class HolderDAO:

    """A container class that holds all DAO objects and provides a convenient way to commit transactions."""

    def __init__(self, manager: TransactionManager) -> None:
        self._manager = manager
        self.user = UserDAO(self._manager.session)

    async def commit(self) -> None:
        """Commits the current transaction."""
        await self._manager.commit()

    async def rollback(self) -> None:
        """Rolls back the current transaction."""
        await self._manager.rollback()
