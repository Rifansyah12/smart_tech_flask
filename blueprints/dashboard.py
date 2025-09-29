from flask import Blueprint, render_template, session, redirect, url_for
from extensions import nocache

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/smart")

@dashboard_bp.route("/index")
@nocache
def smart_index():
    if 'username' not in session:
        return redirect(url_for("auth.login"))
    return render_template(
        "smart/index.html",
        fullname=session.get('fullname', 'Guest'),
        role=session.get('role', 'User')
    )
# smart_nose
@dashboard_bp.route("/smart_nose/dashboard")
@nocache
def smart_nose():
    if 'username' not in session:
        return redirect(url_for("auth.login"))
    return render_template("smart/smart_nose/dashboard.html")
# smart_house
@dashboard_bp.route("/smart_house/dashboard")
@nocache
def smart_house():
    if 'username' not in session:
        return redirect(url_for("auth.login"))
    return render_template("smart/smart_house/dashboard.html")
# smart_plts
@dashboard_bp.route("/smart_plts/dashboard")
@nocache
def smart_plts():
    if 'username' not in session:
        return redirect(url_for("auth.login"))
    return render_template("smart/smart_plts/dashboard.html")
# smart_green
@dashboard_bp.route("/smart_greenPark/dashboard")
@nocache
def smart_greenPark():
    if 'username' not in session:
        return redirect(url_for("auth.login"))
    return render_template("smart/smart_greenPark/dashboard.html")
# smart_parking
@dashboard_bp.route("/smart_parking/dashboard")
@nocache
def smart_parking():
    if 'username' not in session:
        return redirect(url_for("auth.login"))
    return render_template("smart/smart_parking/dashboard.html")
# smart_trash
@dashboard_bp.route("/smart_trash/dashboard")
@nocache
def smart_trash():
    if 'username' not in session:
        return redirect(url_for("auth.login"))
    return render_template("smart/smart_trash/dashboard.html")

# Tambahkan smart_parking, smart_trash, smart_plts, smart_greenPark dengan pola sama
