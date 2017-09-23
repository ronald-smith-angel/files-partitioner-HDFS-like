from sentiance.service.data.folder import Folder
from sentiance.service.data.data_set import DataSet
from sentiance.service.utils.file_utils import FileUtils


class Partitioner(object):
    def __init__(self, data_sets_hash=None):
        self.data_sets_dict = data_sets_hash

    def generate_data_set(self, path, file_max_size, tuples_folders):
        data_set = DataSet(path)
        for name, size in tuples_folders:
            init_file = FileUtils.generate_random_file(size, 2, 20)
            folder = Folder(file_max_size, path + name, init_file)
            folder.partition()
            data_set.list_folders[name] = folder
        self.data_sets_dict[path] = data_set
        return data_set

    def update_data_set(self, data_set_name, tuples_folders):
        data_set = self.data_sets_dict[data_set_name]
        for name, size in tuples_folders:
            folder = data_set.folder_list[name]
            if size > folder.total_size:
                difference = size - folder.total_size
                init_file = FileUtils.generate_random_file(difference, 2, 20)
                folder.repartition(init_file.read())
            elif size < folder.total_size:
                init_file = FileUtils.generate_random_file(size, 2, 20)
                folder.coalesce(init_file)



