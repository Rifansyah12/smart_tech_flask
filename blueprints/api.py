from flask import Blueprint, jsonify
from extensions import get_db_connection, sensor_state


api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/device_info")
def device_info():
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
            device["active"] = str(device["active"]).lower() in ["1", "yes", "true"]
            return jsonify(device)
        else:
            return jsonify({})
    except Exception as e:
        print("❌ Error get device info:", e)
        return jsonify({})

@api_bp.route("/mqtt_data")
def mqtt_data_api():
    return jsonify(sensor_state)


