from test.mocks.channel import MockChannel


class MockMessage:
    def __init__(self, channel: MockChannel = MockChannel()):
        self.channel = channel
        self.guild = channel.guild
