import threading
import atexit
from flask import Flask

POOL_TIME = 5 #Seconds

# variables that are accessible from anywhere
commonDataStruct = {}
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
yourThread = threading.Thread()

def create_app():
    app = Flask(__name__)

    def interrupt():
        global yourThread
        yourThread.cancel()

    def do_stuff():
        global commonDataStruct
        global yourThread
        with dataLock:
        # Do your stuff with commonDataStruct Here
            print("hello")
        # Set the next thread to happen
        yourThread = threading.Timer(POOL_TIME, do_stuff, ())
        yourThread.start()

    def doStuffStart():
        # Do initialisation stuff here
        global yourThread
        # Create your thread
        yourThread = threading.Timer(POOL_TIME, do_stuff, ())
        yourThread.start()

    # Initiate
    doStuffStart()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

app = create_app()
if __name__ == '__main__':
    app.run()