from flask import *
from serverCommands import Server
import webview
import threading
import requests
import os
import subprocess
import time
app = Flask(__name__)

server = Server()
@app.route('/', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        #set up where to download from and where to send to
        url = "https://api.papermc.io/v2/projects/paper/versions/1.21.4/builds/187/downloads/paper-1.21.4-187.jar"
        filename = "paper-1.21.4-187.jar"
        if request.form['path'] == "":
            saveDir = "c:\dev-server"
        else:
            saveDir = request.form['path']
    
        os.makedirs(saveDir, exist_ok=True)
        paperFilePath = os.path.join(saveDir, filename)

        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(paperFilePath, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Download complete! File saved to: {paperFilePath}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
        
        runFile = os.path.join(saveDir, "run.bat")

        batContent= "java -Xmx1024M -Xms1024M -jar paper-1.21.4-187.jar nogui"

        with open(runFile, "w") as file:
            file.write(batContent)
        print(f"Batch file saved at: {runFile}")    
        time.sleep(1)
        subprocess.Popen(["cmd.exe", "/c", f"title MinecraftServer && cd /d " + saveDir + " && run run.bat"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        while os.path.exists(saveDir + "/eula.txt") == False:
            time.sleep(.1)
        time.sleep(3)
        eulaContent = "eula=true\n"
        with open(saveDir + "/eula.txt", "w") as file:
            file.write(eulaContent)

        time.sleep(1)
        serverManConfig = saveDir
        serverConfig = os.path.join("./ServermanConfig.txt")
        with open(serverConfig, "w") as file:
            file.write(serverManConfig + "\n")
        return redirect("/control")

    return render_template('index.html')   

@app.route('/control', methods=['GET', 'POST'])
async def controlPanel():
    if request.method == 'POST':
        if request.form['bat'] != "":
            server.setRoute(request.form['bat'])
        if request.form['playIt'] != "":
            server.setPlayIt(request.form['playIt'])
        
        if request.form['action'] == "Start":
            server.controlServer("run")
        if request.form['action'] == "Stop":
            server.controlServer("stop")
        if request.form['action'] == "Schedule Start":
            await server.scheduleStart(request.form['startTime'])
        if request.form['action'] == "Schedule Stop":
            await server.scheduleStop(request.form['stopTime'])
    return render_template('controlPanel.html')     

# Create a function to run the Flask app in a separate thread
def run_flask():
    app.run()

# Run the Flask app in a separate thread and start the webview window
def start_desktop_app():
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Create a window with pywebview
    webview.create_window("ServerMan", "http://127.0.0.1:5000/")
    webview.start()

if __name__ == '__main__':
    start_desktop_app()