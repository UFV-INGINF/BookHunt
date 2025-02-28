<h1 align="center">
  BookHunt
</h1>

<p align="center">
  Aplicación de código abierto en Python que facilita la búsqueda de libros por ISBN, permitiendo a los usuarios comparar precios en distintas tiendas online de manera sencilla.
</p>

<div align="center">
    <img alt="Github repo stars" src="https://img.shields.io/github/stars/carmoruda/BookHunt?color=db6d28&labelColor=202328&style=for-the-badge">
    <img alt="Github repo forks" src="https://img.shields.io/github/forks/carmoruda/BookHunt?color=388bfd&labelColor=202328&style=for-the-badge">
    <img alt="Github repo open issues" src="https://img.shields.io/github/issues/carmoruda/BookHunt?color=f85149&labelColor=202328&style=for-the-badge">
    <img alt="Github repo open pull requests" src="https://img.shields.io/github/issues-pr/carmoruda/BookHunt?color=a371f7&labelColor=202328&style=for-the-badge">
    <br>
    <img alt="code style: black" src="https://img.shields.io/static/v1?label=code%20style&labelColor=202328&message=black&color=black&style=for-the-badge">
    <img alt="pre-commit" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?&color=2ea043&labelColor=202328&style=for-the-badge">
    <br>
    <img alt="Repo size" src="https://img.shields.io/github/repo-size/carmoruda/BookHunt?color=FF69B4&labelColor=202328&style=for-the-badge">
    <img alt="Github last commit (branch)" src="https://img.shields.io/github/last-commit/carmoruda/BookHunt/main?color=C9CC3F&labelColor=202328&label=Last Update%3F&style=for-the-badge">
    <img alt="Github repo license" src="https://img.shields.io/github/license/carmoruda/BookHunt?color=15121C&labelColor=202328&style=for-the-badge">
</div>

## Introducción

Este proyecto tiene como objetivo desarrollar una aplicación web basada en Python que permita a los usuarios comparar precios de libros en múltiples plataformas en línea mediante técnicas de web scraping. La motivación detrás de este proyecto es simplificar el proceso de compra de libros de texto, reduciendo el tiempo y el esfuerzo necesarios para buscar manualmente las mejores ofertas. Al proporcionar una herramienta centralizada para la comparación de precios, la aplicación ayuda a los estudiantes y sus familias a tomar decisiones informadas, optimizando sus compras en función del costo, el tiempo de envío y la disponibilidad.

## Primeros pasos

### 1. Proceso de instalación y ejecución

#### Prerequisitos

-   Tener instalado [Anaconda](https://www.anaconda.com/products/distribution) o [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
-   Git para clonar el repositorio (opcional).

#### Creación del entorno virtual

1. Clona el repositorio (o descárgalo como ZIP):
    ```bash
    git clone https://github.com/carmoruda/BookHunt.git
    cd BookHunt
    ```
2. Crea el entorno a partir del archivo environment.yml:
    ```bash
    conda env create -f environment.yml
    ```
    > _Nota_: Este comando leerá el archivo environment.yml que contiene todas las dependencias necesarias y creará automáticamente el entorno con el nombre especificado en dicho archivo.
3. Activa el entorno recién creado:
    ```bash
    conda activate BookHunt
    ```

#### Ejecución de la aplicación

1. Asegúrate de que el entorno está activado:
    ```bash
    conda activate BookHunt
    ```
2. Navega al directorio de la aplicación:
    ```bash
    cd app
    ```
3. Ejecuta la aplicación:
    ```bash
    python app.py
    ```
4. Abre tu navegador y accede a la dirección http://localhost:8081 para utilizar la aplicación.

### 2. Dependencias de Software

El proyecto BookHunt utiliza las siguientes dependencias principales:

-   **Python 3.12+**: Lenguaje de programación base.
-   **Flask**: Framework web ligero para crear la interfaz de \* usuario y gestionar las rutas.
-   **Playwright**: Biblioteca para automatización de navegadores que permite el web scraping.
-   **Chromium**: Navegador utilizado por Playwright para realizar las consultas web.

### 3. Estructura de directorios

```
BookHunt/
├── app/
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   └── css/
│   │       └── styles.css (implícito)
│   ├── app.py
│   └── scraper.py
└── .gitignore
```
