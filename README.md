# ProyectoFinal_GrupoB

# Sistema de Control de Biblioteca con Flet

Proyecto Final - UIP Campus - Código: 707-00067 - Grupo: B

## Descripción

Aplicación de escritorio para la gestión de una biblioteca, desarrollada con **Python** y el framework **Flet**. Permite gestionar libros, clientes y préstamos con una interfaz reactiva e intuitiva.

## Estructura del proyecto

```
biblioteca_app/
├── main.py        # Aplicación principal de Flet
├── modelos.py     # Clases Libro y Cliente (módulos de datos)
└── README.md      # Este archivo
```

## Requisitos

- Python 3.9 o superior
- Flet

## Instalación

1. Instala Flet:

```bash
pip install flet
pip install flet-desktop
```

## Ejecución

Desde la carpeta del proyecto ejecuta:

```bash
python main.py
```

Se abrirá una ventana de escritorio con la aplicación.

## Funcionalidades

### 1. Gestión de Libros (pestaña 📚 Libros)
- Registrar libros nuevos con Título, Autor e ISBN (único).
- Los libros se agregan con estado inicial "Disponible".
- Visualización dinámica del inventario completo con su estado.

### 2. Gestión de Clientes (pestaña 👤 Clientes)
- Registrar clientes con nombre y cédula (única).
- Lista dinámica de todos los clientes registrados.

### 3. Préstamos y Devoluciones (pestaña 🔄 Préstamos)
- **Préstamo**: seleccionar un libro disponible (dropdown) y un cliente (dropdown por cédula). Al confirmar, el estado del libro cambia a "Prestado".
- **Devolución**: seleccionar un libro prestado y cambiar su estado de vuelta a "Disponible".
- Vista de préstamos activos con nombre y cédula del cliente que tiene cada libro.

## Validaciones implementadas

- Todos los campos obligatorios deben completarse.
- ISBN único para cada libro.
- Cédula única para cada cliente.
- Solo pueden prestarse libros con estado "Disponible".
- Solo pueden devolverse libros con estado "Prestado".

## Arquitectura

- **Módulos de datos**: las clases `Libro` y `Cliente` en `modelos.py` encapsulan la información.
- **Persistencia en sesión**: los datos se mantienen en listas internas durante la ejecución (similar al ejemplo de To-Do List de Flet).
- **Reactividad**: la interfaz se actualiza automáticamente al agregar o modificar datos usando `page.update()`.
- **Patrón de vistas**: las tres funcionalidades se manejan como pestañas (`ft.Tabs`) dentro de la aplicación principal.

- ## Aportes

- Israel Perez: Implementación de validaciones para ISBN (mínimo 5 caracteres) y cédula (solo números).
