import unittest
import os
from binparse.binary_parse import BinaryParse


class TestBinaryParse(unittest.TestCase):
    """This class provide tests for methods of BinaryParse"""

    def setUp(self) -> None:
        """Set fixtures for tests"""
        # Change current dir to get test file 'test.zip'
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = './test.zip'
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
        """Test find one pattern in entire file"""
        self.bin_parse = BinaryParse(self.file_path, 1)

        result = self.bin_parse.find_pattern({
            '504B0304': 'PK..',
        })

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['results'][0]['range'], (0, 4))
        self.assertEqual(result['results'][0]['size'], 4)
        self.assertEqual(result['results'][0]['pattern'], '504B0304')

    def test_find_patterns_repeat(self):
        """Test find repeat patterns in entire file"""
        self.bin_parse = BinaryParse(self.file_path, 1)

        result = self.bin_parse.find_pattern({
            '63A1': 'c.',
        })

        ranges = [(40, 42), (44, 46), (48, 50), (163, 165), (167, 169), (171, 173)]
        self.assertEqual(len(result['results']), 6)
        for i in range(6):
            self.assertEqual(result['results'][i]['range'], ranges[i])
            self.assertEqual(result['results'][i]['size'], 2)
            self.assertEqual(result['results'][i]['pattern'], '63A1')

    def test_find_patterns_split_pattern(self):
        """Test find one pattern in split file.

        Search pattern is split to different file parts
        """
        self.bin_parse = BinaryParse(self.file_path, 5)

        result = self.bin_parse.find_pattern({
            'B4FCA2DCC492': '......'
        })

        check_data = {
            'B4FCA2DCC492': (80, 86),
        }
        count = 0

        self.assertEqual(len(result['results']), 1)
        for pattern, range in check_data.items():
            self.assertEqual(result['results'][count]['range'], range)
            self.assertEqual(result['results'][count]['size'], 6)
            self.assertEqual(result['results'][count]['pattern'], pattern)
            count += 1

    def test_find_patterns_split_two_patterns(self):
        """Test find two pattern in split file.

        Search two patterns neighboring in different file parts
        """
        self.bin_parse = BinaryParse(self.file_path, 5)

        result = self.bin_parse.find_pattern({
            'FCA2DC': '...',
            'C492CC': '...'
        })

        check_data = {
            'FCA2DC': (81, 84),
            'C492CC': (84, 87)
        }
        count = 0

        self.assertEqual(len(result['results']), 2)
        for pattern, range in check_data.items():
            self.assertEqual(result['results'][count]['range'], range)
            self.assertEqual(result['results'][count]['size'], 3)
            self.assertEqual(result['results'][count]['pattern'], pattern)
            count += 1

    def test_find_repeat_sequences(self):
        """Test find all repeat sequences with length 3."""
        self.bin_parse = BinaryParse(self.file_path, 5)

        result = self.bin_parse.find_repeat_sequences(5)

        check_data = {
            '0000000000000000': {
                'range': (13, 21),
                'size': 8
            },
            '000000000000000000': {
                'range': (137, 146),
                'size': 9
            },
            '0000000000': {
                'range': (206, 211),
                'size': 5
            }
        }
        count = 0

        self.assertEqual(len(result['results']), 3)
        for pattern, values in check_data.items():
            self.assertEqual(result['results'][count]['range'], values['range'])
            self.assertEqual(result['results'][count]['size'], values['size'])
            self.assertEqual(result['results'][count]['pattern'], pattern)
            count += 1

    def test_find_zip_archives(self):
        """Testing of searching for all zip archives in file"""

        self.bin_parse = BinaryParse(self.file_path, 5)

        result = self.bin_parse.find_zip_archives()

        check_data = {
            '504B0304': {
                'range': (0, 4),
                'size': 4,
            }
        }
        count = 0

        self.assertEqual(len(result['results']), 1)
        for pattern, values in check_data.items():
            self.assertEqual(result['results'][count]['range'], values['range'])
            self.assertEqual(result['results'][count]['size'], values['size'])
            self.assertEqual(result['results'][count]['pattern'], pattern)
            count += 1


if __name__ == '__main__':
    unittest.main()
