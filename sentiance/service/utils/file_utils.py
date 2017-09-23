import os
import errno
import string
import random
import datetime
import json
from random import randint
from distutils.dir_util import copy_tree,remove_tree


class FileUtils(object):
    BACK_DICT_PATH = "test-dictionary.json"
    MIN_CHARS_STRINGS = 2
    MAX_CHARS_STRINGS = 20
    FILE_PARTITION_NAME = "file"

    @staticmethod
    def generate_random_content(size, min_chars, max_chars):
        lines = []
        current_size = 0
        while current_size < size:
            possible_total_size = max_chars + current_size
            if possible_total_size <= size:
                range_val = randint(min_chars, max_chars)
            else:
                range_val = size - current_size
            file_line = ''.join(random.choice(string.ascii_letters) for _ in range(range_val))
            current_size += len(file_line)
            lines.append(file_line)
        return lines

    @staticmethod
    def save_data_to_file(lines, output_path):
        if not os.path.exists(os.path.dirname(output_path)):
            try:
                os.makedirs(os.path.dirname(output_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        new_file = open(output_path, 'w')
        new_file.writelines(["%s\n" % line for line in lines])
        new_file.close()

    @staticmethod
    def get_file_chunks(number_partitions, max_size_file, max_size_folder, folder_path, folder_name):
        current_space_folder = 0
        partition_dict = {}
        for i in range(0, number_partitions - 1):
            free_space = max_size_folder - current_space_folder
            if free_space > max_size_file:
                size_content = max_size_file
            else:
                size_content = free_space
            partition_content = FileUtils.generate_random_content(size_content, FileUtils.MIN_CHARS_STRINGS, FileUtils.MIN_CHARS_STRINGS)
            out_put_path = folder_path + FileUtils.FILE_PARTITION_NAME + str(i)
            FileUtils.save_data_to_file(partition_content, out_put_path)
            partition_dict[folder_name + str(i)] = out_put_path
            del partition_content[:]
        return partition_dict

    @staticmethod
    def map_list_to_dic(input_list):
        return dict((i + 1, value) for i, value in enumerate(input_list))

    @staticmethod
    def backup_folder(input_folder, output_folder):
        copy_tree(input_folder, output_folder)

    @staticmethod
    def remove_folder(folder_name):
        current_ts = datetime.datetime.now()
        backup_folder = '{}back{}'.format(folder_name, current_ts)
        copy_tree(folder_name, backup_folder)
        FileUtils.append_to_back_up_dictionary(dict(folder_name, (current_ts, backup_folder)))
        remove_tree(folder_name)

    @staticmethod
    def append_to_back_up_dictionary(new_back_data):
        with open(FileUtils.BACK_DICT_PATH, 'a') as f:
            json.dump(new_back_data, f)
            f.write(os.linesep)
