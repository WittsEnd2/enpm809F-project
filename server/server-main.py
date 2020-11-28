import datetime
import logging
import os
import asyncio
import argparse
import glob

import aiocoap.resource as resource
import aiocoap

imageType = None
        
class ProcessVideo(resource.Resource):
    def __init__(self):
        super().__init__()
        self.videoBytes = None
        
    async def render_post(self, request):
        global imageType
        # Gets the current time and puts it in a specific format
        currentTime = datetime.datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")
        logging.log(logging.INFO, "Current Time: " + currentTime)
        #makes directory if it doesn't exist (for receiving files)
        if not os.path.exists('receivedFiles'):
            os.makedirs('receivedFiles')
            logging.log(logging.INFO, "Created new folder for receiving files")
        
        # Constructs the file path and writes the file that it has received
        
        filename = "./receivedFiles/trafficVideo" + currentTime + ".png"
        logging.log(logging.INFO, "FileName: " + filename)
        logging.log(logging.DEBUG, str(request.payload))
        with open(filename, "wb") as f:
            try:
                f.write(request.payload)
                
                logging.log(logging.INFO, "Successfully wrote to file")
            except e:
                logging.log(logging.ERROR, e)

        # constructs and sends response message    
        return aiocoap.Message(code=aiocoap.CREATED, payload="File received".encode("utf-8"))
 
# logging setup

def setLogging(level):
    """ Checks to see the level, sets it to the appropriate level """
    logLevel = None
    if level == 0:
        logLevel = logging.CRITICAL
    elif level == 1:
        logLevel = logging.ERROR
    elif level == 2:
        logLevel = logging.WARNING
    elif level == 3:
        logLevel = logging.INFO
    elif level == 4: 
        logLevel = logging.DEBUG
    else: 
        logLevel = logging.NOTSET
    logging.basicConfig(level=logLevel)
    logging.getLogger("coap-client").setLevel(logLevel)

def main():
    # Resource tree creation
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--logLevel", help="Sets the log level", type=int)
    args = parser.parse_args()
    if args.logLevel:
        logLevel = args.logLevel
    else:
        logLevel = 0
    setLogging(logLevel)        

    root = resource.Site()
    root.add_resource(['api', '1.0', 'receiveVideo'], ProcessVideo())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
