from flask import Flask, request, jsonify, render_template
import csv
import time
import threading

app = Flask(__name__)

temperature = None  # Global variable for temperature
humidity = None     # Global variable for humidity

@app.route('/')
def index():
    return render_template('index.html', temperature=temperature, humidity=humidity)

@app.route('/update', methods=['GET'])
def update():
    global temperature, humidity
    temperature = request.args.get('temperature', type=float)
    humidity = request.args.get('humidity', type=float)

    print(f'Received temperature: {temperature}, humidity: {humidity}')

    if temperature is None or humidity is None:
        return jsonify({'error': 'Missing temperature or humidity data'}), 400

    return jsonify({'status': 'success'}), 200

@app.route('/data', methods=['GET'])
def data():
    return jsonify({'temperature': temperature, 'humidity': humidity})

def log_data_to_csv():
    global temperature, humidity
    if temperature is not None and humidity is not None:
        with open('data_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), temperature, humidity])
        print(f"Logged data: Temperature = {temperature}, Humidity = {humidity}")
    # Schedule the next log after 1 hour
    threading.Timer(3600, log_data_to_csv).start()

if __name__ == '__main__':
    # Start logging every hour when the app starts
    threading.Timer(3600, log_data_to_csv).start()
    app.run(host='0.0.0.0', port=5000, debug=True)
