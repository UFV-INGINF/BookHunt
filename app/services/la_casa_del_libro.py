import re

import requests
from bs4 import BeautifulSoup
from models.libro import Libro
from playwright.sync_api import sync_playwright


def obtener_link_libro_playwright_casalibro(isbn):
    """Obtiene el enlace del libro en Casa del Libro utilizando Playwright.

    Args:
        isbn: ISBN del libro a buscar.

    Returns:
        str: URL del libro o "No encontrado" si no se encuentra.
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )  # Cambia a True si no necesitas ver el navegador
        page = browser.new_page()

        # Simulación de usuario real
        page.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
        )

        # URL de búsqueda en Casa del Libro
        search_url = f"https://www.casadellibro.com/?query={isbn}"
        page.goto(search_url, timeout=60000)

        # Esperar a que el enlace del libro aparezca (máximo 10 segundos)
        try:
            page.wait_for_selector("a.x-result-link", timeout=10000)
            link_element = page.query_selector("a.x-result-link")
        except:
            link_element = None

        if link_element:
            book_href = link_element.get_attribute("href")
            book_url = (
                book_href
                if "https" in book_href
                else f"https://www.casadellibro.com{book_href}"
            )
        else:
            book_url = "No encontrado"

        browser.close()

    return book_url


def scrape_casa_del_libro(isbn_libro):
    """Scraper de Casa del Libro utilizando requests y BeautifulSoup.

    Args:
        isbn_libro: ISBN del libro a buscar.

    Returns:
        list: Lista de objetos Libro con la información extraída.
    """

    libros = []
    url_libro = obtener_link_libro_playwright_casalibro(isbn_libro)

    if url_libro == "No encontrado":
        return libros

    response = requests.get(
        url_libro,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        },
    )

    soup = BeautifulSoup(response.text, "html.parser")

    # Extraer la información de la etiqueta title
    title_match = soup.title.text
    book_title = "Nombre no disponible"
    price = 0.0
    gastos_envio = 0.0

    if title_match is not None:
        parts = title_match.split(" | ")

        if len(parts) >= 2:
            book_title = parts[0].strip()

            # Extracción de precio usando regex (buscando formato xx.xx EUR)
            price_match = re.search(r'"(\d+\.\d+)\s+EUR"', response.text)
            if price_match:
                # Convertir el precio a float y aplicar descuento
                price = float(price_match.group(1)) - (
                    float(price_match.group(1)) * 0.05
                )
                # Redondear a 2 decimales
                price = round(price, 2)

                # En la casa del libro, los gastos de envío son 0 si el precio es mayor a 19
                if price < 19:
                    gastos_envio = 2.99

    # El enlace será el de la página del libro (no de búsqueda)
    enlace = url_libro
    libro = Libro(
        nombre=book_title.capitalize(),
        isbn=isbn_libro,
        tienda="La Casa del Libro",
        precio=price,
        gastos_envio=gastos_envio,
        enlace=enlace,
        fecha_entrega="1 a 3 días",
    )
    libros.append(libro)

    return libros
