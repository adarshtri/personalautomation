from foldermanager.context.contextmanager import ContextManager


class KeepItClean(object):

    def __init__(self):
        self._context = ContextManager._get_context_internal()
