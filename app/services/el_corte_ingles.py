from decimal import Decimal

import httpx
import secrets

from app.models.libro import Libro

headers = {
    "Host": "www.elcorteingles.es",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en,en-US;q=0.5",
    "DNT": "1",
    "Connection": "keep-alive",
    "Cookie": f"store=eciStore; locale=es_ES; session_id=f{secrets.token_hex(32)};",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1"
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
        return None

    try:

        with httpx.Client(http2=True, headers=headers, timeout=20) as client:
            response = client.get(url_libro)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None

        dict_response = response.json()

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
            return None

        # En el corte ingles no lo indican, así que lo dejamos a 0
        gastos_envio = 0.0

        libro = Libro(
            nombre = titulo.title(),
            autor = autor.title(),
            isbn = isbn_libro_scrap,
            tienda = "El Corte Inglés",
            precio = Decimal(str(precio)),
            gastos_envio = gastos_envio,
            enlace = enlace [:-1] + "?parentCategoryId=999.54302013&color=Sin+especificar",
            fecha_entrega = "1 a 3 días"
        )

        libros.append(libro)

    except httpx.ConnectTimeout:
        print("Error: Tiempo de conexión agotado.")
        return None

    except httpx.ReadTimeout:
        print("Error: Tiempo de lectura agotado.")
        return None

    except httpx.TimeoutException:
        print("Error general de timeout.")
        return None

    except httpx.RequestError as e:
        print(f"Error en la solicitud: {e}")
        return None

    except httpx.HTTPStatusError as e:
        print(f"Error HTTP {e.response.status_code}: {e.response.text[:200]}")
        return None

    except httpx.StreamError as e:
        print(f"Error en el stream: {e}")
        return None

    except Exception as e:
        print(f"Error inesperado: {type(e).__name__}: {e}")
        return None


    return libros
