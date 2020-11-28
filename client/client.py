import datetime
import logging
from aiocoap import *
import asyncio
import os
import imghdr

import argparse

class VideoMessaging():
    def __init__(self):
        self.foldername = None
        self.image = None
        
    async def send_content(self, foldername):
        # gets the folder of images to send files
        folder = os.path.dirname(foldername)+foldername
        logging.log(logging.INFO, "Folder to send: " + folder)
        # Loop throuhg all files, and send the data. 
        for f in os.listdir(folder):
            fullpath = os.path.join(folder, f)
            context = await Context.create_client_context()
            with open (fullpath, "rb") as img:
                self.image = img.read()
                request = Message(code=POST, payload=self.image, uri="coap://localhost/api/1.0/receiveVideo")
                response = await context.request(request).response
                print("Result: %s\n%r" % (response.code, response.payload))
                
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



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Folder of images to be sent", type=str)
    parser.add_argument("-l", "--logLevel", help="Sets the log level", type=int)
    args = parser.parse_args()
    if args.logLevel:
        logLevel = args.logLevel
    else:
        logLevel = 0

    setLogging(logLevel)
    videoMessaging = VideoMessaging()
    asyncio.get_event_loop().run_until_complete(videoMessaging.send_content(args.folder))


