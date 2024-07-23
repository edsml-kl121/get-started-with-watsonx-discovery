# Get started on Elastic search with full-code solution in tech zone with python

### STEP 1: Go to IBM Catalouge and search `Databases for Elasticsearch
Please choose your specification (ie. CPU, RAM needed) and provision the reosource
![image](https://github.com/user-attachments/assets/d00ae721-32dd-4bd2-9fb8-d79844671890)

### STEP 2: Locate to your resource

Locate to resource list tab and wait for your instance to be fully provisioned
![Alt text](Images/locate_to_resource.png)

### STEP 3: finding your endpoint

1. Here you should copy the endpoint and keep it. You should also replace
\$USERNAME and \$PASSWORD using the credentials in step 5-6.

2. Download the certificate and keep it in local repo


![Alt text](Images/get_started.png)

### STEP 4: service credentials to get username and password

Locate to the service credential tab. Here you can use predefined key or create a new one.

![Alt text](Images/where_to_get_your_credentials.png)

### STEP 5: replacing username and password

Lastly within that key find the user name and password and replace it in the endpoint in step 4

![Alt text](Images/Find_your_credential.png)

### STEP 6: populating .env

Example below: change based on your new environment (.pem saved in same directory)
```
es_endpoint='https://ibm_cloud_b6628220_2556_497a_a7d5_1f8715a2d8fd:c10311fed1e52f01a998e2bdae6d8aae1b992c6d4ffd0215be0e457b4d210cdb@1813fc1a-4f41-4fcb-94d7-cf1432418afc.br37s45d0p54n73ffbr0.databases.appdomain.cloud:32382'
es_cert_path='48b1ff99-7b37-4370-b9e6-229f4b939777.pem'
```
Follow the env-template to populate .env file.

### STEP 7: Testing on your local
```pip install -r requirement.txt```


### STEP 8: Finally, run the main file
```python main.py```
