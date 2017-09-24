class Folder(object):
    def __init__(self, max_size_file, path, total_size, name, partitions=None):
        if partitions is None:
            partitions = {}
        self.max_size_file = max_size_file
        self.path = path
        self.total_size = total_size
        self.name = name
        self.partitions = partitions








