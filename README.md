# ruisdael-elk-client

This git repository contains software that collects data form different nodes and sends it to a preconfigured elastic server.
To install this software, there is an installation script and an uninstallation script. 
If you don't want to use our software, you can also use metricbeat, for which there also is an installation and uninstallation script
These 2 programs are independent of each-other.

Once the software is installed on a new instrument with correct configurations, it 
can be polled from Elasticsearch to be shown in the Kibana and will automatically 
appear in the [web UI created to work together with this software](https://gitlab.ewi.tudelft.nl/cse2000-software-project/2022-2023-q4/cluster-12/ruisdael-automatic-network-monitoring-system/ruisdael-elk-client).

## Installing custom collector

This directory includes a collector that sends data to elastic search. This chapter will go into more detail on how to install it.
Firstly it covers the automatic installations via ansible, and the second part has a manual installation.

For the collector to run properly, you need to add a file with some node specific information at /etc/ruisdael_instrument_details.yml 
An example of such a file can be found below. This file is used to send extra metadata to the elasticserver
```yaml
instrument_name: DAVIS-CitG
latitude: 4.375167
longitude: 51.998906 
elevation: "5 m"
location: "CITG Stevinweg"
instrument_type: "Weather station"
```

### Automatic installation

To install this software you need to run the playbook.yaml with ansible targeting the host on which you wish to install the software.
You need root access on the target machine to execute the playbook successfully. 
The playbook clones this repository and changes some settings on the target device. 

First you need to make sure you have the right inventory file, there is a template in template_inventory.yaml. 
You will need to configure the file with corresponding information in corresponding fields.
The certificate can be retrieved via running this command on the elasticsearch server
```shell
sudo openssl x509 -fingerprint -sha256 -in /etc/elasticsearch/certs/http_ca.crt
```

Next you need to add the hostname of the target machine to the inventory.yaml file under the hosts section.
This hosts section should look something like this:
```yaml
all:
  hosts:
    ansible_hosts: [[hostname inside your ~/.ssh/config file]]
    ansible_user: [[username that will execute the commands in the playbook]]
```
You can add multiple machines to simultaneously install the collector on multiple notes

After that, you can run the playbook with the following command
```shell
ansible-playbook -i inventory.yaml playbook.yaml -K
```
You can add --limit to chose on which of the hosts the ansible will be executed. 
The -K means that you need to provide a password to the account that will execute the playbook on the nodes. You are prompted for this after you start the playbook

To check if the playbook worked, you can ssh into the target machine and run this command
```shell
sudo systemctl status collector
```
This should say running.

To uninstall the software you can run the following ansible, you need to change the hosts you want to target beforehand in the inventory file
```shell
ansible-playbook -i inventory.yaml uninstall_playbook.yaml -K
```

### Manual installation

If you are trying to install on a Windows machine running WSL, you need to add the following line to /etc/wsl.conf to enable systemd.
```ini
[boot]
systemd=true
```
After adding this line a reboot is required. 

Next you need to clone this directory to the target machine, this can be done with the following command:
```shell
git clone https://gitlab.ewi.tudelft.nl/cse2000-software-project/2022-2023-q4/cluster-12/ruisdael-automatic-network-monitoring-system/ruisdael-elk-client.git
```

The collector needs some project specific passwords and configurations, these are stored in a .env file. There is a template you can use to create this file .env.template.j2

There are also some dependencies you can install by running 
```shell
pip3 install -r requirements.txt
```

Now the collector is able to run, you can run it via 
```shell
python3 main.py
```

If you want the program to start after a reboot, you need to create a service.
To achieve this, you need to copy the contents of collector.service.j2 to /etc/systemd/system/collector.service, and change the path on line 3 to where you cloned the repository.

To enable the service to run at startup, and start the service you need the following commands
```shell
sudo systemctl enable collector
sudo systemctl start collector
```

## Installing metricbeat

If you don't want to use our custom software, there is an installation script for installing metricbeat.
To execute it, make sure you use the provided inventory_metric_beats.yaml file, there is also a template
The certificate inside the inventory file can be retrieved via running this command on the elasticsearch server
```shell
sudo openssl x509 -fingerprint -sha256 -in /etc/elasticsearch/certs/http_ca.crt
```

You can run the installation script with the following command.
```shell
ansible-playbook -i inventory_metric_beats.yaml install_metricbeats_playbook.yaml -K
```
You can add --limit to chose on which of the hosts the ansible will be executed. 
The -K means that you need to provide a password to the account that will execute the playbook on the nodes. You are prompted for this after you start the playbook

You need to provide the hosts you want to target in the inventory_metric_beats.yaml file under the hosts section.
This hosts section should look something like this:
```yaml
all:
  hosts:
    ansible_hosts: [[hostname inside your ~/.ssh/config file]]
    ansible_user: [[username that will execute the commands in the playbook]]
```

To check if the playbook worked, you can ssh into the target machine and run this command
```shell
sudo systemctl status metricbeat
```
This should say running.

To uninstall metricbeat, you can run this command.
```shell
ansible-playbook -i inventory_metric_beats.yaml uninstall_metricbeats_playbook.yaml -K
```
It uses the same inventory file.

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
among the send data. Lastly, the `time.sleep(n)` makes the timeout between sending be n seconds.

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
