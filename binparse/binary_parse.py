import os


class BinaryParse:
    """ The BinaryParse object provide functionality to search for patterns in binary file

    Args:
        file_path (str): Real absolute path to file

    Attributes:
        file_path (str): Store file_path

    """
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError("Fatal error: File not found")
        self.__file_path = file_path
