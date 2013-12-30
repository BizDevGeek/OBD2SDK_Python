OBD2SDK_Python
==============

Python SDK for using the OBD2 cloud storage service

Contains an SDK that you can use to save OBD2 PID values. 

The SDK stores the saved values in a local buffer. The buffer is a MongoDB collection. 

sync.py pulls records from the local buffer (MongoDB) and sends them to the API via JSON. It then removes them from the buffer. 
