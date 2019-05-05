import sys
import Adafruit_DHT
import json
from flask import Flask
from flask import jsonify, json

app = Flask(__name__)


@app.route("/")
def get_temp():
    data = get_humidity_and_temp()
    response = app.response_class(
        response=json.dumps(data), status=200, mimetype='application/json'

    )
    return response


def get_humidity_and_temp():
    sensor = 11
    pin = 22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        return 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
