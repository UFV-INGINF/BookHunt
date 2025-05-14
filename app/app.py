import os

import requests
from flask import Flask, jsonify, render_template, request
from app.scraper import scrapear_libros

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes?q="

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])  # Vistas, en este caso raíz
def index():
    libros = []

    if request.method == "POST":
        isbn = request.form.get("isbn_libro", "").strip()
        if isbn:
            libros = scrapear_libros(isbn)
            libros = sorted(libros, key=lambda libro: libro.total)

    return render_template("index.html", libros = libros, scroll_to_buscador=True)


@app.route("/buscar_fragmento", methods=["POST"])
def buscar_por_fragmento():
    # Obtenemos el fragmento de texto desde el formulario
    fragmento = request.form.get("fragmento_libro", "").strip()

    if not fragmento:
        return jsonify({"error": "Se requiere un fragmento de texto"}), 400

    # Hacemos la consulta a la API de Google Books
    url = GOOGLE_BOOKS_API_URL + fragmento
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Error al consultar la API de libros"}), 500

    # Procesamos la respuesta de la API
    books_data = response.json()
    books = []

    if "items" in books_data:
        for item in books_data["items"]:
            info = item.get("volumeInfo", {})
            books.append(
                {
                    "titulo": info.get("title", "No disponible"),
                    "autores": info.get("authors", ["Desconocido"]),
                    "editorial": info.get("publisher", "Desconocido"),
                    "año_publicacion": info.get("publishedDate", "Desconocido"),
                }
            )

    return render_template("index.html", books=books)

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 5000))  # Usamos el puerto que Heroku define
    # app.run(debug=False, host='0.0.0.0', port=port)

    # Configuración debug
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
