from decimal import Decimal

import requests
from bs4 import BeautifulSoup

from app.models.libro import Libro


def scrape_iberlibro(isbn_libro):
    """Scraper de Iberlibro utilizando requests y BeautifulSoup."""
    url = f"https://www.iberlibro.com/servlet/SearchResults?ds=20&kn={isbn_libro}&sts=t"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
    }

    response = requests.get(url, headers=headers)
    libros = []

    if response.status_code != 200:
        print(f"Error al acceder a Iberlibro (status code: {response.status_code})")
        return libros

    soup = BeautifulSoup(response.text, "html.parser")

    # Buscar el primer libro en la lista de resultados
    item = soup.select_one("li[data-test-id='listing-item']")

    if item:
        try:
            # Extraer nombre del libro
            nombre_element = item.select_one("span[data-test-id='listing-title']")
            nombre = (
                nombre_element.text.strip()
                if nombre_element
                else "Nombre no disponible"
            )

            # Extraer precio del libro
            precio_element = item.select_one("p[data-test-id='item-price']")
            gastos_envio = 0.0

            gastos_envio_element = item.select_one("span[id='item-shipping-price-1']")

            if precio_element:
                precio_texto = precio_element.text.strip()
                precio = float(
                    precio_texto.replace("EUR", "").replace(",", ".").strip()
                )
            else:
                precio = 0.0

            if gastos_envio_element:
                gastos_envio_texto = gastos_envio_element.text.strip()
                gastos_envio = float(
                    gastos_envio_texto.replace("EUR", "")
                    .replace(",", ".")
                    .replace("Gastos de envío", "")
                    .strip()
                )

            # Extraer enlace del libro
            link_element = item.select_one("a[itemprop='url']")
            if link_element and "href" in link_element.attrs:
                enlace = f"https://www.iberlibro.com{link_element['href']}"
            else:
                enlace = url  # Usar la URL de búsqueda como respaldo

            # Crear objeto Libro
            libro = Libro(
                nombre=nombre,
                isbn=isbn_libro,
                tienda="Iberlibro",
                precio=Decimal(str(precio)),
                gastos_envio=gastos_envio,
                enlace=enlace,
                fecha_entrega="No hay información",
            )
            libros.append(libro)

        except Exception as e:
            print(f"Error al extraer información de un libro de Iberlibro: {e}")
    else:
        print(f"No se encontraron resultados para el ISBN {isbn_libro} en Iberlibro")

    return libros
