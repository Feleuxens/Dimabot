from test.mocks.guild import MockGuild


class MockChannel:
    def __init__(self, guild: MockGuild = None):
        self.guild = guild
