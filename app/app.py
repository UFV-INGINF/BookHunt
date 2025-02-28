from flask import Flask, render_template, request # type: ignore
from scraper import scrapear_libros  # Importamos la función de scraping desde scrape.py

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST']) # Vistas, en este caso raíz
def index():
    libros = []

    if request.method == 'POST':
        isbn = request.form.get('isbn_libro', '').strip()
        if isbn:
            libros = scrapear_libros(isbn)
            libros = sorted(libros, key=lambda libro: libro.precio)
    return render_template('index.html', libros=libros)

if __name__ == '__main__':
    app.run(debug=True,port=8081)

