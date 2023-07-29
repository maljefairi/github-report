# tests/test_utils.py
import unittest
import os
from src.utils.utils import text_file_word_count

class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file_path = 'tests/test_file.txt'
        with open(cls.test_file_path, 'w') as file:
            file.write('This is a test file.')

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_file_path):
            os.remove(cls.test_file_path)

    def test_text_file_word_count(self):
        word_count = text_file_word_count(self.test_file_path)
        self.assertEqual(word_count, 5)
        
if __name__ == '__main__':
    unittest.main()