from flask import render_template, redirect, url_for
from flask_login import login_required

from models import ParadeMiis
from room import app, db
from theunderground.encodemii import parade_encode
from theunderground.forms import ParadeForm
from theunderground.operations import manage_delete_item


@app.route("/theunderground/parade")
@login_required
def list_parade():
    parade_miis = ParadeMiis.query.order_by(ParadeMiis.mii_id.asc()).all()
    return render_template(
        "parade_list.html", miis=parade_miis, type_length=len(parade_miis)
    )


@app.route("/theunderground/parade/<mii_id>/create", methods=["GET", "POST"])
@login_required
def create_parade(mii_id):
    form = ParadeForm()
    q = ParadeMiis.query.filter_by(mii_id=mii_id).first()
    if form.validate_on_submit():
        # Encode an image to the appropriate size.
        inserted_image = parade_encode(form.image.data.read())

        q = ParadeMiis.query.filter_by(mii_id=mii_id)
        if list(q):
            mii = q.first()
            mii.logo_bin = inserted_image
            mii.news = form.company.data
        else:
            mii = ParadeMiis(
                mii_id=mii_id,
                logo_id="g1234",
                logo_bin=inserted_image,
                news=form.company.data,
                level=1,
            )

        db.session.add(mii)
        db.session.commit()

        return redirect(url_for("list_parade"))

    return render_template("parade_add.html", form=form, room=q)


@app.route("/theunderground/parade/<mii_id>/edit", methods=["GET", "POST"])
@login_required
def edit_parade(mii_id):
    form = ParadeForm()
    q = ParadeMiis.query.filter_by(mii_id=mii_id).first()
    if form.validate_on_submit():
        # Encode an image to the appropriate size.
        inserted_image = parade_encode(form.image.data.read())

        q = ParadeMiis.query.filter_by(mii_id=mii_id)
        if list(q):
            mii = q.first()
            mii.logo_bin = inserted_image
            mii.news = form.company.data
        else:
            mii = ParadeMiis(
                mii_id=mii_id,
                logo_id="g1234",
                logo_bin=inserted_image,
                news=form.company.data,
                level=1,
            )

        db.session.add(mii)
        db.session.commit()

        return redirect(url_for("list_parade"))

    return render_template("parade_edit.html", form=form, room=q)


@app.route("/theunderground/parade/<mii_id>/remove", methods=["GET", "POST"])
@login_required
def remove_parade(mii_id):
    def drop_parade():
        db.session.delete(ParadeMiis.query.filter_by(mii_id=mii_id).first())
        db.session.commit()
        return redirect(url_for("list_parade"))

    return manage_delete_item(mii_id, "Parade Mii", drop_parade)


@app.route("/theunderground/parade/<mii_id>/banner.jpg")
@login_required
def get_parade_banner(mii_id):
    parade_mii = ParadeMiis.query.filter_by(mii_id=mii_id).first()
    return parade_mii.logo_bin
