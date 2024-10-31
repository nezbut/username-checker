from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from username_checker.core.entities.subscription import SubscriptionIdGenerator
from username_checker.core.entities.username import UsernameIdGenerator
from username_checker.core.interactors import subscription, username
from username_checker.core.interfaces.scheduler import Scheduler
from username_checker.core.interfaces.uploader import UsernameUploader
from username_checker.core.interfaces.username import UsernameChecker
from username_checker.tgbot.utils.data import MiddlewareData


class InteractorsMiddleware(BaseMiddleware):

    """Middleware for interactors."""

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        """Interactors Middleware"""
        container = data["dishka_container"]
        username_id_gen = await container.get(UsernameIdGenerator)
        sub_id_gen = await container.get(SubscriptionIdGenerator)

        data["get_user_subscriptions"] = subscription.GetUserSubscriptions(
            getter=data["sub_getter_i"],
        )

        data["get_username"] = username.GetUsername(
            checker=data["username_checker_i"],
            id_generator=username_id_gen,
            getter=data["username_getter_i"],
            upserter=data["username_upserter_i"],
            inspector=data["username_inspector_i"],
            commiter=data["commiter_i"],
        )
        data["check_username"] = username.CheckUsername(
            checker=data["username_checker_i"],
            upserter=data["username_upserter_i"],
            commiter=data["commiter_i"],
        )
        data["subscribe_check_username"] = username.SubscribeCheckUsername(
            scheduler=data["scheduler_i"],
            id_generator=sub_id_gen,
            upserter=data["sub_upserter_i"],
            commiter=data["commiter_i"],
        )
        data["unsubscribe_check_username"] = username.UnsubscribeCheckUsername(
            scheduler=data["scheduler_i"],
            deleter=data["sub_deleter_i"],
            commiter=data["commiter_i"],
        )
        data["upload_available_usernames"] = username.UploadAvailableUsernames(
            uploader=data["uploader_i"],
            getter=data["username_getter_i"],
        )

        return await handler(event, data)


class InterfacesMiddleware(BaseMiddleware):

    """Middleware for interfaces."""

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, MiddlewareData], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        """Interfaces Middleware"""
        container = data["dishka_container"]
        holder = data["holder_dao"]

        data["commiter_i"] = holder
        data["scheduler_i"] = await container.get(Scheduler)
        data["username_checker_i"] = await container.get(UsernameChecker)
        data["uploader_i"] = await container.get(UsernameUploader)

        data["sub_getter_i"] = holder.subscription
        data["sub_upserter_i"] = holder.subscription
        data["sub_deleter_i"] = holder.subscription

        data["user_getter_i"] = data["user_proxy"]
        data["user_updater_i"] = data["user_proxy"]
        data["user_upserter_i"] = data["user_proxy"]

        data["username_getter_i"] = holder.username
        data["username_deleter_i"] = holder.username
        data["username_inspector_i"] = holder.username
        data["username_getter_i"] = holder.username
        data["username_upserter_i"] = holder.username

        return await handler(event, data)
