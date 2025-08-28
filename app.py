from flask import Flask, render_template, request, redirect, session, url_for, make_response
import pymysql
import bcrypt
import traceback

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

@app.route("/smart/smart_nose/dashboard")
@nocache
def smart_nose_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("smart/smart_nose/dashboard.html")

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

if __name__ == "__main__":
    app.run(debug=True)
