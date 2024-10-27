from dishka import Provider, Scope, provide

from username_checker.common.log.configuration import LoggerName
from username_checker.common.log.installer import LoggersInstaller
from username_checker.core.interfaces.uploader import UsernameUploader
from username_checker.infrastructure.uploader.json import JSONFileUsernameUploader


class UploaderProvider(Provider):

    """Provider for uploader."""

    @provide(scope=Scope.APP)
    def get_username_uploader(self, installer: LoggersInstaller) -> UsernameUploader:
        """Returns a username uploader."""
        logger = installer.get_logger(LoggerName.USERNAME_UPLOADER)
        return JSONFileUsernameUploader(logger)


def get_uploader_providers() -> list[Provider]:
    """Returns a list of uploader providers for di."""
    return [
        UploaderProvider(),
    ]
