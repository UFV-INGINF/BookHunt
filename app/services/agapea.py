import requests
from bs4 import BeautifulSoup
from models.libro import Libro


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
}


def scrape_agapea(isbn_libro):
    """Scraper de Agapea utilizando requests y BeautifulSoup."""
    url = f"https://www.agapea.com/buscar/buscador.php?texto={isbn_libro}"

    try:
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"  # Forzar codificación UTF-8

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

        if precio_element:
            # Limpiar el texto del precio de caracteres no deseados
            precio_texto = precio_element.text.strip()
            # Eliminar todos los caracteres excepto dígitos, punto y coma
            precio_limpio = "".join(c for c in precio_texto if c.isdigit() or c in ".,")
            # Reemplazar coma por punto para formato flotante
            precio_limpio = precio_limpio.replace(",", ".")

            try:
                # Intentar convertir a float
                precio = float(precio_limpio)
            except ValueError:
                print(f"No se pudo convertir el precio: '{precio_texto}' a float")
                precio = 0.0

        # Verificar si el envío es gratis
        envio_element = soup.select_one(".envio-gratis")
        gastos_envio = 0 if envio_element else 3.99

        # Crear objeto Libro
        libro = Libro(
            nombre=nombre,
            isbn=isbn_libro,
            tienda="Agapea",
            precio=precio,
            gastos_envio=gastos_envio,
            enlace=url,
            fecha_entrega=0,
        )
        libros.append(libro)

        return libros

    except Exception as e:
        print(f"Error general en Agapea: {e}")
        return []
