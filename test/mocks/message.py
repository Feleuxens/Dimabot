from test.mocks.channel import MockChannel


class MockMessage:
    def __init__(self, channel: MockChannel):
        self.channel = channel
        self.guild = channel.guild
