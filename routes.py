from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Este email já está cadastrado."

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("main.home"))

        return "Email ou senha incorretos."

    return render_template("login.html")

@main.route("/logout")
def logout():

    logout_user()

    return redirect(url_for("main.home"))


@main.route("/games")
def games():

    from app.models import Game

    games = Game.query.all()

    return render_template(
        "games.html",
        games=games
    )
@main.route("/game/<int:game_id>")
def game_detail(game_id):

    from app.models import Game

    game = Game.query.get_or_404(game_id)

    return render_template(
        "game_detail.html",
        game=game
    )

@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":

        current_user.bio = request.form["bio"]

        db.session.commit()

        return redirect(url_for("main.profile"))

    return render_template("profile.html")
@main.route("/game/<int:game_id>/add", methods=["POST"])
@login_required
def add_to_library(game_id):

    from app.models import Game, Library

    game = Game.query.get_or_404(game_id)

    status = request.form.get("status", "Quero jogar")

    existing = Library.query.filter_by(
        user_id=current_user.id,
        game_id=game.id
    ).first()

    if existing:
        existing.status = status
    else:
        library_item = Library(
            user_id=current_user.id,
            game_id=game.id,
            status=status
        )

        db.session.add(library_item)

    db.session.commit()

    return redirect(url_for(
        "main.game_detail",
        game_id=game.id
    ))
@main.route("/library")
@login_required
def library():

    from app.models import Library

    library = Library.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "library.html",
        library=library
    )