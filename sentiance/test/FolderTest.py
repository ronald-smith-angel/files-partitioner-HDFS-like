import unittest
import numpy as np
from random import randint
from sentiance.service.utils.file_utils import FileUtils


class FolderTest(unittest.TestCase):

    def test_files_chunk(self):
        MAX_SIZE_FILE = 500
        INPUT_FILE_NAME = 'init_test_file.txt'
        input_file = open(INPUT_FILE_NAME, 'rb')
        input_data = input_file.read()
        size_input_data = len(input_data)
        data_chunks = FileUtils.get_file_chunks(input_data, 0, MAX_SIZE_FILE)
        partition_dic = FileUtils.map_list_to_dic(data_chunks)
        number_chunks = len(partition_dic)
        self.assertEqual(number_chunks, np.ceil(size_input_data / MAX_SIZE_FILE))
        partition_key =  randint(1, number_chunks - 1)
        size_random_partition = len(partition_dic[partition_key])
        self.assertEqual(size_random_partition, MAX_SIZE_FILE)

    def random_file(self):
        data_file =  FileUtils.generate_random_file(50000, "test-01.txt", 2, 20)
        self.assertGreater(10,20)
        print(data_file)

if __name__ == '__main__':
    unittest.main()








