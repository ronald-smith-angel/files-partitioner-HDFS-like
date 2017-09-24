import abc
class GeneralStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def partition(self, max_size_file, max_size_folder, folder_path, folder_name, init_index=0):
        pass


    @abc.abstractmethod
    def repartition(self, max_size_file, max_size_folder, folder_path, folder_name, added_bytes, current_partitions):
        pass


    @abc.abstractmethod
    def backup_folder(self, input_folder, output_folder):
        pass
