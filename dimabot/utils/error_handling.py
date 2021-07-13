import sentry_sdk
from discord import Embed
from discord.ext.commands import errors, CommandError, Context, Cog

from utils import colors
from utils.logs import get_logger

logger = get_logger(__name__)


class CoreErrorHandler(Cog):
    """
    Cog handling (almost) all command errors
    """

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        # exception have to be ordered from child to parent in exception hierarchy
        # logger.debug(error)

        # Discord Exception -> CommandError -> UserInputError -> MissingRequiredArgument
        if isinstance(error, errors.MissingRequiredArgument):  # lowest children, Parent: UserInputError, Level: 4
            await ctx.send(embed=Embed(title="Something went wrong", description="You need to specify at least one "
                                                                                 "argument.",
                                       color=colors.YELLOW))

        # Discord Exception -> CommandError -> UserInputError -> TooManyArguments
        elif isinstance(error, errors.TooManyArguments):  # lowest children, Parent: UserInputError, Level: 4
            await ctx.send(embed=Embed(title="Something went wrong", description="You specified too many arguments.",
                                       color=colors.RED))

        # Discord Exception -> CommandError -> UserInputError -> BadArgument -> ChannelNotFound
        elif isinstance(error, errors.ChannelNotFound):  # lowest children: Parent: BadArgument, Level: 5
            await ctx.send(embed=Embed(title="Something went wrong",
                                       description="Cannot find that channel. Please check your input.",
                                       color=colors.YELLOW))

        # Discord Exception -> CommandError -> UserInputError -> BadArgument -> RoleNotFound
        elif isinstance(error, errors.RoleNotFound):  # lowest children: Parent: BadArgument, Level: 5
            await ctx.send(embed=Embed(title="Error", description="Cannot find the role. This is most likely due"
                                                                  "to the role being recreated.", color=colors.RED))

        # Discord Exception -> CommandError -> UserInputError
        elif isinstance(error, errors.UserInputError):  # Parent: CommandError, Level: 3
            await ctx.send(embed=Embed(title="Something went wrong", description="Please recheck your arguments.",
                                       color=colors.RED))

        # Discord Exception -> CommandError -> CommandNotFound
        elif isinstance(error, errors.CommandNotFound):  # lowest children, Parent: CommandError, Level: 3
            if "." in error.args[0]:  # ignore message like "..."
                return
            await ctx.send(
                embed=Embed(title="Something went wrong", description="Sorry, I do not know this command. "
                                                                      "Perhaps you misspelled it?",
                            color=colors.RED))

        # Discord Exception -> CommandError -> CheckFailure -> NoPrivateMessage
        elif isinstance(error, errors.NoPrivateMessage):  # lowest children, Parent: CheckFailure, Level: 4
            await ctx.send(embed=Embed(title="Something went wrong",
                                       description="Sorry, you can't use this command outside the server.",
                                       color=colors.YELLOW))

        # Discord Exception -> CommandError -> CheckFailure -> MissingPermissions
        elif isinstance(error, errors.MissingPermissions):  # lowest children, Parent: CheckFailure, Level: 4
            await ctx.send(
                embed=Embed(title="Something went wrong", description="Sorry, you do not have the permission "
                                                                      "to run this command!", color=colors.RED))

        # Discord Exception -> CommandError -> DisabledCommand
        elif isinstance(error, errors.DisabledCommand):  # lowest child, Parent: CommandError, Level: 3
            await ctx.send(embed=Embed(title="Something went wrong", description="This command is currently disabled. "
                                                                                 "Please wait until it gets enabled or "
                                                                                 "flame the developer.",
                                       color=colors.YELLOW))

        # Discord Exception -> CommandError -> CommandOnCooldown
        elif isinstance(error, errors.CommandOnCooldown):  # lowest children, Parent: CommandError, Level: 3
            await ctx.send("Calm down :heart:")

        else:
            logger.error(f"Undhandled error {error} occurred")
            sentry_sdk.capture_exception()
            await ctx.send(
                embed=Embed(title="Something went wrong",
                            description="An unknown error occurred. If you think this "
                                        "shouldn't be happening please inform <@206815202375761920>.",
                            color=colors.RED))
