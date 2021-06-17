import logging
import sys

import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from utils.env import VERBOSITY, SENTRY_ENVIRONMENT

logging_handler = logging.StreamHandler(sys.stdout)
if VERBOSITY.upper() == "DEBUG":
    logging_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s"))
else:
    logging_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))


def get_logger(name: str) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(name)
    logger.addHandler(logging_handler)
    logger.setLevel(VERBOSITY.upper())

    return logger


def setup_sentry(dsn: str, name: str, version: str):
    sentry_sdk.init(
        dsn=dsn,
        attach_stacktrace=True,
        shutdown_timeout=5,
        environment=SENTRY_ENVIRONMENT,
        integrations=[
            AioHttpIntegration(),
            LoggingIntegration(
                level=logging.DEBUG,
                event_level=logging.WARNING
            )
        ],
        release=f"{name}@{version}"
    )
