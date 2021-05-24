from test.mocks.user import MockUser


class MockBot:
    def __init__(self):
        self.user = MockUser()
        self.loaded_extensions = []
        self.cogs = []

    def load_extension(self, extension_name: str):
        self.loaded_extensions.append(extension_name)

    def unload_extension(self, extension_name: str):
        self.loaded_extensions.remove(extension_name)

    def reload_extension(self, extension_name: str):
        self.loaded_extensions.remove(extension_name)
        self.loaded_extensions.append(extension_name)
