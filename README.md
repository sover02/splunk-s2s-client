# Splunk S2S Client
Splunk S2S Pure Python Protocol Implementation. Supports S2S versions v1, v2, v3. S2S has many benefits including:
* Metadata field support (host, source, sourcetype, and index)
* Support in _meta tags
* Multiline and binary data support 
* Efficiency and speed
* Compression 
* Security features (SSL)

![Screen Shot 2023-01-08 at 12 25 58](https://user-images.githubusercontent.com/519424/214026363-cd9dbe4b-34cb-4900-87cf-806e939f26d0.png)

This client is ideal for users ranging from IT administrators, who need to monitor specific custom events and send that data to Splunk for analysis, to developers and even vulnerability researchers exploring Splunk. 

In March 2022, we [published](https://claroty.com/team82/research/splunk-patches-indexer-vulnerability-disclosed-by-team82) research explaining how we uncovered a vulnerability in the Splunk S2S parser. Our client was key in finding this vulnerability, [CVE-2021-3422](https://claroty.com/team82/disclosure-dashboard/cve-2021-3422), which we used in order to trigger an OOB write vulnerability in the main Splunk service.


# How to use
Check out the examples -

```
python3 _example_v2.py 1.2.3.4
```

```
python3 _example_v3.py 1.2.3.4
```

# The longer story
### What is Splunk?
Splunk is a software platform that is used for searching, analyzing, and visualizing machine-generated data. It is commonly used for log analysis, security, and compliance.

One of the main benefits of Splunk is its ability to handle large amounts of data, and scale to meet the data analysis needs of an organization. It is commonly used in industries such as finance, healthcare, and telecommunications to monitor and optimize the performance of systems, detect and troubleshoot issues, and meet compliance requirements.

Splunk can collect data from a variety of sources, including log files, network devices, and applications. It can then index and process this data in real-time, allowing users to search, analyze, and visualize it using a web-based interface. Another popular form of data collection and transfer is the Splunk forwarder.


### Splunk Forwarder
A Splunk forwarder is a piece of software that is installed on a host machine and is used to forward data to a Splunk indexer via a dedicated protocol called S2S (Splunk-to-Splunk) over TCP port 9997. The forwarder acts as a lightweight agent that is responsible for collecting and forwarding data to the indexer, which is responsible for processing and storing the data. Indexers, meanwhile, are a main Spunk component and handle data parsing and indexing. 

![image](https://user-images.githubusercontent.com/519424/214026555-dbf046f6-5b49-4f8d-b12e-3ebc9a888b94.png)


There are several types of Splunk forwarders, including the Universal Forwarder, which is a dedicated, standalone package that is used to forward data from a single machine to a Splunk indexer. There are also forwarders that are built into certain Splunk apps, such as the Splunk App for Windows Infrastructure, which includes a forwarder that is used to forward data from Windows machines to a Splunk indexer.

Splunk forwarders are typically used to forward machine-generated data such as log files, system metrics, and network data to a Splunk indexer. They are an important component of the Splunk platform because they allow organizations to collect data from a wide variety of sources and centralize it for analysis and visualization.

Forwarders are more robust than raw network feeds for data forwarding, with capabilities such as:

* Tagging of metadata (source, source type, and host)
* Configurable buffering
* Data compression
* SSL security
* Use of any available network ports

### Splunk S2S Protocol

Forwarders communicate with indexers via S2S (Splunk-to-Splunk) over TCP port 9997 which has a couple of versions with different capabilities such as data compression, tagging of metadata, and more. 

S2S is a protocol for securely transmitting data between Splunk servers and Splunk Forwarders. It is designed to be efficient, reliable, and secure, with features such as compression, encryption, and automatic retries. S2S is often used to enable Splunk Forwarders to send data to a central indexer or to allow Splunk indexers to replicate data between each other. Here is an example of a simple S2S message in it’s decoded state:

![image](https://user-images.githubusercontent.com/519424/215508360-8b6bbb1c-43ea-4e08-837d-3594c79ae695.png)


In order to send an event, the forwarder would need to initiate a TCP conversation and send a unique signature which includes the protocol version, for example `--splunk-cooked-mode-v3--`. Next, depending on the protocol flavor and version, the forwarder would need to communicate the supported capabilities and/or register a channel to deliver the event. Finally, the event can be constructed and sent to the indexer to be handled. Each event must contain the Splunk Index, origin host, source, source type and data itself encoded as key-value pair. Different versions of the protocol encode the data differently.

We are aware of three S2S protocol versions (v1, v2, v3 (new generation)); each adds more features and capabilities including more data types, compression, security, and more.

![image](https://user-images.githubusercontent.com/519424/214026701-c5745342-1b5e-4c2c-8511-46f2976b04aa.png)


# Data Ingestion
In order to enable Splunk to process S2S data, we first need to add a new type of receiver. This is how to do it - 

### Settings → Forwarding and Receiving
![Screen Shot 2023-01-04 at 15 24 44](https://user-images.githubusercontent.com/519424/214026842-f5ef9e7e-f1a3-4a42-9d1c-8981ef0b2e65.png)

### Add new receiving data input
![Screen Shot 2023-01-04 at 15 24 53](https://user-images.githubusercontent.com/519424/214026885-63e359b9-4cff-4d5f-838c-e40728e23838.png)

### Select port (usually 9997 for S2S)
![Screen Shot 2023-01-04 at 15 25 07](https://user-images.githubusercontent.com/519424/214026893-558a3ace-717a-4f82-9b26-c0ce039c45de.png)

### That’s it
![Screen Shot 2023-01-04 at 15 25 20](https://user-images.githubusercontent.com/519424/214026895-dacbc3a8-41f5-4f1d-b830-243ec316e9f6.png)

### Now you can start receiving data over S2S
![Screen Shot 2023-01-04 at 16 07 02](https://user-images.githubusercontent.com/519424/214026899-83fe3ee2-8c77-44c2-8eaf-6fba4c283002.png)


