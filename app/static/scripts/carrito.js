// Escuchar cuando el tab "carrito" se activa
document.addEventListener('DOMContentLoaded', function () {
    const carritoTab = document.getElementById('carrito-tab');
    carritoTab.addEventListener('shown.bs.tab', function () {
        mostrarCarrito();
    });

    // Añadir evento a los botones de "Añadir" al carrito
    const botonesAñadir = document.querySelectorAll('.boton-añadir');
    botonesAñadir.forEach(boton => {
        boton.addEventListener('click', function () {
            añadirAlCarrito(boton);
        });
    });
});

// Función para añadir un libro al carrito
function añadirAlCarrito(button) {
    const libroElement = button.closest('.result-container');

    const tienda = libroElement.querySelector('.pill-tienda h6').innerText;
    const nombre = libroElement.querySelector('.container-info-libro h5').innerText;
    const isbn = libroElement.querySelector('.container-info-libro p:nth-child(3)').innerText.replace('ISBN: ', '');
    const precio = parseFloat(libroElement.querySelector('.container-info-precios:nth-child(1) p').innerText.replace('€', '').trim());
    const gastosEnvio = parseFloat(libroElement.querySelector('.container-info-precios:nth-child(2) p').innerText.replace('€', '').trim());
    const tiempoEntrega = libroElement.querySelector('.container-info-precios:nth-child(3) p').innerText;
    const precioTotal = parseFloat(libroElement.querySelector('.container-precio-compra h5').innerText.replace('€', '').trim());
    const enlace = libroElement.querySelector('.boton-ver').parentElement.href;

    const libro = {
        tienda: tienda,
        nombre: nombre,
        isbn: isbn,
        precio: precio,
        gastos_envio: gastosEnvio,
        tiempo_entrega: tiempoEntrega,
        total: precioTotal,
        enlace: enlace
    };

    let carrito = JSON.parse(localStorage.getItem("carritoLibros")) || [];
    const yaExiste = carrito.find((item) => item.isbn === libro.isbn);
    if (yaExiste) {
        alert("Este libro ya está en el carrito.");
        return;
    }

    carrito.push(libro);
    localStorage.setItem("carritoLibros", JSON.stringify(carrito));
    alert("Libro añadido al carrito.");
}

// Función para mostrar los libros del carrito
function mostrarCarrito() {
    const contenedor = document.getElementById("carrito-lista");
    contenedor.innerHTML = "";

    const carrito = JSON.parse(localStorage.getItem("carritoLibros")) || [];

    if (carrito.length === 0) {
        contenedor.innerHTML = "<p>No hay libros en el carrito.</p>";
        return;
    }

    carrito.forEach(libro => {
        const item = document.createElement("div");
        item.classList.add("item-carrito");

        item.innerHTML = `
        <div class="info-libro-carrito">
            <h5>${libro.nombre}</h5>
            <p><strong>ISBN:</strong> ${libro.isbn}</p>
            <p><strong>Tienda:</strong> ${libro.tienda}</p>
            <p><strong>Tiempo de entrega:</strong> ${libro.tiempo_entrega}</p>
        </div>
        <div class="precios-carrito">
            <p><strong>Precio:</strong> ${libro.precio}€</p>
            <p><strong>Gastos de envío:</strong> ${libro.gastos_envio}€</p>
            <p class="total-carrito"><strong>Total:</strong> ${libro.total}€</p>
        </div>
        <div class="acciones-carrito">
            <a href="${libro.enlace}" target="_blank"><button class="boton-ver">Ver oferta</button></a>
            <button class="boton-quitar" onclick="quitarDelCarrito('${libro.isbn}')">Quitar</button>
        </div>
      `;
        contenedor.appendChild(item);
    });
}

// Función para quitar un libro del carrito
function quitarDelCarrito(isbn) {
    const carrito = JSON.parse(localStorage.getItem("carritoLibros")) || [];
    const nuevoCarrito = carrito.filter(libro => libro.isbn !== isbn);
    localStorage.setItem("carritoLibros", JSON.stringify(nuevoCarrito));
    mostrarCarrito();
}

// Función para limpiar todo el carrito
function clearCarrito() {
    localStorage.removeItem("carritoLibros");
    mostrarCarrito();
    alert("Carrito eliminado.");
}
