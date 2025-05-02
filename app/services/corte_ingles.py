from playwright.sync_api import sync_playwright
from models.libro import Libro


def scrape_el_corte_ingles(isbn_libro):
    """Scraper de El Corte Inglés utilizando Playwright."""
    libros = []
    isbn_libro = isbn_libro.replace("-", "")  # Por si acaso viene con guiones
    url = f"https://www.elcorteingles.es/libros/search-nwx/1/?s={isbn_libro}&stype=text_box"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:

            page.goto(url, timeout=60000)
            page.wait_for_selector("div.product_preview-ppal", timeout=10000)

            # Coge el primer resultado
            nombre_element = page.query_selector("a.product_preview-title")
            precio_element = page.query_selector("span.price-sale")
            link_element = url

            if nombre_element and precio_element and link_element:
                nombre = nombre_element.inner_text().strip()
                precio_text = precio_element.inner_text().strip()
                enlace = link_element

                precio = float(
                    precio_text.replace("€", "").replace(",", ".").strip()
                )

                libro = Libro(
                    nombre=nombre,
                    isbn=isbn_libro,
                    tienda="El Corte Inglés",
                    precio=precio,
                    gastos_envio=0.0,  # No lo indican fácil
                    enlace=enlace,
                    fecha_entrega= "No hay información",
                )
                libros.append(libro)
            else:
                print(f"No se encontró libro para ISBN {isbn_libro} en El Corte Inglés.")

        except Exception as e:
            print(f"Error al scrapear El Corte Inglés: {e}")

        finally:
            browser.close()

    return libros

