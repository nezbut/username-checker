from uuid import UUID

from taskiq import ScheduleSource
from taskiq.scheduler.scheduled_task import CronSpec

from username_checker.core.entities.subscription import Interval, Subscription
from username_checker.core.interfaces.scheduler import Scheduler
from username_checker.infrastructure.tkq.tasks import check_username_task


class SchedulerImpl(Scheduler):

    """A class that implements the Scheduler"""

    def __init__(self, schedule_source: ScheduleSource):

        self.schedule_source = schedule_source
        self._sub_id_key = "sub_id"

    async def schedule_check_username(self, subscription: Subscription) -> str:
        """
        Schedules a username check from a subscription.

        :param subscription: The subscription.
        :type subscription: Subscription
        :return: Identifier of the scheduled check.
        """
        labels = {self._sub_id_key: str(subscription.id)}
        cron = self._get_cron(subscription.interval)
        schedule = await check_username_task.kicker().with_labels(**labels).schedule_by_cron(
            self.schedule_source,
            cron,
            subscription=subscription,
        )
        return schedule.schedule_id

    async def unschedule_check_username(self, subscription_id: UUID) -> None:
        """
        Unscheduled a username check.

        :param subscription_id: Identifier of the subscription.
        :type subscription_id: UUID
        """
        schedule_tasks = (schedule for schedule in await self.schedule_source.get_schedules())
        for schedule_task in schedule_tasks:
            if schedule_task.labels.get(self._sub_id_key) == str(subscription_id):
                await self.schedule_source.delete_schedule(
                    schedule_id=schedule_task.schedule_id,
                )
                break

    def _get_cron(self, interval: Interval) -> CronSpec:
        match interval:
            case Interval.MINUTE_1:
                cron = CronSpec()
            case Interval.MINUTE_30:
                cron = CronSpec(minutes="*/30")
            case Interval.HOUR_1:
                cron = CronSpec(minutes="0")
            case Interval.DAY_1:
                cron = CronSpec(minutes="0", hours="0")
            case _:
                cron = CronSpec()
        return cron
