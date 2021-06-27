from logging import StreamHandler, Formatter, Logger, DEBUG, WARNING, getLogger
from sys import stdout

from sentry_sdk import init
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from utils.env import VERBOSITY, SENTRY_ENVIRONMENT

logging_handler = StreamHandler(stdout)
if VERBOSITY.upper() == "DEBUG":
    logging_handler.setFormatter(Formatter("[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s"))
else:
    logging_handler.setFormatter(Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))


def get_logger(name: str) -> Logger:
    logger: Logger = getLogger(name)
    logger.addHandler(logging_handler)
    logger.setLevel(VERBOSITY.upper())

    return logger


def setup_sentry(dsn: str, name: str, version: str):
    init(
        dsn=dsn,
        attach_stacktrace=True,
        shutdown_timeout=5,
        environment=SENTRY_ENVIRONMENT,
        integrations=[
            AioHttpIntegration(),
            LoggingIntegration(
                level=DEBUG,
                event_level=WARNING
            )
        ],
        release=f"{name}@{version}"
    )
