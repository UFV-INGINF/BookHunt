from random import randrange
from typing import Callable, TypeVar, List


T = TypeVar("T")  # Tipo genérico para la colección


def quick_sort(coleccion: List[T], key: Callable[[T], any] = None) -> List[T]:
    """Implementación del algoritmo de ordenamiento QuickSort con soporte para key function.

    Args:
        coleccion (List[T]): Colección de elementos a ordenar.
        key (Callable[[T], any], optional): Función que extrae un valor para comparación.

    Returns:
        List[T]: La misma colección pero ordenada.
    """

    # Crear una función de comparación basada en key
    def get_value(item):
        return item if key is None else key(item)

    # Caso base: La colección tiene 0 o 1 elementos
    if len(coleccion) < 2:
        return coleccion

    # Copia para evitar modificar la original
    coleccion_ordenar = coleccion.copy()

    # Elegir un pivote aleatorio
    indice_pivote = randrange(len(coleccion_ordenar))
    pivote = coleccion_ordenar.pop(indice_pivote)

    # Dividir la colección según la key function
    menores = [
        item for item in coleccion_ordenar if get_value(item) <= get_value(pivote)
    ]
    mayores = [
        item for item in coleccion_ordenar if get_value(item) > get_value(pivote)
    ]

    # Recursión y combinación
    return [*quick_sort(menores, key), pivote, *quick_sort(mayores, key)]


def ordenar_libros(libros, criterio="precio"):
    """Ordena una lista de libros según el criterio especificado.

    Args:
        libros (list): Lista de objetos Libro.
        criterio (str): Criterio de ordenación ('precio', 'nombre', etc.).

    Returns:
        list: Lista de libros ordenada.
    """
    if not libros:
        return []

    if criterio == "precio":
        return quick_sort(libros, key=lambda libro: libro.precio)
    elif criterio == "nombre":
        return quick_sort(libros, key=lambda libro: libro.nombre.lower())
    elif criterio == "total":
        return quick_sort(libros, key=lambda libro: libro.total)
    else:
        return libros
