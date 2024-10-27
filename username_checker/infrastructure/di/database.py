from collections.abc import AsyncIterable

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from username_checker.common.log.configuration import LoggerName
from username_checker.common.log.installer import LoggersInstaller
from username_checker.common.settings.models.db import RDBSettings
from username_checker.core.interfaces import subscription as si
from username_checker.core.interfaces import username as uni
from username_checker.core.interfaces.commiter import Commiter
from username_checker.infrastructure.database.rdb.dao.subscription import SubscriptionDAO
from username_checker.infrastructure.database.rdb.dao.user import UserDAO
from username_checker.infrastructure.database.rdb.dao.username import UsernameDAO
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

    scope = Scope.REQUEST

    holder = provide(HolderDAO, scope=Scope.REQUEST, provides=AnyOf[HolderDAO, Commiter])

    @provide
    async def get_subscription_dao(self, holder: HolderDAO) -> AnyOf[
        SubscriptionDAO, si.SubscriptionDeleter, si.SubscriptionGetter, si.SubscriptionUpserter,
    ]:
        """Get the subscription DAO."""
        return holder.subscription

    @provide
    async def get_user_dao(self, holder: HolderDAO) -> UserDAO:
        """Get the user DAO."""
        return holder.user

    @provide
    async def get_username_dao(self, holder: HolderDAO) -> AnyOf[
        UsernameDAO, uni.UsernameDeleter, uni.UsernameGetter, uni.UsernameInspector, uni.UsernameUpserter,
    ]:
        """Get the username DAO."""
        return holder.username


def get_database_providers() -> list[Provider]:
    """Returns a list of database providers for di."""
    return [
        DbProvider(),
        TMProvider(),
        DAOProvider(),
    ]
