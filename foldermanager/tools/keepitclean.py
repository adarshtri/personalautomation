import glob
import shutil
from foldermanager.utility.filesystem_check_utilities import *
from foldermanager.exceptions.foldermanagerexceptions import *


class KeepItClean(object):

    def __init__(self, file_format, src, dest):
        self.file_format = file_format
        self.src = src
        self.dest = dest

        self._directory_checks()

    def _directory_checks(self):

        if (not check_valid_directory(self.src)) or (not check_valid_directory(self.dest)):
            raise DirectoryNotExistsException("Source directory {} doesn't exist.", None)

    def clean_source_directory(self):

        files_to_be_moved = glob.glob(self.src + "/*." + self.file_format)

        for file in files_to_be_moved:
            shutil.move(file, self.dest)
