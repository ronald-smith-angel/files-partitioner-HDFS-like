from sentiance.service.utils.file_utils import FileUtils


class Folder(object):
    def __init__(self, max_size_file, path, init_data, total_size, partitions=None):
        if partitions is None:
            partitions = {}
        self.max_size_file = max_size_file
        self.path = path
        self.init_data = init_data
        self.partitions = partitions
        self.total_size = total_size

    def partition(self):
        self.partitions = self.get_data_partitions(self.init_data, 0)
        return self.partitions

    def repartition(self, new_data):
        new_data_size = len(self.init_data)
        space_in_smallest_partition = self.max_size_file - len(self.partitions[self.partitions_size])
        input_smallest_partition = new_data[0: space_in_smallest_partition - 1]
        self.partitions[self.partitions_size() + 1] = input_smallest_partition
        new_partitions = self.get_data_partitions(space_in_smallest_partition, new_data_size)
        self.partitions.update(new_partitions)
        return self.partitions

    def coalesce(self, new_data):
        self.partitions = {}
        FileUtils.remove_folder(self.path)
        self.partition(new_data)

    def partitions_size(self):
        len(self.partitions)

    def get_data_partitions(self, init_data, init_index):
        file_chunks = FileUtils.get_file_chunks(init_data, init_index, self.max_size_file)
        return FileUtils.map_list_to_dic(file_chunks)

    def flush(self):
        for index, data in self.partitions.items():
            file_pattern = "file{}"
            FileUtils.save_data_to_file(file_pattern.format(index), data)




