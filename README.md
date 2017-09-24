# README #

This project has some functions to repartion files in disk in chunks using a couple of approaches:

### 1 Core approach? ###

This is the general approcha totally implemented and validating using the test in: *sentiance.service.FolderTest*.

This approach basically manages the Master Data Frame Information as json serialized information in disk. Is important
to note that this json does not contain the files bytes but contains a dictionary with the folders and partitions paths
and metadata.

In the Partitioner class you could find MAX_DISK_ALLOCATION that is maximum allocated value for all the values in disk. 
If the information becomes larger and does not match MAX_DISK_ALLOCATION the program will take the parallel strategy 
(not implemented yet).

As Sugesstions if the information becomes larger we could:

Space Usage:
* Use a compression algorith to reduce the size of information in disk. Example: lz4
* Explore a memory-disk allocation strategy using memory when is possible and then sending data to disk.
* Use a serialized method better than json. Examples: kryo and avro.
Data Storage:
*Use a distruited file system.
	-Use s3 if you need eventually consistency.
	-Use hdfs if you need consistency.
	-Create your own distribuited file system.
*Use the api in s3 or hdfs to create backups safetely.
Data processing:
Process data in parallel reading from a distribuited file system (1 partition - 1 slot)
	*Use spark or MR to process data in batch.
	*Use a custom python library to process data in parallel: from multiprocessing import Process








### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact