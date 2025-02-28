import requests # type: ignore
from flask import Flask, request # type: ignore
from flask import jsonify # type: ignore
from scraper import scrapear_libros

app=Flask(__name__)



@app.route('/api/<isbn>', methods=['GET'])
def get_books(isbn):
    libros = scrapear_libros(isbn)
    libros_json = [
        {
            "nombre": libro.nombre,
            "isbn": libro.isbn,
            "tienda": libro.tienda,
            "precio": libro.precio,
            "total": libro.total,
            "enlace": libro.enlace
        }
        for libro in libros
    ]
    return jsonify(libros_json)

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes?q="
@app.route('/fragmento', methods=['POST'])
def buscar_por_fragmento():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Se requiere un fragmento de texto"}), 400

    fragmento = data["text"]
    url = GOOGLE_BOOKS_API_URL + fragmento

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Error al consultar la API de libros"}), 500

    books_data = response.json()
    books = []

    if "items" in books_data:
        for item in books_data["items"]:
            info = item.get("volumeInfo", {})
            books.append({
                "titulo": info.get("title", "No disponible"),
                "autores": info.get("authors", ["Desconocido"]),
                "editorial": info.get("publisher", "Desconocido"),
                "año_publicacion": info.get("publishedDate", "Desconocido"),
            })

    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True,port=8080)