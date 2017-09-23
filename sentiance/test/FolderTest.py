import unittest
import numpy as np
from random import randint
from sentiance.service.utils.file_utils import FileUtils


class FolderTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(FolderTest, self).__init__(*args, **kwargs)

    def test_files_chunk(self):
        MAX_SIZE_FILE = 500
        input_file = open("init_test_file.txt", "rb")
        input_data = input_file.read()
        size_input_data = len(input_data)
        data_chunks = FileUtils.get_file_chunks(input_data, 0, MAX_SIZE_FILE)
        partition_dic = FileUtils.map_list_to_dic(data_chunks)
        number_chunks = len(partition_dic)
        self.assertEqual(number_chunks, np.ceil(size_input_data / MAX_SIZE_FILE))
        partition_key =  randint(1, number_chunks - 1)
        size_random_partition = len(partition_dic[partition_key])
        self.assertEqual(size_random_partition, MAX_SIZE_FILE)

        






