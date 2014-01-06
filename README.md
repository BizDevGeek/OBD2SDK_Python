OBD2SDK_Python
==============

Python SDK for using the OBD2 cloud storage service

The OBD2 cloud storage service is available here: https://github.com/BizDevGeek/OBD2CloudStorage

This project contains an SDK that you can use to save OBD2 PID values. Use it with existing Python based OBD2 capture software such as the popular "pyobd". Any time a PID is logged from the computer, save it using the SDK so that it gets stored in the cloud storage service.  

The SDK stores the saved values in a local buffer. The buffer is a MongoDB collection. 

sync.py pulls records from the local buffer (MongoDB) and sends them to the API via JSON. It then removes them from the buffer. 
