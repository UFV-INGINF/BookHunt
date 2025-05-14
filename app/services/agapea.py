import requests
from bs4 import BeautifulSoup
from app.models.libro import Libro


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
}


def extraer_tiempo_entrega_agapea(soup):
    """
    Extrae el tiempo de entrega de la página de Agapea.

    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup con el HTML parseado

    Returns:
        str: El tiempo de entrega (ej: "1 a 15 días") o None si no se encuentra
    """
    # Buscar el div con la clase "etiqueta" que contiene el tiempo de entrega
    etiqueta_div = soup.select_one("div.etiquetas-cont div.etiqueta span")

    if etiqueta_div:
        return etiqueta_div.text

    return None


def scrape_agapea(isbn_libro):
    """Scraper de Agapea utilizando requests y BeautifulSoup."""
    url = f"https://www.agapea.com/buscar/buscador.php?texto={isbn_libro}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"

        if response.status_code != 200:
            print(f"Error al acceder a Agapea (status code: {response.status_code})")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        libros = []

        # Extraer nombre del libro
        nombre_element = soup.select_one("h1")
        nombre = (
            nombre_element.text.strip() if nombre_element else "Nombre no disponible"
        )

        # Extraer precio del libro
        precio_element = soup.select_one(".precio strong")
        precio = 0.0
        gastos_envio = 0.0

        if precio_element:
            precio_texto = precio_element.text.strip()
            precio_limpio = "".join(c for c in precio_texto if c.isdigit() or c in ".,")
            precio_limpio = precio_limpio.replace(",", ".")

            try:
                precio = float(precio_limpio)
            except ValueError:
                precio = 0.0

        # Extraer tiempo de entrega - PASANDO EL OBJETO SOUP
        tiempo_entrega = extraer_tiempo_entrega_agapea(soup)

        # Determinar días hasta entrega
        dias_entrega = "1 a 15 días"
        if tiempo_entrega:
            dias_entrega = tiempo_entrega

        # Determinar gastos de envío
        if precio < 18:
            gastos_envio = 2.95

        # Crear objeto Libro
        libro = Libro(
            nombre=nombre,
            isbn=isbn_libro,
            tienda="Agapea",
            precio=precio,
            gastos_envio=gastos_envio,
            enlace=url,
            fecha_entrega=dias_entrega,
        )
        libros.append(libro)

        return libros

    except Exception as e:
        print(f"Error en Agapea: {e}")
        import traceback

        traceback.print_exc()
        return []
