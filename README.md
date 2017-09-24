# FILES PARTITIONER #

This project has some functions to repartion files in disk in chunks using a couple of approaches:

### 1-Core approach ###

This is the general approach totally implemented and validating using the test in: 

```sentiance.service.FolderTest```

This approach basically manages the Master DataSet Information as json serialized information in disk.

Is important to note that this json does not contain the files bytes but contains a dictionary with the folders and partitions paths and metadata.

In the Partitioner class you could find ```MAX_DISK_ALLOCATION``` that is maximum allocated value for all the values in disk. 

If the information becomes larger and does not match ```MAX_DISK_ALLOCATION``` the program will take the parallel strategy (not implemented yet).

### Parallel Strategy ###

As Suggestions if the information becomes larger we could change:


# Space Usage:
* Use a compression algorithm to reduce the size of information in disk. Example: lz4
* Explore a memory-disk allocation strategy using memory when is possible and then sending data to disk.
* Use a serialized method better than json. Examples: kryo and avro.
# Data Storage:
* Use a distributed file system.
	- Use s3 if you need eventually consistency.
	- Use hdfs if you need consistency.
	- Create your own distributed file system.
* Use the api in s3 or hdfs to create backups safely.
# Data processing:
* Process data in parallel reading from a distributed file system (1 partition - 1 slot)
	- Use spark or MR to process data in batch.
	- Use a custom python library to process data in parallel: python multiprocessing lib.




### How do I get set up? ###

* Run Unit Test: 

	```py folder_test.py```

* Run Files Generator

	```py data_generation.py  {path_ds} {max_value_file} {str_folders}```

* Run Files Update:
	
	```py data_update.py  {path_ds} {str_folders}```
	
* Run folder backup

	```py data_back_up.py {input_folder} {output_folder}```

