from decimal import Decimal

import requests

from app.models.libro import Libro

headers = {
    "Referer": "https://www.elcorteingles.es/",
    "Origin": "https://www.elcorteingles.es"
}

def construir_url_busqueda(isbn_libro: str) -> str:
    """
    Construye la URL para la API de El Corte Inglés con el ISBN especificado.

    Args:
        isbn_libro (str): ISBN del libro a buscar.

    Returns:
        str: URL completa para la API de El Corte Inglés.
    """

    try:
        isbn_int = int(isbn_libro)

    except ValueError:
        print(isbn_libro)
        print("El ISBN debe ser un número entero.")
        return ""

    return f"https://www.elcorteingles.es/api/firefly/vuestore/new-search/1/?s={isbn_int}&stype=text_box_multi&isHome=false&isBookSearch=true"


def  scrape_el_corte_ingles(isbn_libro):
    """Scraper de el Corte Ingles utilizando requests.

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

    try:
        response = requests.get(
            url_libro, headers=headers, timeout=10
        )

        print("Request hecho")

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return NotImplementedError

        dict_response = response.json()
        with open("response.json", "w") as f:
            f.write(response.text)

        if dict_response["data"]["pagination"]["_total"] == 0:
            print("No se han encontrado resultados.")
            return None

        book_info = dict_response["data"]["paginatedDatalayer"]["products"][0]

        if book_info["category"][0].lower() != "libros":
            print(f"Los resultados no son libros.")
            return None

        titulo = book_info["name"].title()

        autor = "Desconocido"

        if dict_response["data"]["products"][0]["brand"]["type"].lower() == "author":
            autor = dict_response["data"]["products"][0]["brand"]["name"]

        isbn_libro_scrap = book_info["gtin"]
        precio = book_info["price"]["f_price"]
        enlace = dict_response["data"]["products"][0]["_base_url"]

        if isbn_libro != isbn_libro_scrap:
            print(f"El ISBN {isbn_libro} no coincide con el ISBN {isbn_libro_scrap}.")
            return libros

        # En el corte ingles no lo indican, así que lo dejamos a 0
        gastos_envio = 0.0

        libro = Libro(
            nombre = titulo,
            autor = autor,
            isbn = isbn_libro_scrap,
            tienda = "El Corte Inglés",
            precio = Decimal(str(precio)),
            gastos_envio = gastos_envio,
            enlace = enlace,
            fecha_entrega = "1 a 3 días"
        )

        libros.append(libro)

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None


    return libros
