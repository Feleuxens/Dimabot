from pathlib import Path

from discord import Intents, Message
from discord.ext.commands import Bot

from utils.changelog import CoreChangelog
from utils.config import load_config, Config
from utils.env import TOKEN, SENTRY_DSN
from utils.error_handling import CoreErrorHandler
from utils.extensions import load_extensions
from utils.logs import get_logger, setup_sentry
from utils.prefix import CorePrefix
from utils.runtime import CoreRuntime

logger = get_logger(__name__)

print(
    r"""
      ____  _                 __          __
     / __ \(_)___ ___  ____ _/ /_  ____  / /_
    / / / / / __ `__ \/ __ `/ __ \/ __ \/ __/
   / /_/ / / / / / / / /_/ / /_/ / /_/ / /_
  /_____/_/_/ /_/ /_/\__,_/_.___/\____/\__/
"""
)

logger.debug("Loading config...")
load_config(Path("config.yml"))


async def _check_prefix(b: Bot, msg: Message):
    p = [f"<@!{b.user.id}> ", f"<@{b.user.id}> ", f"<@!{b.user.id}>", f"<@{b.user.id}>"]
    if msg.guild is None:
        p.append(Config.DEFAULT_PREFIX)
    elif msg.guild.id in Config.SERVER_PREFIXES:
        p.append(Config.SERVER_PREFIXES.get(msg.guild.id))
    else:
        p.append(Config.DEFAULT_PREFIX)
    return p


bot = Bot(command_prefix=_check_prefix, case_insensitive=True, intents=(Intents.all()), self_bot=False)
bot.remove_command("help")  # remove standard help function


extensions = (
    "general.welcome",
    "general.easter_eggs",
    "information.bot_info",
    "information.server_info",
    "information.help",
    "information.list"
)
core = (
    CoreRuntime(bot, *extensions),
    CoreErrorHandler(),
    CoreChangelog(bot),
    CorePrefix(bot)
)


logger.debug("Loading core modules...")
for cog in core:
    bot.add_cog(cog)


@bot.event
async def on_error(*_, **__):
    # sentry_sdk.capture_exception()
    raise  # skipcq: PYL-E0704


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} v{Config.VERSION}\n")


load_extensions(
    bot,
    *extensions
)

if SENTRY_DSN:
    logger.debug("Initializing sentry")
    setup_sentry(SENTRY_DSN, Config.NAME, Config.VERSION)

bot.run(TOKEN)
