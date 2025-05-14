from datetime import datetime

import requests
from bs4 import BeautifulSoup
from app.models.libro import Libro


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
}


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
    gastos_envio = 0.0
    precio = 0.0

    for item in soup.select("div.s-result-item"):
        titulo = item.select_one("h2 span")
        precio_entero = item.select_one("span.a-price-whole")
        precio_decimal = item.select_one("span.a-price-fraction")
        link = item.select_one("a.a-link-normal")
        fecha_spans = item.select("span.a-color-base.a-text-bold")

        dias_restantes = 3

        try:
            if precio_entero and precio_decimal:
                precio = float((precio_entero.text + precio_decimal.text).replace(",", "."))
            else:
                print("Precio no encontrado en el elemento.")
                continue

            if precio < 19:
                gastos_envio = 0.99

        except Exception as e:
            print(f"Error procesando el precio: {e}")

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
                    precio=precio,
                    gastos_envio=gastos_envio,
                    enlace= str(link["href"]),
                    fecha_entrega=f"{dias_restantes} días",
                )
            )

        if len(resultados) >= 1:
            break

    return resultados
