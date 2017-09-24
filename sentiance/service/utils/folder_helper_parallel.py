from sentiance.service.utils.general_strategy import GeneralStrategy
from multiprocessing import Process
import boto
import boto.s3.connection


class FolderHelperParallel(GeneralStrategy):

    """
    Class that defines a strategy to process files using (spark / MR/ multiprocessing lib) in parallel using a distributed file system  i
    """

    #TODO: explore memory mapping and cache
    def partition(self, max_size_file, max_size_folder, folder_path, folder_name, init_index=0):
        #TODO: Use s3/HDFS or your own distributed file system in cluster  depending on required consistency model. see: s3guard-s3-consistency
        pass



    def repartition(self, max_size_file, max_size_folder, folder_path, folder_name, added_bytes, current_partitions):
        pass



    def backup_folder(self, input_folder, output_folder):
        #TODO: move data from side to side using spark/MR/multiprocessing lib or calling the file system API backup method in case of s3/HDFS
        pass