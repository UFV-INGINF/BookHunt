from app.services.agapea import scrape_agapea
from app.services.amazon import scrape_amazon
from app.services.corte_ingles import scrape_el_corte_ingles
from app.services.iberlibro import scrape_iberlibro
from app.services.la_casa_del_libro import scrape_casa_del_libro
from app.utilities.formatear_isbn import formatear_isbn


def scrapear_libros(isbn_libro):
    libros = []

    isbn_libro = formatear_isbn(isbn_libro)

    respuesta_casa_del_libro = scrape_casa_del_libro(isbn_libro)
    if respuesta_casa_del_libro:
        libros += respuesta_casa_del_libro

    # libros += scrape_iberlibro(isbn_libro)
    # libros += scrape_agapea(isbn_libro)
    # libros += scrape_amazon(isbn_libro)
    # libros += scrape_el_corte_ingles(isbn_libro)
    return libros


#isbn_libro = "9788467033540"
#libros = scrapear_libros(isbn_libro)

#for libro in libros:
 #   print(
  #      f"Nombre: {libro.nombre}, ISBN: {libro.isbn}, Tienda: {libro.tienda}, Precio: {libro.precio}, Total: {libro.total}, Enlace: {libro.enlace}. Gastos de envío: {libro.gastos_envio}"
   # )
