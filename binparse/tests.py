import unittest
from binparse.binary_parse import BinaryParse


class TestBinaryParse(unittest.TestCase):
    """This class provide tests for methods of BinaryParse"""

    def setUp(self) -> None:
        """Set fixtures for tests"""

        self.bin_parse = BinaryParse('./binary_parse.py')

    def test_file_not_found(self):
        """Test creation object with missing file"""

        with self.assertRaises(FileNotFoundError):
            BinaryParse('fail_file.zip')


if __name__ == '__main__':
    unittest.main()