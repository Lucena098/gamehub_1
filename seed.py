from app import create_app, db
from app.models import Game

app = create_app()

with app.app_context():

    games = [
        Game(
            title="Minecraft",
            description="Um jogo de exploração, construção e sobrevivência.",
            genre="Sandbox",
            platform="PC, PlayStation, Xbox, Switch",
            release_date="2011"
        ),

        Game(
            title="Genshin Impact",
            description="Um RPG de ação e exploração em mundo aberto.",
            genre="RPG",
            platform="PC, PlayStation, Mobile",
            release_date="2020"
        ),

        Game(
            title="Hollow Knight",
            description="Um jogo de ação e aventura em um mundo subterrâneo.",
            genre="Metroidvania",
            platform="PC, PlayStation, Xbox, Switch",
            release_date="2017"
        )
    ]

    db.session.add_all(games)
    db.session.commit()

    print("🎮 Jogos adicionados com sucesso!")