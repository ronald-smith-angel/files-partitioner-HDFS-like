import os
import unittest
from random import randint

from sample.service.utils.folder_helper import FolderHelper


class FolderTest(unittest.TestCase):
    # Config with Default and Expected values
    # TODO: Add a Mock frame and if is possible a BDD (cucumber like) framework to Mock connections with fs & variables.
    # TODO: Add methods for failing Scenarios
    MAX_SIZE_FILE = 500
    MAX_SIZE_TOTAL_FOLDER = 2700
    ADDED_BYTES_VALUE = 600
    INPUT_FILE_NAME = './test01/'
    INPUT_BK_FILE_NAME = '/test-dir/'
    OUT_PUT_BK_FILE = '/test-dir-bk/'
    NAME_INPUT_FOLDER = 'test01'
    EXPECTED_ORIGINAL_LAST_SIZE = 200
    EXPECTED_MODIFIED_LAST_SIZE = 300
    original_data_chunks = {}

    @classmethod
    def setUpClass(cls):
        current_directory = os.getcwd()
        content_file1 = FolderHelper.generate_random_content(3)
        content_file2 = FolderHelper.generate_random_content(3)
        FolderHelper.save_data_to_file(content_file1, current_directory + FolderTest.INPUT_BK_FILE_NAME + "file1.text")
        FolderHelper.save_data_to_file(content_file2, current_directory + FolderTest.INPUT_BK_FILE_NAME + "file2.text")

    def test_files_chunk(self):
        """  This method tests the files creation process
        """
        # Testing number of chunks created
        folder_helper = FolderHelper()
        data_chunks = folder_helper.partition(FolderTest.MAX_SIZE_FILE,
                                              FolderTest.MAX_SIZE_TOTAL_FOLDER,
                                              FolderTest.INPUT_FILE_NAME,
                                              FolderTest.NAME_INPUT_FOLDER)
        number_chunks = len(data_chunks)
        self.assertEqual(number_chunks, FolderHelper.partitions_size(FolderTest.MAX_SIZE_TOTAL_FOLDER,

                                                                     FolderTest.MAX_SIZE_FILE))
        # Validating size of intermediary key space
        random_key = randint(1, number_chunks - 1)
        partition_key = FolderTest.NAME_INPUT_FOLDER + str(random_key)
        size_random_partition = data_chunks[partition_key][1]
        self.assertEqual(size_random_partition, FolderTest.MAX_SIZE_FILE)
        FolderTest.original_data_chunks = data_chunks

        # Validating size of last key space
        self.assertEqual(data_chunks[FolderTest.NAME_INPUT_FOLDER + str(number_chunks)][1],
                         FolderTest.EXPECTED_ORIGINAL_LAST_SIZE)

    def test_files_update(self):
        """  This method test the files update process.
        """
        # Modifying a folder and testing number of partitions
        folder_helper = FolderHelper()
        folder_modified_size = FolderTest.MAX_SIZE_TOTAL_FOLDER + FolderTest.ADDED_BYTES_VALUE
        new_number_chunks = FolderHelper.partitions_size(folder_modified_size, FolderTest.MAX_SIZE_FILE)

        modified_data_chunks = folder_helper.repartition(FolderTest.MAX_SIZE_FILE,
                                                         FolderTest.MAX_SIZE_TOTAL_FOLDER,
                                                         FolderTest.INPUT_FILE_NAME,
                                                         FolderTest.NAME_INPUT_FOLDER,
                                                         FolderTest.ADDED_BYTES_VALUE,
                                                         FolderTest.original_data_chunks)
        self.assertEqual(new_number_chunks, len(modified_data_chunks))

        # Validating size of intermediary key space
        random_key_new = randint(1, new_number_chunks - 1)
        partition_key_new = FolderTest.NAME_INPUT_FOLDER + str(random_key_new)
        size_random_partition_new = modified_data_chunks[partition_key_new][1]
        self.assertEqual(size_random_partition_new, FolderTest.MAX_SIZE_FILE)

        # Validating size of last key space
        self.assertEqual(modified_data_chunks[FolderTest.NAME_INPUT_FOLDER + str(new_number_chunks)][1],
                         FolderTest.EXPECTED_MODIFIED_LAST_SIZE)

    def test_back_up(self):
        """  This method test the backup creation process
        """
        # Validating backup creation
        folder_helper = FolderHelper()
        current_directory = os.getcwd()

        input_dir = current_directory + FolderTest.INPUT_BK_FILE_NAME
        output_dir = current_directory + FolderTest.OUT_PUT_BK_FILE

        folder_helper.backup_folder(input_dir, output_dir)
        # Getting sure there are not issues with existing folder
        folder_helper.backup_folder(input_dir, output_dir)
        self.assertEqual(os.path.getsize(input_dir), os.path.getsize(output_dir))

    @classmethod
    def tearDownClass(cls):
        current_directory = os.getcwd()
        FolderHelper.remove_folder(current_directory + FolderTest.INPUT_BK_FILE_NAME)
        FolderHelper.remove_folder(current_directory + FolderTest.OUT_PUT_BK_FILE)
        FolderHelper.remove_folder(current_directory + FolderTest.INPUT_FILE_NAME.replace(".", ""))


if __name__ == '__main__':
    unittest.main()
