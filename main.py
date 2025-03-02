from flask import *
from serverCommands import Server
import webview
import threading

app = Flask(__name__)

server = Server()
@app.route('/', methods=['GET', 'POST'])
async def display():
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
    return render_template('index.html')     

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