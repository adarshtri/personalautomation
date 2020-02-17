from foldermanager.config.managers.configmanager import ConfigurationConstants, ConfigurationManager
from foldermanager.tools.keepitclean import KeepItClean


class Context(object):

    def __init__(self, context):
        self.context = context

    def run(self):

        for utility_type in self.context:

            if utility_type == ConfigurationConstants.KEEPITCLEAN_CONFIGURATION:
                self._handle_keep_it_clean_type_utility(self.context[utility_type])

    @staticmethod
    def _handle_keep_it_clean_type_utility(configuration):
        for format_type in configuration:
            for conf in configuration[format_type]:
                keep_it_clean_obj = KeepItClean(file_format=format_type, src=conf["src"], dest=conf["dest"])
                keep_it_clean_obj.clean_source_directory()


class ContextManager(object):

    context = None
    configurationFile = None

    def __init__(self):
        raise Exception("Can not instantiate ContextManager class.")

    @staticmethod
    def _create_context(configuration_file):

        if ContextManager.context:
            raise Exception("Context already exists. Use get_or_create_context() instead.")

        ContextManager.configurationFile = configuration_file
        configuration_manager = ConfigurationManager(configuration_file=configuration_file)
        ContextManager.context = Context(context=configuration_manager.get_configuration())

    @staticmethod
    def get_context(configuration_file):

        if not ContextManager.context:
            ContextManager._create_context(configuration_file=configuration_file)

        return ContextManager.context

    @staticmethod
    def get_or_create_context(configuration_file):

        if not ContextManager.context:
            ContextManager._create_context(configuration_file=configuration_file)

        return ContextManager.context

    @staticmethod
    def _get_context_internal():

        if not ContextManager.context:
            raise Exception("Create a context. Context missing.")

        return ContextManager.context
