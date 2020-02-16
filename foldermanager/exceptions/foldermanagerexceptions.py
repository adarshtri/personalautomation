class FolderManagerExceptions(Exception):

    def __init__(self, message, errors):

        # calling the base class constructor
        super().__init__(message)
        self.message = message
        self.errors = errors


class InvalidConfigurationFileException(FolderManagerExceptions):
    pass


class ConfigurationFileNotFoundException(FolderManagerExceptions):
    pass


class ConfigurationFileParseException(FolderManagerExceptions):
    pass