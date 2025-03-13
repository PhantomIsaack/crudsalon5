#CRUD - Gestión de Alumnos SALON 5

Este proyecto es una aplicación CRUD desarrollada con Flask y PostgreSQL para gestionar información de alumnos. La aplicación permite agregar, editar, listar y eliminar alumnos, mostrando la información en tarjetas ("cards") con un diseño personalizado mediante CSS (archivo `main.css`).

## Tabla de Contenidos

- [Descripción](#descripción)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requerimientos](#requerimientos)
- [Base de Datos](#base-de-datos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso](#uso)
- [Rutas Principales](#rutas-principales)
- [Archivos del Proyecto](#archivos-del-proyecto)
- [Personalización](#personalización)
- [Licencia](#licencia)

## Descripción

La aplicación permite gestionar dos conjuntos de datos:

1. **Datos de Alumnos (`datosalumnos`):**  
   Contiene información personal de cada alumno, como nombre, apellido, dirección, fecha de nacimiento, carrera, teléfono e indicador de estado (activo/inactivo).

2. **Calificaciones de Alumnos (`calificacionesalumnos`):**  
   Almacena registros de calificaciones por semestre para cada alumno. Se espera que cada alumno tenga 7 registros, correspondientes a los semestres: *primero*, *segundo*, *tercero*, *cuarto*, *quinto*, *sexto* y *septimo*.

La interfaz muestra cada alumno en una tarjeta que incluye una imagen genérica (usando un string base64), el nombre, apellido y la carrera.


## Requerimientos

- **Python 3.12** (o superior recomendado)
- **Flask**
- **psycopg2-binary**

Para instalar las dependencias, ejecuta:
pip install -r requirements.txt

cLONA EL REPOSITORIO
git clone https://github.com/PhantomIsaack/crudsalon5
cd flask_crud

python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows

Instalar las dependencias
pip install -r requirements.txt

Uso
python app.py





