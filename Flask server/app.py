from flask import Flask, request, jsonify, render_template

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

    # Print received values for debugging
    print(f'Received temperature: {temperature}, humidity: {humidity}')

    if temperature is None or humidity is None:
        return jsonify({'error': 'Missing temperature or humidity data'}), 400

    return jsonify({'status': 'success'}), 200

@app.route('/data', methods=['GET'])
def data():
    return jsonify({'temperature': temperature, 'humidity': humidity})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
