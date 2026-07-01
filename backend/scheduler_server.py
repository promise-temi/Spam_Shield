import asyncio
import datetime
import logging

from modules.Scheduler import Scheduler

logging.basicConfig(level=logging.INFO)

RUN_HOUR = 9
RUN_MINUTE = 0


async def sleep_until_next_run():
    now = datetime.datetime.now()

    next_run = now.replace(
        # hour=RUN_HOUR,
        # minute=RUN_MINUTE,
        second=0,
        microsecond=0
    )

    if next_run <= now:
        next_run += datetime.timedelta(minutes=1)

    seconds = (next_run - now).total_seconds()

    logging.info(f"Prochaine exécution : {next_run}")
    await asyncio.sleep(seconds)


async def run_scheduler():
    scheduler = Scheduler()

    while True:
        await sleep_until_next_run()

        logging.info("Lancement du scheduler SpamShield")
        scheduler.get_current_phase()
        logging.info("Scheduler terminé")


async def main():
    await run_scheduler()


if __name__ == "__main__":
    asyncio.run(main())