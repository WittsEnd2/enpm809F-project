# enpm809F-project

This is a simple clinet-server implementation of the COAP protocol.

1) Install aiocoap and all other requirements. The easiest way to do this is by running `python3 -m pip install -r requirements.txt`
2) Start the server. `python3 ./server/server-main.py -l [0-5]`
3) Start the client `python3 ./client/client.py ./client/RL -l [0-5]`
    - The second parameter needs to be a folder of images. 
    - The log level is ordered by 0 (least amount of logging) to 5 (most amount of logging).By default, you do not need to set this.