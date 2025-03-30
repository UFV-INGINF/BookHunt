def formatear_isbn(isbn):
    """
    Formatea un ISBN añadiendo un guión después del prefijo.

    Args:
        isbn (str): El ISBN sin formatear (ej. '9788467586930')

    Returns:
        str: El ISBN formateado (ej. '978-8467586930')
    """
    # Eliminar cualquier guión existente y espacios
    isbn_limpio = isbn.replace("-", "").replace(" ", "")

    # Si el ISBN tiene 13 dígitos (ISBN-13), añadir guión después de los primeros 3 dígitos
    if len(isbn_limpio) == 13:
        return f"{isbn_limpio[:3]}-{isbn_limpio[3:]}"

    # Si el ISBN tiene 10 dígitos (ISBN-10), dejarlo sin cambios
    return isbn_limpio
