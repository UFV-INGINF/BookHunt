import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from utilities.formatear_isbn import formatear_isbn


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
}


class Libro:
    def __init__(
        self,
        nombre="Error de Carga",
        tienda="Error de Carga",
        precio=0.0,
        isbn=0,
        gastos_envio=0.0,
        enlace="",
        fecha_entrega=0,
    ):
        self.nombre = nombre
        self.isbn = isbn
        self.tienda = tienda
        self.precio = precio
        self.enlace = enlace
        self.gastos_envio = gastos_envio
        self.total = self.calc_total()
        self.fecha_entrega = fecha_entrega

    def calc_total(self):
        return self.precio + self.gastos_envio


def obtener_link_libro_playwright_casalibro(isbn):
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

    # El enlace será el de la página del libro (no de búsqueda)
    enlace = url_libro
    libro = Libro(
        nombre=book_title.capitalize(),
        isbn=isbn_libro,
        tienda="La Casa del Libro",
        precio=price,
        gastos_envio=0,
        enlace=enlace,  # Añadir el enlace de búsqueda
        fecha_entrega=0,
    )
    libros.append(libro)

    return libros


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
            if precio_element:
                precio_texto = precio_element.text.strip()
                precio = float(
                    precio_texto.replace("EUR", "").replace(",", ".").strip()
                )
            else:
                precio = 0.0

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
                precio=precio,
                gastos_envio=0,  # Iberlibro generalmente no muestra gastos de envío en la página de resultados
                enlace=enlace,
                fecha_entrega=0,  # Iberlibro no suele mostrar fechas de entrega en resultados
            )
            libros.append(libro)

        except Exception as e:
            print(f"Error al extraer información de un libro de Iberlibro: {e}")
    else:
        print(f"No se encontraron resultados para el ISBN {isbn_libro} en Iberlibro")

    return libros


def scrape_agapea(isbn_libro):
    """Scraper de Agapea utilizando requests y BeautifulSoup."""
    url = f"https://www.agapea.com/buscar/buscador.php?texto={isbn_libro}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
    }

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


def scrape_amazon(isbn):
    meses = {
        "ene": "Jan",
        "feb": "Feb",
        "mar": "Mar",
        "abr": "Apr",
        "may": "May",
        "jun": "Jun",
        "jul": "Jul",
        "ago": "Aug",
        "sep": "Sep",
        "oct": "Oct",
        "nov": "Nov",
        "dic": "Dec",
    }

    url = f"https://www.amazon.es/s?k={isbn}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error al acceder a Amazon (status code: {response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    resultados = []

    for item in soup.select("div.s-result-item"):
        titulo = item.select_one("h2 span")
        precio_entero = item.select_one("span.a-price-whole")
        precio_decimal = item.select_one("span.a-price-fraction")
        link = item.select_one("a.a-link-normal")
        fecha_spans = item.select("span.a-color-base.a-text-bold")

        dias_restantes = 3

        if fecha_spans:
            fecha_texto = None
            for span in fecha_spans:
                if "," in span.text and "de" in span.text:
                    fecha_texto = span.text.strip()
                    break

            if fecha_texto:
                try:
                    # Extraer componentes de la fecha
                    partes = fecha_texto.split()
                    if len(partes) >= 4 and "de" in fecha_texto:
                        # Formato esperado: "jue, 3 de abr"
                        dia_numero = partes[1].replace(",", "")  # Quitar la coma
                        mes = partes[3]  # "abr"

                        if mes in meses:
                            fecha_formateada = (
                                f"{dia_numero} {meses[mes]} {datetime.now().year}"
                            )
                            fecha_objetivo = datetime.strptime(
                                fecha_formateada, "%d %b %Y"
                            )
                            hoy = datetime.now()
                            dias_restantes = (fecha_objetivo - hoy).days

                            # Si la fecha ya pasó, asumimos que es para el próximo año
                            if dias_restantes < 0:
                                fecha_objetivo = datetime(
                                    hoy.year + 1,
                                    fecha_objetivo.month,
                                    fecha_objetivo.day,
                                )
                                dias_restantes = (fecha_objetivo - hoy).days

                            print(
                                f"Fecha de entrega encontrada: {fecha_texto}, días restantes: {dias_restantes}"
                            )
                    else:
                        print(f"Formato de fecha no reconocido: {fecha_texto}")
                except Exception as e:
                    print(f"Error procesando la fecha: {e}")
            else:
                print("No se encontró texto de fecha en los spans")
        else:
            print("No se encontraron spans con la clase necesaria")

        if titulo and precio_entero and link:
            resultados.append(
                Libro(
                    nombre=titulo.text.strip(),
                    isbn=isbn,
                    tienda="Amazon",
                    precio=float(
                        (precio_entero.text + precio_decimal.text).replace(",", ".")
                    ),
                    gastos_envio=0,
                    enlace="https://amazon.es" + link["href"],
                    fecha_entrega=dias_restantes,
                )
            )

        if len(resultados) >= 1:
            break

    return resultados


def scrapear_libros(isbn_libro):
    libros = []

    isbn_libro = formatear_isbn(isbn_libro)

    libros += scrape_casa_del_libro(isbn_libro)
    libros += scrape_iberlibro(isbn_libro)
    libros += scrape_agapea(isbn_libro)
    libros += scrape_amazon(isbn_libro)
    return libros


# isbn_libro = "9788467033540"
# libros = scrapear_libros(isbn_libro)

# for libro in libros:
#     print(
#         f"Nombre: {libro.nombre}, ISBN: {libro.isbn}, Tienda: {libro.tienda}, Precio: {libro.precio}, Total: {libro.total}, Enlace: {libro.enlace}. Gastos de envío: {libro.gastos_envio}"
#     )
