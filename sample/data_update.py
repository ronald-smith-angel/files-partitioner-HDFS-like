import sys
from sample.service.partitioner import Partitioner

# Parsing Params
program_args = sys.argv
path = program_args[1]
str_partitions = program_args[2]

BYTES_MEGA_BYTE = 1000000

# Conversions in List
list_folders = str_partitions.split(",")
iter_list_folders = iter(list_folders)
list_tuples_folder = zip(iter_list_folders, iter_list_folders)
list_tuples_folder_bytes = [(val[0], int(val[1]) * BYTES_MEGA_BYTE) for val in list_tuples_folder]

# Calling Partitioner
Partitioner.update_data_set(path, list_tuples_folder_bytes)
