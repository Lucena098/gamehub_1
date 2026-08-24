from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User, Game, Library, Review


main = Blueprint("main", __name__)


# ==========================================
# PÁGINA INICIAL
# ==========================================

@main.route("/")
def home():
    return render_template("index.html")


# ==========================================
# CADASTRO
# ==========================================

@main.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            return "Este email já está cadastrado."

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            bio=""
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template("register.html")


# ==========================================
# LOGIN
# ==========================================

@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(
                url_for("main.home")
            )

        return "Email ou senha incorretos."

    return render_template("login.html")


# ==========================================
# LOGOUT
# ==========================================

@main.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("main.home")
    )


# ==========================================
# PERFIL
# ==========================================

@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":

        current_user.bio = request.form["bio"]

        db.session.commit()

        return redirect(
            url_for("main.profile")
        )

    return render_template(
        "profile.html"
    )


# ==========================================
# LISTA DE JOGOS
# ==========================================

@main.route("/games")
def games():

    games = Game.query.all()

    return render_template(
        "games.html",
        games=games
    )


# ==========================================
# PÁGINA INDIVIDUAL DO JOGO
# ==========================================

@main.route("/game/<int:game_id>")
def game_detail(game_id):

    game = Game.query.get_or_404(game_id)

    reviews = Review.query.filter_by(
        game_id=game.id
    ).all()

    return render_template(
        "game_detail.html",
        game=game,
        reviews=reviews
    )


# ==========================================
# ADICIONAR JOGO À BIBLIOTECA
# ==========================================

@main.route(
    "/game/<int:game_id>/add",
    methods=["POST"]
)
@login_required
def add_to_library(game_id):

    game = Game.query.get_or_404(game_id)

    status = request.form.get(
        "status",
        "Quero jogar"
    )

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

    return redirect(
        url_for(
            "main.game_detail",
            game_id=game.id
        )
    )


# ==========================================
# MINHA BIBLIOTECA
# ==========================================

@main.route("/library")
@login_required
def library():

    library = Library.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "library.html",
        library=library
    )


# ==========================================
# ADICIONAR AVALIAÇÃO
# ==========================================

@main.route(
    "/game/<int:game_id>/review",
    methods=["POST"]
)
@login_required
def add_review(game_id):

    game = Game.query.get_or_404(game_id)

    rating = int(
        request.form["rating"]
    )

    comment = request.form.get(
        "comment"
    )

    if rating < 1 or rating > 5:

        return "Nota inválida."

    review = Review(
        user_id=current_user.id,
        game_id=game.id,
        rating=rating,
        comment=comment
    )

    db.session.add(review)

    db.session.commit()

    return redirect(
        url_for(
            "main.game_detail",
            game_id=game.id
        )
    )
