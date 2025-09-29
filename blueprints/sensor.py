from flask import Blueprint, render_template, jsonify
import random, datetime

sensor_bp = Blueprint("sensor", __name__)

# Halaman Data Sensor
@sensor_bp.route("/smart/smart_nose/data_sensor")
def data_sensor():
    return render_template("smart/smart_nose/data_sensor.html")

# API Data Sensor (dummy)
@sensor_bp.route("/api/sensor_data")
def sensor_data():
    now = datetime.datetime.now()
    data = []
    for i in range(10):  # contoh 10 data terakhir
        timestamp = (now - datetime.timedelta(minutes=10-i)).strftime("%H:%M:%S")
        data.append({
            "time": timestamp,
            "sensor1": random.randint(10, 50),
            "sensor2": random.randint(20, 60),
            "sensor3": random.randint(15, 55),
            "sensor4": random.randint(5, 40),
            "sensor5": random.randint(25, 70),
            "sensor6": random.randint(30, 80),
        })
    return jsonify(data)
