from flask import Flask, jsonify

app = Flask(__name__)

# Catálogo fake (em memória)
catalogo = [
    {"id": 1, "titulo": "Stranger Things", "genero": "Ficção Científica"},
    {"id": 2, "titulo": "La Casa de Papel", "genero": "Ação"},
    {"id": 3, "titulo": "The Witcher", "genero": "Fantasia"},
    {"id": 4, "titulo": "Breaking Bad", "genero": "Drama"},
]

# Rota inicial
@app.route("/")
def home():
    return jsonify({"mensagem": "API da Netflix Fake - Bem-vindo!"})

# Rota para listar todo catálogo
@app.route("/catalogo")
def listar_catalogo():
    return jsonify(catalogo)

# Rota para buscar por ID
@app.route("/catalogo/<int:item_id>")
def buscar_por_id(item_id):
    for item in catalogo:
        if item["id"] == item_id:
            return jsonify(item)
    return jsonify({"erro": "Item não encontrado"}), 404

# Rota para filtrar por gênero
@app.route("/catalogo/genero/<genero>")
def filtrar_por_genero(genero):
    resultado = [item for item in catalogo if item["genero"].lower() == genero.lower()]
    if resultado:
        return jsonify(resultado)
    return jsonify({"erro": "Nenhum item encontrado para esse gênero"}), 404


if __name__ == "__main__":
    app.run(debug=True)
