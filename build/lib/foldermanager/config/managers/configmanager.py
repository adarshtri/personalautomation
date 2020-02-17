import ast
from foldermanager.exceptions import foldermanagerexceptions
from abc import ABC, abstractmethod


class ConfigurationManager(object):

    def __init__(self, configuration_file):
        self._configuration = None
        self._configuration_file = configuration_file
        self._read_configuration_file()
        self._parse_configuration_for_correctness()

    def _read_configuration_file(self):

        """
        :return: dictionary of configuration present in the configuraton file provided
        """

        conf_file_pointer = None

        # opening configuration file pointer, raise exception if file not exists
        try:
            conf_file_pointer = open(self._configuration_file, 'r')
        except FileNotFoundError as fe:
            raise foldermanagerexceptions.ConfigurationFileNotFoundException(
                message="Could not find the configuration file {}.".format(self._configuration_file),
                errors=None)

        configuration_string = conf_file_pointer.read()
        configuration_dictionary = None

        # converting configuration string to dictionary
        try:
            configuration_dictionary = ast.literal_eval(node_or_string=configuration_string)
        except SyntaxError as se:
            raise foldermanagerexceptions.InvalidConfigurationFileException(
                message="Invalid configuration. Check if the file is in proper json format.",
                errors=None
            )

        self._configuration = configuration_dictionary

    def _parse_configuration_for_correctness(self):

        for utility_type in self._configuration:
            if utility_type not in ConfigurationConstants.VALID_FOLDER_MANAGER_UTILITIES:
                raise foldermanagerexceptions.InvalidUtilityConfigurationType(
                    "Utility type \"{}\" is not supported.".format(utility_type),
                    None)
            else:
                parser = ConfigurationConstants.VALID_FOLDER_MANAGER_UTILITIES[utility_type](
                    self._configuration[utility_type])
                try:
                    parser.parse()
                except foldermanagerexceptions.ConfigurationFileParseException as cfpe:
                    self._configuration = None
                    raise foldermanagerexceptions.ConfigurationFileParseException(message=cfpe.message, errors=cfpe.message)

    def get_configuration(self):
        return self._configuration


class ConfigurationFileParser(ABC):

    def __init__(self, configuration):
        self._configuration = configuration

    @abstractmethod
    def parse(self) -> bool:
        pass


class KeepItCleanConfigurationFileParser(ConfigurationFileParser):

    def __init__(self, configuration):
        super().__init__(configuration=configuration)

    def parse(self) -> bool:

        """
        :return: Boolean, True if the configuration passed in matched the specified structured else False
        """
        configuration = self._configuration

        for key in configuration:

            if not isinstance(configuration[key], list):
                raise foldermanagerexceptions.ConfigurationFileParseException(
                    message="Invalid configuration file json format. Kindly visit the documentation for more details.",
                    errors=None)

            for each_conf in configuration[key]:

                if "src" not in each_conf or "dest" not in each_conf:
                    raise foldermanagerexceptions.ConfigurationFileParseException(
                        message="Missing parameter {} in one of the configurations.".format("src/dest"),
                        errors=None
                    )
        return True


class ConfigurationConstants:

    # to implement strategy pattern
    VALID_FOLDER_MANAGER_UTILITIES = {
        "keepitclean": KeepItCleanConfigurationFileParser
    }

    KEEPITCLEAN_CONFIGURATION = "keepitclean"
