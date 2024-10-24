from username_checker.core.entities.username import Username, UsernameStatus
from username_checker.core.interfaces.username import UsernameChecker


class TelegramUsernameChecker(UsernameChecker):

    """A class for checking the username status in Telegram."""

    async def check(self, username: Username) -> UsernameStatus:
        """
        Checking a username status in Telegram.

        :param username: The username to be checked.
        :type username: Username
        :return: username status
        :rtype: UsernameStatus
        """
        return UsernameStatus.AVAILABLE
