import sys
from sample.service.partitioner import Partitioner

# Parsing Params
program_args = sys.argv
input_folder = program_args[1]
output_folder = program_args[2]

# Calling method to create backup
Partitioner.back_up_folder(input_folder, output_folder)