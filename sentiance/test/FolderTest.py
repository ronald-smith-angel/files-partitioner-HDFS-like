import unittest
import numpy as np
from random import randint
from sentiance.service.utils.file_utils import FileUtils


class FolderTest(unittest.TestCase):
    MAX_SIZE_FILE = 500
    INPUT_FILE_NAME = 'init_test_file.txt'
    OUT_PUT_FILE_NAME = 'test-01.txt'
    GENERATED_FILE_SIZE = 5000

    def test_files_chunk(self):
        #input_file = open(FolderTest.INPUT_FILE_NAME, 'rb')
        #nput_data = input_file.read()

        path = "/c/Users/ronald/PycharmProjects/files-partitioner/uno/"
        name = "folder1"
        max_file = 200
        max_total = 1100
        number_partitions = int(np.ceil(max_total / float(max_file)))
        print(number_partitions)
        data_chunks = FileUtils.get_file_chunks(number_partitions, max_file,max_file, path, name)
        print(data_chunks)
        #partition_dic = FileUtils.map_list_to_dic(data_chunks)
        #number_chunks = len(partition_dic)
        #self.assertEqual(number_chunks, np.ceil(size_input_data / float(FolderTest.MAX_SIZE_FILE)))
        #partition_key = randint(1, number_chunks - 1)
        #size_random_partition = len(partition_dic[partition_key])
        #self.assertEqual(size_random_partition, FolderTest.MAX_SIZE_FILE)

    #def test_random_file(self):
    #    FileUtils.generate_random_file(FolderTest.GENERATED_FILE_SIZE, FolderTest.OUT_PUT_FILE_NAME, 2, 20)
    #    random_file_data = open(FolderTest.OUT_PUT_FILE_NAME, 'rb').read()
    #    self.assertEqual(len(random_file_data), FolderTest.GENERATED_FILE_SIZE)

if __name__ == '__main__':
    unittest.main()








