import requests
from bs4 import BeautifulSoup
from models.libro import Libro


def scrape_fnac(isbn_libro):
    """Scraper de FNAC utilizando requests y BeautifulSoup."""
    url = f"https://www.fnac.es/SearchResult/ResultList.aspx?SCat=0!1&Search={isbn_libro}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
    }

    response = requests.get(url, headers=headers)
    libros = []

    if response.status_code != 200:
        print(f"Error al acceder a FNAC (status code: {response.status_code})")
        return libros

    soup = BeautifulSoup(response.text, "html.parser")
    item = soup.select_one(".Article-itemGroup")

    if item:
        try:
            nombre_element = item.select_one(".Article-title")
            nombre = (
                nombre_element.get_text(strip=True)
                if nombre_element
                else "Nombre no disponible"
            )

            precio_element = item.select_one(".userPrice")
            if precio_element:
                precio_texto = precio_element.get_text(strip=True)
                precio = float(
                    precio_texto.replace("€", "").replace(",", ".").strip()
                )
            else:
                precio = 0.0

            gastos_envio = 0.0  

            link_element = item.select_one(".Article-title a")
            enlace = (
                "https://www.fnac.es" + link_element["href"]
                if link_element and "href" in link_element.attrs
                else url
            )

            libro = Libro(
                nombre=nombre,
                isbn=isbn_libro,
                tienda="FNAC",
                precio=precio,
                gastos_envio=gastos_envio,
                enlace=enlace,
                fecha_entrega=0,
            )
            libros.append(libro)

        except Exception as e:
            print(f"Error al extraer información de un libro de FNAC: {e}")
    else:
        print(f"No se encontraron resultados para el ISBN {isbn_libro} en FNAC")

    return libros
