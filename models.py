from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

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

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)

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
class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)

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
        backref=db.backref("library", lazy=True)
    )

    game = db.relationship(
        "Game",
        backref=db.backref("players", lazy=True)
    )

    def __repr__(self):
        return f"<Library User:{self.user_id} Game:{self.game_id}>"