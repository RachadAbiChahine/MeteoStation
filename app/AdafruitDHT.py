#!/usr/bin/python
import sqlite3
import json
from datetime import datetime
import Adafruit_DHT
from flask import Flask, render_template
from flask import json

app = Flask(__name__)
db = sqlite3.connect('meteo_station.db', check_same_thread=False)
cursor = db.cursor()


@app.route("/api")
def render_as_api():
    data = dumps(get_humidity_and_temp())
    response = app.response_class(
        response=data, status=200, mimetype='application/json'

    )
    return response


@app.route("/")
def render_as_web_page():
    data = get_humidity_and_temp()
    all = db.execute("select * from meteo_station ")
    json_response = []
    for raw in all:
        json_response.append([raw[0], raw[1], raw[2]])
    return render_template("index.html", temperature=data['temperature'], humidity=data['humidity'],
                           allData=json.dumps(json_response))


@app.route("/all")
def get_all_data():
    data = db.execute("select * from meteo_station ")
    json_response = []
    for raw in data:
        json_response.append({'datetime': raw[0], 'temperature': raw[1], 'humidity': raw[2]})
    response = app.response_class(
        response=json.dumps(json_response), status=200, mimetype='application/json')
    return response


def get_humidity_and_temp():
    sensor = 11
    pin = 21
    humidity, temp = Adafruit_DHT.read_retry(sensor, pin)
    data = {}
    if humidity is not None and temp is not None:
        data['humidity'] = humidity
        data['temperature'] = temp
    else:
        data['error'] = "unable to get information"
    sql_statement = 'insert into meteo_station values(?,?,?)'
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(sql_statement, (now, temp, humidity))
    db.commit()
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0')
