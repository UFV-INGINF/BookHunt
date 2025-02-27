from playwright.sync_api import sync_playwright # type: ignore

class Libro:
    def __init__(self, nombre='Error de Carga', tienda='Error de Carga', precio=0.0, isbn=0, gastos_envio=0.0, enlace = ''):
        self.nombre = nombre
        self.isbn = isbn
        self.tienda = tienda
        self.precio = precio
        self.enlace = enlace
        self.gastos_envio = gastos_envio
        self.total = self.calc_total()

    def calc_total(self):
        return self.precio + self.gastos_envio

def scrape_casa_del_libro(isbn_libro):
    url = f"https://www.casadellibro.com/?query={isbn_libro}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
        }
        page.set_extra_http_headers(headers)

        page.goto(url)

        # Esperar hasta que el contenido de la página esté completamente cargado
        page.wait_for_load_state('domcontentloaded', timeout=30000)

        libros = []

        try:
            page.wait_for_selector('.x-result__description', timeout=10000)

            items = page.query_selector_all('.x-result__description')

            for item in items:
                try:
                    nombre_element = item.query_selector('h2[data-test="result-title"]')
                    if nombre_element:
                        nombre = nombre_element.inner_text().strip()
                    else:
                        nombre = "Nombre no disponible"

                    precio_element = item.query_selector('.x-currency')
                    if precio_element:
                        precio = precio_element.inner_text().strip().replace("€", "").replace(",", ".")
                    else:
                        precio = "0.0"

                    try:
                        precio = float(precio)
                    except ValueError:
                        precio = 0.0

                    # El enlace será el de la página de búsqueda
                    enlace = f"https://www.casadellibro.com/?query={isbn_libro}"

                    libro = Libro(
                        nombre=nombre,
                        isbn=isbn_libro,
                        tienda="La Casa del Libro",
                        precio=precio,
                        gastos_envio=3.0,
                        enlace=enlace  # Añadir el enlace de búsqueda
                    )
                    libros.append(libro)
                except Exception as e:
                    print(f"Error al extraer información de un producto: {e}")

        except Exception as e:
            print(f"Error general: {e}")

        browser.close()
    return libros


def scrape_iberlibro(isbn_libro):
    url = f"https://www.iberlibro.com/servlet/SearchResults?ds=20&kn={isbn_libro}&sts=t"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)
        page.wait_for_load_state('networkidle', timeout=10000)
        page.wait_for_selector('span[data-test-id="listing-title"]', timeout=10000)

        item = page.query_selector('li.result-item')

        libros = []
        if item:
            try:
                nombre_element = item.query_selector('span[data-test-id="listing-title"]')
                if nombre_element:
                    nombre = nombre_element.inner_text().strip()
                else:
                    nombre = "Nombre no disponible"
                
                precio_element = item.query_selector('p[data-test-id="item-price"]')
                if precio_element:
                    precio_texto = precio_element.inner_text().strip()
                    precio = float(precio_texto.replace('EUR', '').replace(',', '.').strip())
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
                    enlace=enlace  # Añadir el enlace de búsqueda de Iberlibro
                )
                libros.append(libro)

            except Exception as e:
                print(f"Error al extraer información de un libro de Iberlibro: {e}")
        
        browser.close()

    return libros




def scrapear_libros(isbn_libro):
    libros = []

    libros += scrape_casa_del_libro(isbn_libro)
    libros += scrape_iberlibro(isbn_libro)

    return libros

isbn_libro = "9788467033540"
libros = scrapear_libros(isbn_libro)

for libro in libros:
    print(f"Nombre: {libro.nombre}, ISBN: {libro.isbn}, Tienda: {libro.tienda}, Precio: {libro.precio}, Total: {libro.total}, Enlace: {libro.enlace}")
