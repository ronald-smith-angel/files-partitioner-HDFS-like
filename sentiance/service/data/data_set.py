from sentiance.service.utils.file_utils import FileUtils


class DataSet(object):
    def __init__(self, name, path, folder_list=None):
        self.name = name
        self.folder_list = folder_list
        self.path = path

    def save_all(self):
        for folder in self.folder_list:
            for key, value in folder.partitions.items():
                FileUtils.save_data_to_file(value, "file" + key)
