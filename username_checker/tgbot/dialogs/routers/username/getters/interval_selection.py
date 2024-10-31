from typing import Any

from fluentogram import TranslatorRunner

from username_checker.core.entities.subscription import Interval


async def interval_buttons_getter(i18n: TranslatorRunner, **_: Any) -> Any:
    """Get interval buttons."""
    buttons = [
        {
            "interval_seconds": interval.value,
            "interval_readable": i18n.get(
                "interval-selection-button-username-dialog",
                interval=interval.value,
            ),
        } for interval in Interval
    ]
    return {"interval_buttons": buttons}
