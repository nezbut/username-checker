from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from username_checker.common.log.configuration import LoggerName
from username_checker.common.log.installer import LoggersInstaller
from username_checker.common.settings.models.db import RDBSettings
from username_checker.infrastructure.database.rdb.factory import create_engine, create_session_maker
from username_checker.infrastructure.database.rdb.holder import HolderDAO
from username_checker.infrastructure.database.rdb.tm import TransactionManager


class DbProvider(Provider):

    """Provider for database"""

    scope = Scope.APP

    @provide
    async def get_engine(self, rdb_settings: RDBSettings, installer: LoggersInstaller) -> AsyncIterable[AsyncEngine]:
        """Provides an asynchronous database engine based on the provided configuration."""
        engine = create_engine(rdb_settings)
        logger = installer.get_logger(LoggerName.DB, url=engine.url)
        await logger.ainfo("Database engine created")
        yield engine
        await engine.dispose(close=True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        """Creates a session maker for the given asynchronous database engine."""
        return create_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, pool: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        """Provides an asynchronous database session based on the given session maker."""
        async with pool() as session:
            yield session


class TMProvider(Provider):

    """Provider for Transaction Manager"""

    @provide(scope=Scope.REQUEST)
    async def get_tm(self, session: AsyncSession, installer: LoggersInstaller, rdb_settings: RDBSettings) -> AsyncIterable[TransactionManager]:
        """Provides a Transaction Manager instance for the given asynchronous database session."""
        logger = installer.get_logger(
            LoggerName.DB,
            url=session.bind.url if isinstance(
                session.bind,
                AsyncEngine,
            ) else rdb_settings.make_uri().value,
        )
        async with TransactionManager(session) as tm:
            await logger.ainfo("New transaction")
            yield tm
            await logger.ainfo("End transaction")


class DAOProvider(Provider):

    """Provider for DAO objects."""

    holder = provide(HolderDAO, scope=Scope.REQUEST)


def get_database_providers() -> list[Provider]:
    """Returns a list of database providers for di."""
    return [
        DbProvider(),
        TMProvider(),
        DAOProvider(),
    ]
