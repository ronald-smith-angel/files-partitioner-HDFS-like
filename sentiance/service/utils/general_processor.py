class GeneralProcessor(object):
    """
    Define the interface to be exposed to clients.
    Gets a Strategy object and execute methods depending on it.
    """

    def __init__(self, strategy):
        self._strategy = strategy

    def partition(self, folder):
        self._strategy.get_file_chunks(folder.max_size_file, folder.total_size, folder.path, folder.name)

    def repartition(self, folder, added_bytes):
        self._strategy.modify_file_chunks(folder.max_size_file,
                                           folder.total_size,
                                           folder.path,
                                           folder.name,
                                           added_bytes,
                                           folder.current_partitions)

    def backup_folder(self,input_folder, output_folder):
        self._strategy.backup_folder(input_folder, output_folder)


