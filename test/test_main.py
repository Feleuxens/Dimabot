import pytest

from test.mocks.bot import MockBot
from test.mocks.channel import MockChannel
from test.mocks.guild import MockGuild
from test.mocks.message import MockMessage

from dimabot.main import _check_prefix


# noinspection PyTypeChecker
class TestCheckPrefix:
    @pytest.mark.asyncio
    async def test_prefix_without_guild(self):
        bot = MockBot()
        msg = MockMessage()
        assert await _check_prefix(bot, msg) == [f"<@!{bot.user.id}> ", f"<@{bot.user.id}> ", f"<@!{bot.user.id}>",
                                                 f"<@{bot.user.id}>", "."]

    @pytest.mark.asyncio
    async def test_prefix_with_unknown_guild(self):
        bot = MockBot()
        msg = MockMessage(channel=MockChannel(guild=MockGuild(123)))
        assert await _check_prefix(bot, msg) == [f"<@!{bot.user.id}> ", f"<@{bot.user.id}> ", f"<@!{bot.user.id}>",
                                                 f"<@{bot.user.id}>", "."]

