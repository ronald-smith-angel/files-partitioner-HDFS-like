class DataSet(object):
    def __init__(self, path, folder_list=None):
        if folder_list is None:
            folder_list = {}
        self.path = path
        self.folder_list = folder_list

