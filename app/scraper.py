from services.agapea import scrape_agapea
from services.amazon import scrape_amazon
from services.iberlibro import scrape_iberlibro
from services.la_casa_del_libro import scrape_casa_del_libro
from utilities.formatear_isbn import formatear_isbn


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
