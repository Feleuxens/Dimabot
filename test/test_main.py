import pytest

from test.mocks.bot import MockBot
from test.mocks.channel import MockChannel
from test.mocks.message import MockMessage

from dimabot.main import _check_prefix


@pytest.mark.asyncio
async def test_check_prefix():
    bot = MockBot()
    msg = MockMessage(channel=MockChannel())

    # noinspection PyTypeChecker
    assert await _check_prefix(bot, msg) == [f"<@!{bot.user.id}> ", f"<@{bot.user.id}> ", f"<@!{bot.user.id}>",
                                             f"<@{bot.user.id}>", "."]
