"""
Módulos de Datos: Clases Libro y Cliente
Proyecto Final - Sistema de Control de Biblioteca con Flet
"""


class Libro:
    """Representa un libro en el inventario de la biblioteca."""

    ESTADO_DISPONIBLE = "Disponible"
    ESTADO_PRESTADO = "Prestado"

    def __init__(self, titulo: str, autor: str, isbn: str):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn  # Identificador único
        self.estado = Libro.ESTADO_DISPONIBLE
        self.cliente_prestamo = None  # Referencia al cliente si está prestado

    def prestar(self, cliente):
        """Cambia el estado del libro a prestado y lo asocia a un cliente."""
        if self.estado != Libro.ESTADO_DISPONIBLE:
            return False
        self.estado = Libro.ESTADO_PRESTADO
        self.cliente_prestamo = cliente
        return True

    def devolver(self):
        """Cambia el estado del libro de vuelta a Disponible."""
        if self.estado != Libro.ESTADO_PRESTADO:
            return False
        self.estado = Libro.ESTADO_DISPONIBLE
        self.cliente_prestamo = None
        return True

    def esta_disponible(self) -> bool:
        return self.estado == Libro.ESTADO_DISPONIBLE

    def __str__(self):
        return f"{self.titulo} - {self.autor} [{self.estado}]"


class Cliente:
    """Representa un cliente de la biblioteca."""

    def __init__(self, nombre: str, cedula: str):
        self.nombre = nombre
        self.cedula = cedula  # Identificador único

    def __str__(self):
        return f"{self.nombre} (Cédula: {self.cedula})"