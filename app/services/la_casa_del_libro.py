import requests
from app.models.libro import Libro


def construir_url_busqueda(isbn_libro: int) -> str:
    """
    Construye la URL para la API de Casa del Libro con el ISBN especificado.

    Args:
        isbn_libro (int): ISBN del libro a buscar.

    Returns:
        str: URL completa para la API de Casa del Libro.
    """

    try:
        isbn_libro = int(isbn_libro)
    except ValueError:
        print("El ISBN debe ser un número entero.")
        return ""

    return f"https://api.empathy.co/search/v1/query/cdl/isbnsearch?internal=true&query={isbn_libro}&origin=search_box:none&start=0&rows=24&instance=cdl&lang=es&scope=desktop&currency=EUR&store=ES"


def  scrape_casa_del_libro(isbn_libro):
    """Scraper de Casa del Libro utilizando requests y BeautifulSoup.

    Args:
        isbn_libro: ISBN del libro a buscar.

    Returns:
        list: Lista de objetos Libro con la información extraída.
    """

    libros = []
    url_libro = construir_url_busqueda(isbn_libro)

    response = requests.get(
        url_libro
    )

    dict_response = response.json()
    book_info = dict_response["catalog"]["content"][0]

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return libros

    if dict_response["catalog"]["numFound"] == 0:
        print("No se han encontrado resultados.")
        return libros

    titulo = book_info["__name"].title()
    isbn_libro = book_info["ean"]
    precio = book_info["price"]["current"]
    enlace = book_info["__url"]

    gastos_envio = 0.0

    # En la casa del libro, los gastos de envío son 0 si el precio es mayor a 19
    if precio < 19:
        gastos_envio = 2.99

    print(book_info["__name"].title())
    print(book_info["ean"])
    print(book_info["price"]["current"])

    libro = Libro(
        nombre = titulo,
        isbn = isbn_libro,
        tienda = "Casa del Libro",
        precio = precio,
        gastos_envio = gastos_envio,
        enlace = enlace,
        fecha_entrega = "1 a 3 días"
    )

    libros.append(libro)

    return libros
