class Libro:
    def __init__(
        self,
        nombre="Error de Carga",
        tienda="Error de Carga",
        precio=0.0,
        isbn=0,
        gastos_envio=0.0,
        enlace="",
        fecha_entrega="0 días",
    ):
        self.nombre = nombre
        self.isbn = isbn
        self.tienda = tienda
        self.precio = precio
        self.enlace = enlace
        self.gastos_envio = gastos_envio
        self.total = self.calc_total()
        self.fecha_entrega = fecha_entrega

    def calc_total(self):
        return round(self.precio + self.gastos_envio, 2)
