# Introduction

This repo contains example code and configuration used to present at the Future of Data event in Johannesburg. 
It contains steps and examples on how to setup your own NiFi/MiNiFi, along with InfluxDB and Grafana to get your monitoring going. 

### Architecture
Each Linux system will deploy JAVA and Python's psutil. Periodically (default: 10s), MiNiFi will run a Python script collecting all kinds of system metrics and then compress & encrypt the data before sending it to the main NiFi system. NiFi will then decrypt and decompress and write to InfluxDB, which is a specialist time-series database. Grafana is used to connect to InfluxDB and visualize on dashboards for monitoring.
![alt text](https://raw.githubusercontent.com/willie-engelbrecht/future-of-data-nifi-minifi-linux-monitoring/master/Architecture.png "Architecture")

### Grab the following files
* NiFi: https://nifi.apache.org/download.html  
* MiNiFi: https://nifi.apache.org/minifi/download.html  
* InfluxDB: https://portal.influxdata.com/downloads  
* Grafana: https://grafana.com/grafana/download  

### Setup
Download the files above, and install NiFi, InfluxDB and Grafana on the same host, and then start the services. You should be able to browse to NiFi on host.name:8080/nifi and host.name:3000 for Grafana
Import the nifi-template.xml into your NiFi installation, and adjust the site-to-site URL to your DNS name. You will need to do the same in the config.yml file that MiNiFi uses, and adjust the site-to-site URL
Update the setup_minifi script to point to your Grafana and HTTP location where you store a copy of MiNiFi. Then run it as
```
curl -s http://your.host.name/minifi/setup_minifi | bash
```
This will download and extract MiNiFi, download the config.yml file for MiNiFi (which contains the flow for MiNiFi to execute), install dependencies and create a new Grafana dashboard for you
All the required files are in this GitHub repo, but it would be best to host them on a webserver somewhere and adjust the URL's to point to them.

### Additional Files
This repo contains additional files to use:
* nifi-template.xml: The template you need to import into NiFi and adjust to your DNS names
* config.yml: This contains the flowfile definition for MiNiFi to execute. Adjust the site-to-site URL to your location
* setup_minifi: A simple bash script to automate the deployment of MiNiFi on a rpm based distro. Adjust the URL's to your location
* metrics.py: The script that will be running on each Linux instance to collect stats using Python's psutil module

One thing you will need to do when importing the nifi-template.xml file into NiFi, is that you will need to re-set the Encryption password used in the EncryptContent processor. Please set the value as: Hortonworks

When you're done, you should have a dashboard that looks like:
![alt text](https://raw.githubusercontent.com/willie-engelbrecht/future-of-data-nifi-minifi-linux-monitoring/master/Final.JPG "Final State")


 
