import pytest

from test.mocks.bot import MockBot

from dimabot.utils.extensions import load_extensions, unload_extensions, reload_extensions


# noinspection PyTypeChecker
class TestLoadExtension:
    def test_load_one_extension(self):
        self.bot = MockBot()
        load_extensions(self.bot, "test")
        assert "extensions.test" in self.bot.loaded_extensions

    def test_load_multiple_extensions(self):
        self.bot = MockBot()
        extensions = ["1", "2", "3", "4", "5"]
        load_extensions(self.bot, *extensions)
        for i in extensions:
            assert f"extensions.{i}" in self.bot.loaded_extensions

    def test_load_int(self):
        self.bot = MockBot()
        pytest.raises(TypeError, load_extensions, self.bot, 1)


# noinspection PyTypeChecker
class TestUnloadExtension:
    def test_unload_one_extension(self):
        self.bot = MockBot()
        self.bot.loaded_extensions = ["extensions.test"]
        unload_extensions(self.bot, "test")
        assert self.bot.loaded_extensions == []

    def test_unload_multiple_extensions(self):
        self.bot = MockBot()
        self.bot.loaded_extensions = ["extensions.1", "extensions.2", "extensions.3"]
        unload_extensions(self.bot, "1", "2", "3")
        assert self.bot.loaded_extensions == []

    def test_unload_unknown_extension(self):
        self.bot = MockBot()
        self.bot.loaded_extensions = []
        pytest.raises(ValueError, unload_extensions, self.bot, "test")


# noinspection PyTypeChecker
class TestReloadExtension:
    @pytest.mark.asyncio
    async def test_reload_one_extension(self):
        self.bot = MockBot()
        self.bot.loaded_extensions = ["extensions.test"]
        embed = await reload_extensions(self.bot, "author", "test")
        assert self.bot.loaded_extensions == ["extensions.test"]
        assert embed.title == "Reloaded"

    @pytest.mark.asyncio
    async def test_reload_multiple_extensions(self):
        self.bot = MockBot()
        self.bot.loaded_extensions = ["extensions.1", "extensions.2", "extensions.3"]
        embed = await reload_extensions(self.bot, "author", "1", "2", "3")
        assert self.bot.loaded_extensions == ["extensions.1", "extensions.2", "extensions.3"]
        assert embed.title == "Reloaded"

    @pytest.mark.asyncio
    async def test_reload_unknown_extensions(self):
        self.bot = MockBot()
        self.bot.loaded_extensions = ["extensions.1", "extensions.2"]
        with pytest.raises(ValueError):
            await reload_extensions(self.bot, "author", "3")
