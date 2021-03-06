import errno
import json
import os
import random
import string
from distutils.dir_util import copy_tree, remove_tree
from random import randint

import numpy as np

from sample.service.utils.general_strategy import GeneralStrategy


class FolderHelper(GeneralStrategy):
    MIN_CHARS_STRINGS = 2
    MAX_CHARS_STRINGS = 20
    FILE_PARTITION_NAME = "file"
    BACKUPS_CACHE_FILE = "backs-history.txt"

    @staticmethod
    def generate_random_content(max_file_size):
        """  This method generates random content for a file with size:file_size. Basically iterates until the max size is
             reached. Therefore, returns a list of random generated ascii_letters lines.
        """
        lines = []
        current_size = 0
        while current_size < max_file_size:
            possible_total_size = FolderHelper.MAX_CHARS_STRINGS + current_size
            line_max_size = randint(FolderHelper.MIN_CHARS_STRINGS, FolderHelper.MAX_CHARS_STRINGS) \
                if possible_total_size <= max_file_size else max_file_size - current_size
            file_line = ''.join(random.choice(string.ascii_letters) for _ in range(line_max_size))
            current_size += len(file_line)
            lines.append(file_line)
        return lines

    @staticmethod
    def save_data_to_file(lines, output_path):
        """  This method writes a list of lines in a given file.
        """
        # TODO: replace validation for easier function in python 3
        if not os.path.exists(os.path.dirname(output_path)):
            try:
                os.makedirs(os.path.dirname(output_path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        new_file = open(output_path, 'w')
        new_file.writelines(["%s\n" % line for line in lines])
        new_file.close()

    @staticmethod
    def partitions_size(max_size_folder, max_size_file):
        """  This method encapsulates logic to ceil the number of partitions = (max_size_folder / max_size_file).
        """
        return int(np.ceil(max_size_folder / float(max_size_file)))

    @staticmethod
    def path_name(path_str):
        if len(path_str) > 5 and ('/' in path_str):
            return path_str.rsplit('/', 1)[-1]
        else:
            return path_str

    def partition(self, max_size_file, max_size_folder, folder_path, folder_name, init_index=0):
        """  This method creates a file with random content per partition and add that to dictionary using as key:
             {folder_name + index}: this will be used to find any partition with cost O(1).
             Finally, returns the dictionary of partitions as dic(key, (path, size))
             init_index: index to start partitions indexes from, in case of repartition it should be:
              the maximum dictionary index + 1.
        """
        current_space_folder = 0
        partition_dict = {}
        number_partitions = FolderHelper.partitions_size(max_size_folder, max_size_file)
        for i in range(0, number_partitions):
            free_space = max_size_folder - current_space_folder
            size_content = max_size_file if free_space > max_size_file else free_space
            file_index_name = str(i + 1 + init_index)
            partition_content = FolderHelper.generate_random_content(size_content)
            out_put_path = "{}{}{}".format(folder_path, FolderHelper.FILE_PARTITION_NAME, file_index_name)
            FolderHelper.save_data_to_file(partition_content, out_put_path)
            partition_dict[folder_name + file_index_name] = (out_put_path, size_content)
            current_space_folder += size_content
            del partition_content[:]
        return partition_dict

    def repartition(self, max_size_file, max_size_folder, folder_path, folder_name, added_bytes, current_partitions):
        """  This method modifies the chunk in a folder. First of all add bytes the the reminded space in the last
            partition and finally the generates new partitions with reminded bytes
        """
        # Balancing the smallest partition
        last_partition_key_str = folder_name + str(len(current_partitions))
        size_smallest_partition = current_partitions[last_partition_key_str][1]
        space_in_smallest_partition = max_size_file - size_smallest_partition
        difference_bytes = added_bytes - space_in_smallest_partition
        bytes_reminded = space_in_smallest_partition if difference_bytes > 0 else added_bytes
        out_put_path = "{}{}{}".format(folder_path, FolderHelper.FILE_PARTITION_NAME, str(len(current_partitions)))
        reminded_content = FolderHelper.generate_random_content(bytes_reminded)
        current_partitions[last_partition_key_str] = (out_put_path, size_smallest_partition + bytes_reminded)
        FolderHelper.save_data_to_file(reminded_content, out_put_path)

        # Creating new partitions
        new_partitions = {}
        if bytes_reminded > 0:
            new_partitions = self.partition(max_size_file, bytes_reminded, folder_path, folder_name,
                                            len(current_partitions))
        current_partitions.update(new_partitions)
        return current_partitions

    @staticmethod
    def map_list_to_dic(input_list):
        return dict((i + 1, value) for i, value in enumerate(input_list))

    def backup_folder(self, input_folder, output_folder):
        """  This method calls the distutils.dir_util method. This method moves a folder to an output path
             Regardless of whether the folder already exists or not
        """
        copy_tree(input_folder, output_folder)

    @staticmethod
    def remove_folder(folder_name):
        remove_tree(folder_name)

    @staticmethod
    def append_to_back_up_dictionary(new_back_data):
        with open(FolderHelper.BACKUPS_CACHE_FILE, 'a') as f:
            json.dump(new_back_data, f)
            f.write(os.linesep)

    @staticmethod
    def save_ds_as_json(ds_file, ds_name):
        with open(ds_name, 'w') as f:
            json.dump(ds_file, f)

    @staticmethod
    def read_from_json(file_name):
        with open(file_name) as json_data:
            data = json.load(json_data)
        return data
