import os
import re


class BinaryParse:
    """The BinaryParse object provide functionality to search for patterns in binary file

    Attributes:
        __file_path (str): Store file_path
        __file_size (str): Store size file
        __chunks (list): List of chunks to read file
    """

    def __init__(self, file_path, parts=5):
        """Initialization object class

        Args:
            file_path (str): Real absolute path to file
            parts (int): Count of parts to split readable file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("Fatal error: File not found")
        self.__file_path = file_path
        self.__file_size = os.path.getsize(file_path)
        self.__chunks = self.__create_chunks(parts)

    def get_file_path(self) -> str:
        """Getter for attribute __file_path"""
        return self.__file_path

    def get_file_size(self) -> int:
        """Getter for attribute __file_size"""
        return self.__file_size

    def get_chunks(self) -> list:
        """Getter for attribute __chunks"""
        return self.__chunks

    def __create_chunks(self, parts) -> list:
        """Create chunks to split readable file to parts

        Args:
            parts (int): Count of parts to split readable file

        Returns:
            List (int): List size of chunks

        Raises:
            ZeroDivisionError: Zero is not correct value for parts of files. One part is using.
        """

        try:
            # Calculate size of parts
            result = [self.__file_size // parts for i in range(parts)]
            # Add rest bytes
            if self.__file_size % parts > 0:
                result[-1] += self.__file_size % parts
        except ZeroDivisionError as e:
            print('Zero is not correct value for parts of files. One part is using.')
            result = [self.__file_size]
        return result

    def __read_next_chunk(self) -> tuple:
        """Generator function to read next part of file

        Returns:
            Tuple (chunk_size, byte):

            chunk_size (int): size of read part
            byte (bytes): read part

        Raises:
            MemoryError: File has very big size
        """

        try:
            with open(self.__file_path, "rb") as file:
                for chunk_size in self.__chunks:
                    byte = file.read(chunk_size).hex().upper()
                    if not byte:
                        break
                    yield chunk_size, byte
        except MemoryError as e:
            print('File has very big size')
            exit(1)

    def find_pattern(self, patterns) -> dict:
        """Search for all patterns in file

        Search each of pattern from patterns dictionary in current file

        Args:
            patterns (dict): dict of search patterns. Keys - patterns as a hex string

        Returns:
            dict
        """
        if not isinstance(patterns, dict):
            raise TypeError("Argument 'patterns' must be a dictionary")

        # Init dict for results
        result = {
            'results': []
        }

        # Save current offset from file beginning
        offset = 0

        # Buffer bytes between parts of file
        buffer = ''
        max_len = max(map(len, patterns))
        buffer_range = []
        for chunk_size, chunk in self.__read_next_chunk():
            if buffer:
                chunk = buffer + chunk
            for pattern in patterns:
                find_patterns = re.finditer(pattern, chunk)
                for find in find_patterns:
                    range_begin = offset + find.span()[0] // 2 - len(buffer) // 2
                    range_end = offset + find.span()[1] // 2 - len(buffer) // 2
                    if (range_begin, range_end) not in buffer_range:
                        buffer_range.append((range_begin, range_end))
                        result['results'].append({
                            'range': (range_begin, range_end),
                            'size': range_end - range_begin,
                            'pattern': pattern
                        })
            buffer = chunk[-max_len:]
            offset += chunk_size

        return result
