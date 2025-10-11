from flask import Flask, render_template
import os

# Catálogo fake
catalogo = [
    {"titulo": "Stranger Things", "genero": "Ficção Científica"},
    {"titulo": "La Casa de Papel", "genero": "Ação"},
    {"titulo": "The Witcher", "genero": "Fantasia"},
    {"titulo": "Breaking Bad", "genero": "Drama"},
]

app = Flask(__name__)

# Carregar ambiente pela variável de ambiente APP_ENV
env = os.getenv("APP_ENV", "dev")

if env == "dev":
    app.config.from_pyfile("config/config_dev.py")
elif env == "hom":
    app.config.from_pyfile("config/config_hom.py")
else:
    app.config.from_pyfile("config/config_main.py")

@app.route("/")
def home():
    return render_template("index.html", ambiente=app.config["ENV_NAME"])

@app.route("/catalogo")
def catalogo_page():
    return render_template("catalog.html", catalogo=catalogo, ambiente=app.config["ENV_NAME"])

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
