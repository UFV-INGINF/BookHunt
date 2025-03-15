from playwright.sync_api import sync_playwright  # type: ignore
import re
import requests


class Libro:
    def __init__(
        self,
        nombre="Error de Carga",
        tienda="Error de Carga",
        precio=0.0,
        isbn=0,
        gastos_envio=0.0,
        enlace="",
    ):
        self.nombre = nombre
        self.isbn = isbn
        self.tienda = tienda
        self.precio = precio
        self.enlace = enlace
        self.gastos_envio = gastos_envio
        self.total = self.calc_total()

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

    response = requests.get(
        url_libro,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        },
    )

    # Extraer la información de la etiqueta title
    title_match = re.search(r"<title>(.*?)</title>", response.text)
    book_title = "Nombre no disponible"
    price = 0.0

    if title_match:
        title_content = title_match.group(1)
        # El formato esperado es: "TÍTULO | AUTOR | EDITORIAL | Casa del Libro"
        parts = title_content.split(" | ")

        if len(parts) >= 3:
            book_title = parts[0].strip()
            author = parts[1].strip()
            editorial = parts[2].strip() if len(parts) > 2 else "N/A"

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
        gastos_envio=0.0,
        enlace=enlace,  # Añadir el enlace de búsqueda
    )
    libros.append(libro)

    return libros


def scrape_iberlibro(isbn_libro):
    url = f"https://www.iberlibro.com/servlet/SearchResults?ds=20&kn={isbn_libro}&sts=t"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)
        page.wait_for_load_state("networkidle", timeout=10000)
        page.wait_for_selector('span[data-test-id="listing-title"]', timeout=10000)

        item = page.query_selector("li.result-item")

        libros = []
        if item:
            try:
                nombre_element = item.query_selector(
                    'span[data-test-id="listing-title"]'
                )
                if nombre_element:
                    nombre = nombre_element.inner_text().strip()
                else:
                    nombre = "Nombre no disponible"

                precio_element = item.query_selector('p[data-test-id="item-price"]')
                if precio_element:
                    precio_texto = precio_element.inner_text().strip()
                    precio = float(
                        precio_texto.replace("EUR", "").replace(",", ".").strip()
                    )
                else:
                    precio = 0.0

                # El enlace será el de la página de búsqueda de Iberlibro
                enlace = f"https://www.iberlibro.com/servlet/SearchResults?ds=20&kn={isbn_libro}&sts=t"

                libro = Libro(
                    nombre=nombre,
                    isbn=isbn_libro,
                    tienda="Iberlibro",
                    precio=precio,
                    gastos_envio=0,
                    enlace=enlace,  # Añadir el enlace de búsqueda de Iberlibro
                )
                libros.append(libro)

            except Exception as e:
                print(f"Error al extraer información de un libro de Iberlibro: {e}")

        browser.close()

    return libros


def scrape_agapea(isbn_libro):
    url = f"https://www.agapea.com/buscar/buscador.php?texto={isbn_libro}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
        }
        page.set_extra_http_headers(headers)
        page.goto(url)
        page.wait_for_load_state("domcontentloaded", timeout=10000)

        libros = []

        try:

            nombre_element = page.query_selector("h1")
            nombre = (
                nombre_element.inner_text().strip()
                if nombre_element
                else "Nombre no disponible"
            )
            precio_element = page.query_selector(".precio strong")
            precio_texto = (
                precio_element.inner_text().strip() if precio_element else "0"
            )
            precio = float(precio_texto.replace("€", "").replace(",", ".").strip())
            envio_element = page.query_selector(".envio-gratis")
            gastos_envio = (
                0 if envio_element else 3.99
            )  # Suponiendo que el envío cuesta 3.99 si no es gratis

            libro = Libro(
                nombre=nombre,
                isbn=isbn_libro,
                tienda="Agapea",
                precio=precio,
                gastos_envio=gastos_envio,
                enlace=url,
            )

            libros.append(libro)

        except Exception as e:
            print(f"Error general en Agapea: {e}")
        browser.close()

    return libros


def scrapear_libros(isbn_libro):
    libros = []

    libros += scrape_casa_del_libro(isbn_libro)
    libros += scrape_iberlibro(isbn_libro)
    libros += scrape_agapea(isbn_libro)
    return libros


isbn_libro = "9788467033540"
libros = scrapear_libros(isbn_libro)

for libro in libros:
    print(
        f"Nombre: {libro.nombre}, ISBN: {libro.isbn}, Tienda: {libro.tienda}, Precio: {libro.precio}, Total: {libro.total}, Enlace: {libro.enlace}. Gastos de envío: {libro.gastos_envio}"
    )
