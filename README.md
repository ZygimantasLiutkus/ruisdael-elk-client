# ruisdael-elk-client



## Getting started

To install this software you need to run the playbook.yaml with ansible targeting the host on which you wish to install the software.
You need root access on the target machine to execute the playbook successfully.

First you need to make sure you have the right .env.template.j2 file, this should have been provided to you.
You will need to configure the file with corresponding information in corresponding fields.
Next you need to add the hostname of the target machine to the inventory.yaml file

After that, you can run the playbook with the following command
```shell
ansible-playbook -i inventory.yaml playbook.yaml -K
```
To check if the playbook worked, you can ssh into the target machine and run this command
```shell
sudo systemctl status collector
```
This should say running.

## Usage

After the software is started/run, it will automatically begin to send data to the specified elasticsearch host.

By running the following command:

```shell
sudo journalctl -xeu collector
```

you will be able to see the end of the run report of the software.
If everything is working as intended you should be able to see the messages similar to:
```
{'_index': 'collector_[device-name]', '_id': '[some_id]', '_version': 1, 'result': 'created', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': [n], '_primary_term': 1}
```

## Contributing

To contribute to the software, you should be aware of what the files and modules contain.

The `main.py` module contains the index configuration and is responsible for the actual sending of data to the
Elasticsearch host. An index can be reset (deleted if it exists) by uncommenting line 21. The `mappings` dictionary contains
the properties that you want the index to have, for e.g., now it is configured to recognize the location property
among the sent data. Lastly, the `time.sleep(n)` makes the timeout between sending be n seconds.

The `elasticSearch.py` module creates the connection to Elasticsearch and an index. It also has a 
function which sends the given data to the Elasticsearch host.

The `collector.py` module contains the logic for the actual collection of monitored data. 
The `collect()` function creates a dictionary with the collected data, where mainly the [psutil
module](https://psutil.readthedocs.io/en/latest/) is used to monitor system statuses. If you 
want to add some more data to be monitored, simply add a variable declaration within the function
of what you want to be monitored and then append it to the dictionary (data variable) with whatever
key value (name) you choose. If the data is expected to not change, for example, location, you should
declare it in the constructor of the Collector class (the __init__ funciton) as `self.variable = x` and
then add it in the data dictionary with key of your choice and value `self.variable`.
