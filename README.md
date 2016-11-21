# imap-attachements-extractor
Python script to extract the messages's attachments from imap server. The script connects to the imap server and download all attachements associated with the a user mailbox. The future release will support the multi-user attachements fetch. 


```````
Configuration
```````

The configuration file has the following structure:

[server_config]  
server_hostname = <MAIL SERVER HOSTNAME>  
user_name = <USERNAME>  
password = <PASSWORD>  

//Where to save the attachments / URLS 

[path]  
files_path = <FILES_PATH>  
urls_path = <URLS_PATH>  

 
