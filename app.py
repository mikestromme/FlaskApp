from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)

# Simulated progress
current_progress = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_progress')
def get_progress():
    global current_progress

    if current_progress < 100:
        current_progress += 1

    return jsonify({'progress': current_progress})

if __name__ == '__main__':
    app.run(debug=True)
