from playwright.sync_api import sync_playwright
from app.models.libro import Libro  # si tienes tu clase Libro

def scrape_carrefour_desde_web(isbn):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        isbn = isbn.replace("-", "").strip()
        search_url = f"https://www.carrefour.es/?search={isbn}"
        page.goto(search_url)
        page.wait_for_timeout(4000)

        try:
            producto = page.query_selector("a.product-card-title")
            if not producto:
                print("⚠️ No se encontró el producto.")
                browser.close()
                return []

            titulo = producto.inner_text().strip()
            enlace = producto.get_attribute("href")
            if enlace and not enlace.startswith("http"):
                enlace = "https://www.carrefour.es" + enlace

            if enlace:
                page.goto(enlace)
            else:
                raise ValueError("El enlace es None y no se puede navegar a él.")
            page.wait_for_timeout(3000)

            precio_raw = page.query_selector("span.price")
            precio = float(precio_raw.inner_text().replace("€", "").replace(",", ".").strip()) if precio_raw else 0.0
            gastos_envio = 0.0 if precio >= 19 else 2.99

            libro = Libro(
                nombre=titulo,
                isbn=isbn,
                tienda="Carrefour",
                precio=precio,
                gastos_envio=gastos_envio,
                enlace=enlace,
                fecha_entrega="1 a 3 días"
            )

            browser.close()
            return [libro]

        except Exception as e:
            print(f"❌ Error: {e}")
            browser.close()
            return []

scrape_carrefour_desde_web("9788418174070")
