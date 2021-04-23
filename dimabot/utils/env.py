from os import environ, getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN: str = environ["TOKEN"]
VERBOSITY: str = getenv("VERBOSITY", "INFO")

SENTRY_DSN: str = getenv("SENTRY_DSN")
SENTRY_ENVIRONMENT: str = getenv("SENTRY_ENVIRONMENT", "dev")
