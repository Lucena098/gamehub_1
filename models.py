from app import db
from flask_login import UserMixin


# ==========================================
# USUÁRIO
# ==========================================

class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    def __repr__(self):
        return f"<User {self.username}>"


# ==========================================
# JOGO
# ==========================================

class Game(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    genre = db.Column(
        db.String(100),
        nullable=True
    )

    platform = db.Column(
        db.String(100),
        nullable=True
    )

    release_date = db.Column(
        db.String(20),
        nullable=True
    )

    cover = db.Column(
        db.String(500),
        nullable=True
    )

    def __repr__(self):
        return f"<Game {self.title}>"


# ==========================================
# BIBLIOTECA
# ==========================================

class Library(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    game_id = db.Column(
        db.Integer,
        db.ForeignKey("game.id"),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Quero jogar"
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "library",
            lazy=True
        )
    )

    game = db.relationship(
        "Game",
        backref=db.backref(
            "players",
            lazy=True
        )
    )

    def __repr__(self):
        return (
            f"<Library "
            f"User:{self.user_id} "
            f"Game:{self.game_id}>"
        )


# ==========================================
# AVALIAÇÃO
# ==========================================

class Review(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    game_id = db.Column(
        db.Integer,
        db.ForeignKey("game.id"),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    comment = db.Column(
        db.Text,
        nullable=True
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "reviews",
            lazy=True
        )
    )

    game = db.relationship(
        "Game",
        backref=db.backref(
            "reviews",
            lazy=True
        )
    )

    def __repr__(self):
        return f"<Review {self.rating}/5>"
