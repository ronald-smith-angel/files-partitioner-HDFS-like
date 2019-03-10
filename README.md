# FILES PARTITIONER #

This project has some functions to repartion files in chunks using randomly generated data. This an example created to 
understand locally the HDFS (first version) version main concepts: block size, metadata store and repartition. 

### Core approach ###

This is the general approach totally implemented and validated using the test in: 

```sentiance.service.FolderTest```

This approach basically manages the Master DataSet Information as json serialized information in disk.

Is important to note that this json does not contain the files bytes but contains a dictionary with the folders and partitions paths and metadata.

In the Partitioner class you could find ```MAX_DISK_ALLOCATION``` that is maximum allocated value for all the values in disk. 

If the information becomes larger and does not match ```MAX_DISK_ALLOCATION``` the program will take the parallel strategy (not implemented yet).



### How do I get set up? ###

* Run Unit Test: 

	```py folder_test.py```

* Run Files Generator

	```py data_generation.py  {path_ds} {max_value_file} {str_folders}```

* Run Files Update:
	
	```py data_update.py  {path_ds} {str_folders}```
	
* Run folder backup

	```py data_back_up.py {input_folder} {output_folder}```

