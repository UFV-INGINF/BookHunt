import requests
from decimal import Decimal

from app.models.libro import Libro


def construir_url_busqueda(isbn_libro: str) -> str:
    """
    Construye la URL para la API de Casa del Libro con el ISBN especificado.

    Args:
        isbn_libro (str): ISBN del libro a buscar.

    Returns:
        str: URL completa para la API de Casa del Libro.
    """

    try:
        isbn_int = int(isbn_libro)

    except ValueError:
        print(isbn_libro)
        print("El ISBN debe ser un número entero.")
        return ""

    return f"https://api.empathy.co/search/v1/query/cdl/isbnsearch?internal=true&query={isbn_int}&origin=search_box:none&start=0&rows=24&instance=cdl&lang=es&scope=desktop&currency=EUR&store=ES"


def  scrape_casa_del_libro(isbn_libro):
    """Scraper de Casa del Libro utilizando requests.

    Args:
        isbn_libro: ISBN del libro a buscar.

    Returns:
        list: Lista de objetos Libro con la información extraída.
    """

    libros = []

    isbn_libro = isbn_libro.replace("-", "")
    isbn_libro = isbn_libro.replace(" ", "")

    url_libro = construir_url_busqueda(isbn_libro)

    if url_libro == "":
        print("Error al construir la URL.")
        return libros

    response = requests.get(
        url_libro
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return libros

    dict_response = response.json()

    if dict_response["catalog"]["numFound"] == 0:
        print("No se han encontrado resultados.")
        return libros

    book_info = dict_response["catalog"]["content"][0]

    titulo = book_info["__name"].title()
    isbn_libro_scrap = book_info["ean"]
    precio = book_info["price"]["current"]
    enlace = book_info["__url"]
    autor = book_info["authors"][0]

    if isbn_libro != isbn_libro_scrap:
        print(f"El ISBN {isbn_libro} no coincide con el ISBN {isbn_libro_scrap}.")
        return libros

    gastos_envio = 0.0

    # En la casa del libro, los gastos de envío son 0 si el precio es mayor a 19
    if precio < 19:
        gastos_envio = 2.99

    libro = Libro(
        nombre = titulo,
        autor = autor,
        isbn = isbn_libro_scrap,
        tienda = "Casa del Libro",
        precio = Decimal(str(precio)),
        gastos_envio = gastos_envio,
        enlace = enlace,
        fecha_entrega = "1 a 3 días"
    )

    libros.append(libro)

    return libros
