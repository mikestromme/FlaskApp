from flask import Flask, render_template, jsonify
import time
import subprocess
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Simulated progress
current_progress = 0

def run_demucs():
    process = subprocess.Popen(['demucs', '-n', 'mdx_extra', 'input/Barracuda.mp3'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.STDOUT, 
                               universal_newlines=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            # Parse the output to get progress information
            # Send progress back to the browser
            progress = subprocess.run(['demucs', '-n', 'mdx_extra', 'input/Barracuda.mp3'])  # Extract progress from output  # Extract progress from output
            print(progress)  # For testing, you can print it out
            socketio.emit('update_progress', {'progress': progress})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_progress')
def get_progress():
    global current_progress

    if current_progress < 100:
        current_progress += 1
        #current_progress = demucs -n mdx_extra "You Really Got Me.mp3"

    return jsonify({'progress': current_progress})

@app.route('/process', methods=['POST'])
def process_audio():
    # Start the background task to run the demucs command
    socketio.start_background_task(target=run_demucs)
    return 'Processing started'

if __name__ == '__main__':
    app.run(debug=True)
