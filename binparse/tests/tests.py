import unittest
import os
from binparse.binary_parse import BinaryParse


class TestBinaryParse(unittest.TestCase):
    """This class provide tests for methods of BinaryParse"""

    def setUp(self) -> None:
        """Set fixtures for tests"""
        self.file_path = './tests/test.zip'
        self.file_size = os.path.getsize(self.file_path)

    def test_file_not_found(self):
        """Test creation object with missing file"""
        self.bin_parse = BinaryParse(self.file_path)
        with self.assertRaises(FileNotFoundError):
            BinaryParse('fail_file.zip')

    def test_init_object(self):
        """Test initialization object"""
        self.bin_parse = BinaryParse(self.file_path)
        # Init path to file
        self.assertEqual(self.file_path, self.bin_parse.get_file_path())

        # Init file size
        self.assertEqual(self.file_size, self.bin_parse.get_file_size())

        # Init split parts to read file
        self.assertIsInstance(self.bin_parse.get_chunks(), list)

        # Check that file was split correct
        self.assertEqual(self.file_size, sum(self.bin_parse.get_chunks()))

    def test_find_patterns_arguments_type(self):
        """Test that argument is a dict"""
        self.bin_parse = BinaryParse(self.file_path)
        with self.assertRaises(TypeError):
            self.bin_parse.find_pattern(['504B0304', 'E757B8E2'])

    def test_find_patterns_return_type(self):
        """Test that func find_patterns return correct dict"""
        self.bin_parse = BinaryParse(self.file_path)
        result = self.bin_parse.find_pattern({
            '42F0FBB21BE9': 'test1',
            '504B0304': 'zip',
        })
        self.assertIsInstance(result, dict)
        self.assertIn('results', result)
        self.assertIsInstance(result['results'], list)

    def test_find_patterns_one(self):
        """Test find one pattern in file without splits"""
        self.bin_parse = BinaryParse(self.file_path, 1)

        result = self.bin_parse.find_pattern({
            '504B0304': 'PK..',
        })

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['results'][0]['range'], "(0, 4)")
        self.assertEqual(result['results'][0]['size'], 4)
        self.assertEqual(result['results'][0]['pattern'], '504B0304')

    def test_find_patterns_repeat(self):
        """Test find repeat patterns in file without splits"""
        self.bin_parse = BinaryParse(self.file_path, 1)

        result = self.bin_parse.find_pattern({
            '63A1': 'c.',
        })

        ranges = ["(40, 42)", "(44, 46)", "(48, 50)", "(163, 165)", "(167, 169)", "(171, 173)"]
        self.assertEqual(len(result['results']), 6)
        for i in range(6):
            self.assertEqual(result['results'][i]['range'], ranges[i])
            self.assertEqual(result['results'][i]['size'], 2)
            self.assertEqual(result['results'][i]['pattern'], '63A1')


if __name__ == '__main__':
    unittest.main()