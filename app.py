from flask import Flask, render_template
from blueprints.auth import auth_bp
from blueprints.dashboard import dashboard_bp
from blueprints.api import api_bp
from extensions import client
from blueprints.sensor import sensor_bp

app = Flask(__name__)
app.secret_key = "12345"

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(api_bp)
app.register_blueprint(sensor_bp) 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_mqtt")
def send_mqtt():
    client.publish("smartnose-uninus/test", "Halo dari Flask + Shiftr.io", qos=1)
    return "Pesan MQTT terkirim!"

if __name__ == "__main__":
    app.run(debug=True)
