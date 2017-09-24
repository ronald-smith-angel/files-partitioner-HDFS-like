from abc import ABCMeta, abstractmethod


class GeneralStrategy(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def partition(self, max_size_file, max_size_folder, folder_path, folder_name, init_index=0):
        pass

    @abstractmethod
    def repartition(self, max_size_file, max_size_folder, folder_path, folder_name, added_bytes, current_partitions):
        pass

    @abstractmethod
    def backup_folder(self, input_folder, output_folder):
        pass
