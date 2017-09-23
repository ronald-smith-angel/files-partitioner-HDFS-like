import os
import string
import random
import datetime
import json
from random import randint
from distutils.dir_util import copy_tree,remove_tree


class FileUtils(object):
    BACK_DICT_PATH = "test-dictionary.json"

    @staticmethod
    def generate_random_file(size, file_name, min_chars, max_chars):
        new_file = open(file_name, 'w')
        while os.path.getsize(file_name) < size:
            file_line = ''.join(random.choice(string.ascii_letters) for _ in range(randint(min_chars, max_chars)))
            new_file.write(file_line + '\n')
        data_file = new_file.read()
        new_file.close()
        return data_file

    @staticmethod
    def save_data_to_file(file_data, output_path):
        new_file = open(output_path, 'w')
        new_file.write(file_data)
        new_file.close()

    @staticmethod
    def get_file_chunks(init_data, init_index, max_size_file):
        return (init_data[i:i + max_size_file] for i in range(init_index, len(init_data), max_size_file))

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
