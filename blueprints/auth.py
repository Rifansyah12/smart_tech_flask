from flask import Blueprint, render_template, request, redirect, session, url_for
import bcrypt, traceback
from extensions import get_db_connection, nocache

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
@nocache
def login():
    return proses_login("login.html", "dashboard.smart_index")

@auth_bp.route("/logout")
@nocache
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

def proses_login(template_name, index_route):
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

            valid = bcrypt.checkpw(password.encode(), db_password.encode())

            if valid:
                session['username'] = user.get('username', '')
                session['fullname'] = user.get('fullname', '')
                session['role'] = user.get('role', '')
                return redirect(url_for(index_route))
            else:
                return render_template(template_name, message="Password salah")
        except Exception as e:
            print("❌ Error login:", e)
            traceback.print_exc()
            return render_template(template_name, message="Server error")
    return render_template(template_name)
