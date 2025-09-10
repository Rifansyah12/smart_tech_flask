from flask import Flask, render_template, request, redirect, session, url_for, make_response
import pymysql
import bcrypt
import traceback
import paho.mqtt.client as mqtt
import threading
from flask import jsonify


app = Flask(__name__)
app.secret_key = '12345'

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="smart_nose",
        cursorclass=pymysql.cursors.DictCursor
    )


# Konfigurasi MQTT
BROKER = "smartnose-uninus.cloud.shiftr.io"
PORT = 1883
USERNAME = "smartnose-uninus"
PASSWORD = "0DKItrqWCc9bbr5w"
TOPIC = "smartnose-uninus/#" 


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT Connected to Shiftr.io")
        client.subscribe(TOPIC, qos=1)
    else:
        print("❌ MQTT Connection failed with code", rc)
mqtt_data = []

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"📩 Pesan diterima di {msg.topic}: {payload}")

        data = {
            "id": len(mqtt_data) + 1,
            "serial_number": "SN001",   
            "sensor_actuator": "sensor",
            "value": payload,
            "name": "Sensor A",
            "mqtt_topic": msg.topic
        }
        mqtt_data.append(data)

        # batasi hanya 100 data terakhir
        if len(mqtt_data) > 100:
            mqtt_data.pop(0)

    except Exception as e:
        print("❌ Error parsing MQTT message:", e)


client = mqtt.Client(client_id="vsmqtt_client_5d7e")  # Client ID bisa custom
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

def mqtt_loop():
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

# Jalankan MQTT di background thread
threading.Thread(target=mqtt_loop, daemon=True).start()

# Contoh route untuk publish ke broker
@app.route("/send_mqtt")
def send_mqtt():
    if 'username' not in session:
        return redirect(url_for('login'))
    client.publish("smartnose-uninus/test", "Halo dari Flask + Shiftr.io", qos=1)
    return "Pesan MQTT terkirim ke Shiftr.io!"

# ------------------------
# Fungsi untuk mencegah cache browser
# ------------------------
def nocache(view):
    def no_cache(*args, **kwargs):
        resp = make_response(view(*args, **kwargs))
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '-1'
        return resp
    no_cache.__name__ = view.__name__
    return no_cache

# endpoint_device
@app.route("/api/device_info")
def api_device_info():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT serial_number, mcu_type, location, created_time, active
            FROM devices
            ORDER BY created_time DESC LIMIT 1
        """)
        device = cursor.fetchone()
        cursor.close()
        conn.close()

        if device:
            # Normalisasi nilai active
            device["active"] = True if str(device["active"]).lower() in ["1", "yes", "true"] else False
            return jsonify(device)
        else:
            return jsonify({})
    except Exception as e:
        print("❌ Error get device info:", e)
        return jsonify({})


# ------------------------
# Routes
# ------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
@nocache
def login():
    return proses_login_smart("login.html", "smart_index")
# smart_nose
@app.route("/smart/smart_nose/dashboard")
@nocache
def smart_nose_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("smart/smart_nose/dashboard.html")

# smart_house
@app.route("/smart/smart_house/dashboard")
@nocache
def smart_house_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("smart/smart_house/dashboard.html")

# smart_parking
@app.route("/smart/smart_parking/dashboard")
@nocache
def smart_parking_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("smart/smart_parking/dashboard.html")

# smart_trash
@app.route("/smart/smart_trash/dashboard")
@nocache
def smart_trash_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("smart/smart_trash/dashboard.html")

# smart_plts
@app.route("/smart/smart_plts/dashboard")
@nocache
def smart_plts_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("smart/smart_plts/dashboard.html")

# smart_green_park
@app.route("/smart/smart_greenPark/dashboard")
@nocache
def smart_greenPark_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("smart/smart_greenPark/dashboard.html")





@app.route("/smart/index")
@nocache
def smart_index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template(
        "smart/index.html",
        fullname=session.get('fullname', 'Guest'),
        role=session.get('role', 'User'),
        flash_message=None
    )

@app.route("/logout")
@nocache
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------------
# Fungsi Login
# ------------------------
def proses_login_smart(template_name, index_route):
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template(template_name, message="Username dan Password wajib diisi")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM `user` WHERE username=%s LIMIT 1", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if not user:
                return render_template(template_name, message="Username tidak terdaftar")

            db_password = user.get('password', '')
            if db_password.startswith("$2y$"):
                db_password = "$2b$" + db_password[4:]

            valid = bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8'))

            if valid:
                session['username'] = user.get('username', '')
                session['fullname'] = user.get('fullname', '')
                session['role'] = user.get('role', '')
                return redirect(url_for(index_route))
            else:
                return render_template(template_name, message="Password salah")
        except Exception as e:
            print("Error saat login:", e)
            traceback.print_exc()
            return render_template(template_name, message="Terjadi kesalahan di server")
    return render_template(template_name)





@app.route("/api/mqtt_data")
def api_mqtt_data():
    return jsonify(mqtt_data)

if __name__ == "__main__":
    app.run(debug=True)
