from foldermanager.config.managers.configmanager import ConfigurationManager


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
        ContextManager.context = configuration_manager.get_configuration()

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
