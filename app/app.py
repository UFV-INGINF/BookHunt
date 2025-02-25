from flask import Flask, render_template, request # type: ignore

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST']) # Vistas, en este caso raíz
def index():
    class Libro():
        def __init__(self, nombre='Error de Carga', tienda = 'Error de Carga', precio=0.0, gastos_envio=0.0):
            self.nombre = nombre
            self.tienda = tienda
            self.precio = precio
            self.gastos_envio = gastos_envio
            self.total = self.calc_total()

        def calc_total(self):
            return self.precio + self.gastos_envio   

    libros = [
        Libro(nombre="La Celestina", tienda="Amazon", precio=25.5, gastos_envio=5.0),
        Libro(nombre="La Celestina", tienda="Fnac", precio=28.0, gastos_envio=3.0),
        Libro(nombre="La Celestina", tienda="eBay", precio=24.0, gastos_envio=6.5),
        Libro(nombre="La Celestina", tienda="La Casa del Libro", precio=25.5, gastos_envio=3.0),
        Libro(nombre="La Celestina", tienda="Ibero", precio=23.0, gastos_envio=7.0)
    ]

    libros.sort(key=lambda libro: libro.total)

    if request.method == 'POST':
        query = request.form.get('nombre_libro', '').lower()  # Obtener el término de búsqueda
        
        libros = [libro for libro in libros if query in libro.nombre.lower()]


    return render_template('index.html', libros=libros)

if __name__ == '__main__':
    app.run(debug=True,port=8081)