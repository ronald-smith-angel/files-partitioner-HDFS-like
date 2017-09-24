from sentiance.service.data.folder import Folder
from sentiance.service.data.data_set import DataSet
from sentiance.service.utils.general_processor import GeneralProcessor
from sentiance.service.utils.folder_helper import FolderHelper
from sentiance.service.utils.folder_helper_parallel import FolderHelperParallel

class Partitioner(object):

    MAX_DISK_ALLOCATION = 500000


    def __init__(self, data_sets_hash=None):
        self.data_sets_dict = data_sets_hash

    @staticmethod
    def generate_data_set(self, path, file_max_size_bytes, tuples_folders):
        ds_name = FolderHelper.path_name(path)
        data_set = DataSet(path)
        for path, max_size_folder_bytes in tuples_folders:
            folder_name =  FolderHelper.path_name(path)
            folder = Folder(file_max_size_bytes, path, max_size_folder_bytes, folder_name)
            #TODO: calculate total space used in disk - could be only iterate data_sets_dict sizes in folder
            if("1" < Partitioner.MAX_DISK_ALLOCATION):
                helper = FolderHelper()
            else:
                helper = FolderHelperParallel()
            folder_processor = GeneralProcessor(helper)
            folder_processor.partition(folder)
            data_set.folder_list[folder_name] = folder

        self.data_sets_dict[ds_name] = data_set
        return data_set

    @staticmethod
    def update_data_set(self, path, tuples_folders):
        ds_name =  FolderHelper.path_name(path)
        data_set = self.data_sets_dict[ds_name]
        for name, size in tuples_folders:
            folder = data_set.folder_list[name]
            helper = FolderHelper()
            folder_processor = GeneralProcessor(helper)
            folder_processor.repartition(folder, size)

    @staticmethod
    def back_up_folder(self, input_folder, output_folder):
        helper = FolderHelper()
        folder_processor = GeneralProcessor(helper)
        folder_processor.backup_folder(input_folder, output_folder)




