import subprocess
import psutil
import pygetwindow as gw
from datetime import datetime
import asyncio
import time

# Path to your batch file


class Server:
    def __init__(self):
        self.runServer = None
        self.runTunnel = None
        self.route = ""
        self.playItRoute = ""
        self.running = False
    
    def setRoute(self, route):
        self.route = route
    def setPlayIt(self, playItRoute):
        self.playItRoute = playItRoute

    def controlServer(self, tag):
        if tag == "run":
            self.runServer = subprocess.Popen(["cmd.exe", "/c", f"title MinecraftServer && cd /d " + self.route + " && run run.bat"], creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.runTunnel = subprocess.Popen([self.playItRoute], creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.running = True
        if tag == "stop":
            parentServer = psutil.Process(self.runServer.pid)
            for child in parentServer.children(recursive=True):
                child.terminate()
            parentServer.terminate()
            
            parentTunnel = psutil.Process(self.runTunnel.pid)
            for child in parentTunnel.children(recursive=True):
                child.terminate()
            parentTunnel.terminate()

            self.runServer = None
            self.runTunnel = None
            self.running = False
    
    async def scheduleStart(self, hour):
        currentTime = datetime.now().minute
        while self.running == False:
            time.sleep(1)
            print("start:",currentTime, " ", hour)
            currentTime = datetime.now().minute
            if int(currentTime) == int(hour):
                self.controlServer("run")

    async def scheduleStop(self, hour):
        currentTime = datetime.now().minute
        while self.running == False:
            time.sleep(1)
            print("stop:",currentTime, " ", hour)
            currentTime = datetime.now().minute
            if int(currentTime) == int(hour):
                self.controlServer("stop")







