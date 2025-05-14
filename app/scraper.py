from app.services.agapea import scrape_agapea
from app.services.amazon import scrape_amazon
from app.services.el_corte_ingles import scrape_el_corte_ingles
from app.services.iberlibro import scrape_iberlibro
from app.services.la_casa_del_libro import scrape_casa_del_libro
from app.utilities.formatear_isbn import formatear_isbn


def scrapear_libros(isbn_libro):
    libros = []

    isbn_libro = formatear_isbn(isbn_libro)

    respuesta_casa_del_libro = scrape_casa_del_libro(isbn_libro)
    if isinstance(respuesta_casa_del_libro, list):
        libros += respuesta_casa_del_libro

    respuesta_corte_ingles = scrape_el_corte_ingles(isbn_libro)
    if isinstance(respuesta_corte_ingles, list):
        libros += respuesta_corte_ingles

    respuesta_iberlibro = scrape_iberlibro(isbn_libro)
    if isinstance(respuesta_iberlibro, list):
        libros += respuesta_iberlibro

    respuesta_agapea = scrape_agapea(isbn_libro)
    if isinstance(respuesta_agapea, list):
        libros += respuesta_agapea

    respuesta_amazon = scrape_amazon(isbn_libro)
    if isinstance(respuesta_amazon, list):
        libros += respuesta_amazon

    return libros


#isbn_libro = "9788467033540"
#libros = scrapear_libros(isbn_libro)

#for libro in libros:
 #   print(
  #      f"Nombre: {libro.nombre}, ISBN: {libro.isbn}, Tienda: {libro.tienda}, Precio: {libro.precio}, Total: {libro.total}, Enlace: {libro.enlace}. Gastos de envío: {libro.gastos_envio}"
   # )
