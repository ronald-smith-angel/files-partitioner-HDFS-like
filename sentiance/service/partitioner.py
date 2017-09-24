import os

import jsonpickle

from sentiance.service.data.data_set import DataSet
from sentiance.service.data.folder import Folder
from sentiance.service.utils.folder_helper import FolderHelper
from sentiance.service.utils.folder_helper_parallel import FolderHelperParallel
from sentiance.service.utils.general_processor import GeneralProcessor


class Partitioner(object):
    """  This class is a General interface that coordinates calls to helper functions and
         final storage of master DataSet files.
    """
    MAX_DISK_ALLOCATION = 500000
    MASTER_DS_FORMAT = ".ds"

    def __init__(self, data_sets_hash=None):
        if data_sets_hash is None:
            data_sets_hash = {}
        self.data_sets_dict = data_sets_hash

    @staticmethod
    def generate_data_set(path_ds, file_max_size_bytes, tuples_folders):
        """  This method calls a strategy to create file chunks between parallel and regular helper.
             In addition, Serializes the df information using json to disk. The ds information does not contain
             the bytes information (that in only 1 computer does not match in memory allocation)
             but the reference for the path in disk where the file was stored. The info is serialized  as a json
             of folders dictionary that contains the partitions info as a dictionary (key, (path, size))
        """
        ds_name = FolderHelper.path_name(path_ds)
        ds_file_name = path_ds + "/" + ds_name + Partitioner.MASTER_DS_FORMAT
        data_set = DataSet(path_ds)
        for path, max_size_folder_bytes in tuples_folders:
            str_folder_path = path_ds + path
            # TODO: Create hash or UUID(MD5) as folder name | for now: str_folder_path
            folder_name = str_folder_path
            folder = Folder(file_max_size_bytes, str_folder_path, max_size_folder_bytes, folder_name)
            # TODO: calculate total space used in disk - could be only iterate data_sets_dict sizes in folder
            if 1 < Partitioner.MAX_DISK_ALLOCATION:
                helper = FolderHelper()
            else:
                helper = FolderHelperParallel()

            folder_processor = GeneralProcessor(helper)
            folder.partitions = folder_processor.partition(folder)
            data_set.folder_list[folder.name] = folder

        json_ds = jsonpickle.encode(data_set)
        FolderHelper.save_ds_as_json(json_ds, ds_file_name)
        return data_set

    @staticmethod
    def update_data_set(path_ds, tuples_folders):
        """  This method opens the json serialized file for a ds and call the helper to re-partition the folders.
             In addition, update the json serialized file with latest information.
        """
        ds_name = FolderHelper.path_name(path_ds)
        ds_json_file_path = path_ds + "/" + ds_name + Partitioner.MASTER_DS_FORMAT
        if os.path.exists(ds_json_file_path):
            data_set = jsonpickle.decode(FolderHelper.read_from_json(ds_json_file_path))
        else:
            print("No such file '{}'".format(ds_json_file_path))
            return
        for name, size in tuples_folders:
            folder = data_set.folder_list[path_ds + name]
            helper = FolderHelper()
            folder_processor = GeneralProcessor(helper)
            folder.partitions = folder_processor.repartition(folder, size)
        json_ds = jsonpickle.encode(data_set)
        FolderHelper.save_ds_as_json(json_ds, ds_json_file_path)
        return data_set

    @staticmethod
    def back_up_folder(input_folder, output_folder):
        """  This method calls the helper to create a backup.
        """
        helper = FolderHelper()
        folder_processor = GeneralProcessor(helper)
        folder_processor.backup_folder(input_folder, output_folder)
