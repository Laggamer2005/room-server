import uuid

from flask import url_for, flash, render_template, send_from_directory
from werkzeug.utils import redirect
from flask_oidc import OpenIDConnect
from first import conf_first_bin_xml
from models import User, db
from room import app

import config


oidc = OpenIDConnect(app)


@app.context_processor
def inject_oidc():
    return dict(oidc=oidc)


def is_maintenance():
    returned_xml = conf_first_bin_xml()
    if b"<maint>1</maint>" in returned_xml:
        return True
    else:
        return False


@app.route("/")
def index():
    return redirect(url_for("root"))


@app.route("/theunderground")
@app.route("/theunderground/")
def root():
    return redirect(url_for("login"))


@app.route("/theunderground/login")
def login():
    if oidc.user_loggedin:
        return redirect(url_for("admin"))

    return render_template("login.html")


@app.route("/theunderground/logout")
@oidc.require_login
def logout():
    oidc.logout()
    response = redirect(config.oidc_logout_url)
    response.set_cookie("session", expires=0)
    return response


@app.route("/theunderground/admin")
@oidc.require_login
def admin():
    return render_template("underground.html", maintenance=is_maintenance())
