"""
Sistema de Control de Biblioteca con Flet
Proyecto Final - UIP Campus - Código: 707-00067 - Grupo: 1

Aplicación de escritorio para la gestión de una biblioteca,
con tres secciones principales: Libros, Clientes y Préstamos.
"""

import flet as ft
from modelos import Libro, Cliente


class BibliotecaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Control de Biblioteca"
        self.page.window.width = 900
        self.page.window.height = 700
        self.page.padding = 20
        self.page.theme_mode = ft.ThemeMode.LIGHT

        # Estructura de datos: listas internas que persisten durante la sesión
        self.libros: list[Libro] = []
        self.clientes: list[Cliente] = []

        # Construir la interfaz
        self._construir_ui()

    # =========================================================
    # CONSTRUCCIÓN DE LA INTERFAZ
    # =========================================================
    def _construir_ui(self):
        """Crea la estructura principal con pestañas (patrón de vistas).

        En Flet 0.80+, Tabs actúa como controlador (length + selected_index),
        TabBar muestra la franja de rótulos y TabBarView muestra el cuerpo
        que cambia según la pestaña seleccionada.
        """
        vista_libros = self._vista_libros()
        vista_clientes = self._vista_clientes()
        vista_prestamos = self._vista_prestamos()

        self.tabs = ft.Tabs(
            length=3,
            selected_index=0,
            animation_duration=300,
            content=ft.Column(
                [
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Libros", icon=ft.Icons.BOOK),
                            ft.Tab(label="Clientes", icon=ft.Icons.PEOPLE),
                            ft.Tab(label="Préstamos", icon=ft.Icons.SWAP_HORIZ),
                        ],
                    ),
                    ft.Container(
                        content=ft.TabBarView(
                            controls=[vista_libros, vista_clientes, vista_prestamos],
                        ),
                        expand=True,
                    ),
                ],
                expand=True,
            ),
            expand=True,
        )

        self.page.add(
            ft.Column(
                [
                    ft.Text(
                        "Sistema de Control de Biblioteca",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                    ft.Divider(),
                    self.tabs,
                ],
                expand=True,
            )
        )

    # =========================================================
    # VISTA 1: GESTIÓN DE LIBROS
    # =========================================================
    def _vista_libros(self) -> ft.Container:
        # Campos del formulario
        self.tf_titulo = ft.TextField(label="Título", width=250)
        self.tf_autor = ft.TextField(label="Autor", width=250)
        self.tf_isbn = ft.TextField(label="ISBN", width=200)

        btn_agregar = ft.ElevatedButton(
            "Agregar libro",
            icon=ft.Icons.ADD,
            on_click=self._agregar_libro,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
        )

        # ListView reactivo que muestra los libros
        self.lista_libros = ft.ListView(expand=True, spacing=5, padding=10)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Registro de Libros", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [self.tf_titulo, self.tf_autor, self.tf_isbn, btn_agregar],
                        alignment=ft.MainAxisAlignment.START,
                        wrap=True,
                    ),
                    ft.Divider(),
                    ft.Text("Inventario de Libros", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=self.lista_libros,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                        padding=5,
                        expand=True,
                    ),
                ],
                expand=True,
            ),
            padding=15,
            expand=True,
        )

    def _agregar_libro(self, e):
        """Valida los datos y agrega un libro nuevo al inventario."""
        titulo = self.tf_titulo.value.strip() if self.tf_titulo.value else ""
        autor = self.tf_autor.value.strip() if self.tf_autor.value else ""
        isbn = self.tf_isbn.value.strip() if self.tf_isbn.value else ""

        # Validación: campos obligatorios
        if not titulo or not autor or not isbn:
            self._mostrar_snack("⚠️ Todos los campos son obligatorios", ft.Colors.ORANGE)
            return

        # Validación: ISBN único
        if any(libro.isbn == isbn for libro in self.libros):
            self._mostrar_snack(f"⚠️ Ya existe un libro con ISBN {isbn}", ft.Colors.ORANGE)
            return

        # Crear y agregar libro (estado inicial = Disponible)
        nuevo_libro = Libro(titulo, autor, isbn)
        self.libros.append(nuevo_libro)

        # Limpiar formulario
        self.tf_titulo.value = ""
        self.tf_autor.value = ""
        self.tf_isbn.value = ""

        # Reactividad: actualizar vistas
        self._refrescar_libros()
        self._refrescar_dropdowns_prestamo()
        self._mostrar_snack(f"Libro '{titulo}' agregado", ft.Colors.GREEN)

    def _refrescar_libros(self):
        """Actualiza dinámicamente la ListView de libros."""
        self.lista_libros.controls.clear()

        if not self.libros:
            self.lista_libros.controls.append(
                ft.Text("No hay libros registrados todavía.", italic=True, color=ft.Colors.GREY)
            )
        else:
            for libro in self.libros:
                color_estado = (
                    ft.Colors.GREEN_700 if libro.esta_disponible() else ft.Colors.RED_700
                )
                info_prestamo = ""
                if not libro.esta_disponible() and libro.cliente_prestamo:
                    info_prestamo = f" → Prestado a: {libro.cliente_prestamo.nombre}"

                self.lista_libros.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.BOOK, color=ft.Colors.BLUE_700),
                                ft.Column(
                                    [
                                        ft.Text(libro.titulo, weight=ft.FontWeight.BOLD, size=14),
                                        ft.Text(
                                            f"Autor: {libro.autor}  •  ISBN: {libro.isbn}",
                                            size=12,
                                            color=ft.Colors.GREY_700,
                                        ),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        libro.estado + info_prestamo,
                                        color=ft.Colors.WHITE,
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    bgcolor=color_estado,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                    border_radius=15,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=10,
                        border=ft.border.all(1, ft.Colors.GREY_200),
                        border_radius=8,
                        bgcolor=ft.Colors.WHITE,
                    )
                )
        self.page.update()

    # =========================================================
    # VISTA 2: GESTIÓN DE CLIENTES
    # =========================================================
    def _vista_clientes(self) -> ft.Container:
        self.tf_nombre_cliente = ft.TextField(label="Nombre completo", width=300)
        self.tf_cedula_cliente = ft.TextField(label="Cédula", width=200)

        btn_agregar_cliente = ft.ElevatedButton(
            "Agregar cliente",
            icon=ft.Icons.PERSON_ADD,
            on_click=self._agregar_cliente,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
        )

        self.lista_clientes = ft.ListView(expand=True, spacing=5, padding=10)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Registro de Clientes", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [self.tf_nombre_cliente, self.tf_cedula_cliente, btn_agregar_cliente],
                        alignment=ft.MainAxisAlignment.START,
                        wrap=True,
                    ),
                    ft.Divider(),
                    ft.Text("Lista de Clientes", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=self.lista_clientes,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                        padding=5,
                        expand=True,
                    ),
                ],
                expand=True,
            ),
            padding=15,
            expand=True,
        )

    def _agregar_cliente(self, e):
        nombre = self.tf_nombre_cliente.value.strip() if self.tf_nombre_cliente.value else ""
        cedula = self.tf_cedula_cliente.value.strip() if self.tf_cedula_cliente.value else ""

        if not nombre or not cedula:
            self._mostrar_snack("Nombre y cédula son obligatorios", ft.Colors.ORANGE)
            return

        if any(c.cedula == cedula for c in self.clientes):
            self._mostrar_snack(f"Ya existe un cliente con cédula {cedula}", ft.Colors.ORANGE)
            return

        self.clientes.append(Cliente(nombre, cedula))

        self.tf_nombre_cliente.value = ""
        self.tf_cedula_cliente.value = ""

        self._refrescar_clientes()
        self._refrescar_dropdowns_prestamo()
        self._mostrar_snack(f"Cliente '{nombre}' agregado", ft.Colors.GREEN)

    def _refrescar_clientes(self):
        self.lista_clientes.controls.clear()
        if not self.clientes:
            self.lista_clientes.controls.append(
                ft.Text("No hay clientes registrados todavía.", italic=True, color=ft.Colors.GREY)
            )
        else:
            for cliente in self.clientes:
                self.lista_clientes.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREEN_700),
                                ft.Column(
                                    [
                                        ft.Text(cliente.nombre, weight=ft.FontWeight.BOLD, size=14),
                                        ft.Text(
                                            f"Cédula: {cliente.cedula}",
                                            size=12,
                                            color=ft.Colors.GREY_700,
                                        ),
                                    ],
                                    spacing=2,
                                ),
                            ]
                        ),
                        padding=10,
                        border=ft.border.all(1, ft.Colors.GREY_200),
                        border_radius=8,
                        bgcolor=ft.Colors.WHITE,
                    )
                )
        self.page.update()

    # =========================================================
    # VISTA 3: PRÉSTAMOS Y DEVOLUCIONES
    # =========================================================
    def _vista_prestamos(self) -> ft.Container:
        # Dropdowns de selección
        self.dd_libro_prestamo = ft.Dropdown(
            label="Seleccionar libro disponible", width=350, options=[]
        )
        self.dd_cliente_prestamo = ft.Dropdown(
            label="Seleccionar cliente (por cédula)", width=350, options=[]
        )
        btn_prestar = ft.ElevatedButton(
            "Prestar libro",
            icon=ft.Icons.BOOK_ONLINE,
            on_click=self._realizar_prestamo,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
        )

        # Dropdown y botón de devolución (funcionalidad opcional avanzada)
        self.dd_libro_devolucion = ft.Dropdown(
            label="Seleccionar libro prestado", width=350, options=[]
        )
        btn_devolver = ft.ElevatedButton(
            "Devolver libro",
            icon=ft.Icons.ASSIGNMENT_RETURN,
            on_click=self._realizar_devolucion,
            bgcolor=ft.Colors.ORANGE_600,
            color=ft.Colors.WHITE,
        )

        # Lista de préstamos activos
        self.lista_prestamos = ft.ListView(expand=True, spacing=5, padding=10)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Realizar Préstamo", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([self.dd_libro_prestamo, self.dd_cliente_prestamo, btn_prestar], wrap=True),
                    ft.Divider(),
                    ft.Text("Devolución de Libros", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([self.dd_libro_devolucion, btn_devolver], wrap=True),
                    ft.Divider(),
                    ft.Text("Préstamos Activos", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=self.lista_prestamos,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                        padding=5,
                        expand=True,
                    ),
                ],
                expand=True,
            ),
            padding=15,
            expand=True,
        )

    def _refrescar_dropdowns_prestamo(self):
        """Actualiza los dropdowns cuando cambian las listas."""
        # Libros disponibles para prestar
        self.dd_libro_prestamo.options = [
            ft.dropdown.Option(key=libro.isbn, text=f"{libro.titulo} - {libro.autor}")
            for libro in self.libros
            if libro.esta_disponible()
        ]
        self.dd_libro_prestamo.value = None

        # Clientes disponibles
        self.dd_cliente_prestamo.options = [
            ft.dropdown.Option(key=c.cedula, text=f"{c.cedula} - {c.nombre}")
            for c in self.clientes
        ]
        self.dd_cliente_prestamo.value = None

        # Libros prestados para devolver
        self.dd_libro_devolucion.options = [
            ft.dropdown.Option(key=libro.isbn, text=f"{libro.titulo} - {libro.autor}")
            for libro in self.libros
            if not libro.esta_disponible()
        ]
        self.dd_libro_devolucion.value = None

        self._refrescar_prestamos_activos()
        self.page.update()

    def _realizar_prestamo(self, e):
        isbn = self.dd_libro_prestamo.value
        cedula = self.dd_cliente_prestamo.value

        if not isbn or not cedula:
            self._mostrar_snack("Debes seleccionar un libro y un cliente", ft.Colors.ORANGE)
            return

        libro = next((l for l in self.libros if l.isbn == isbn), None)
        cliente = next((c for c in self.clientes if c.cedula == cedula), None)

        # Validación: solo se prestan libros disponibles
        if not libro or not libro.esta_disponible():
            self._mostrar_snack("El libro no está disponible", ft.Colors.RED)
            return
        if not cliente:
            self._mostrar_snack("Cliente no encontrado", ft.Colors.RED)
            return

        libro.prestar(cliente)

        # Reactividad: actualizar todas las vistas
        self._refrescar_libros()
        self._refrescar_dropdowns_prestamo()
        self._mostrar_snack(
            f"Libro '{libro.titulo}' prestado a {cliente.nombre}", ft.Colors.GREEN
        )

    def _realizar_devolucion(self, e):
        isbn = self.dd_libro_devolucion.value
        if not isbn:
            self._mostrar_snack("Debes seleccionar un libro para devolver", ft.Colors.ORANGE)
            return

        libro = next((l for l in self.libros if l.isbn == isbn), None)
        if not libro:
            self._mostrar_snack("Libro no encontrado", ft.Colors.RED)
            return

        nombre_cliente = libro.cliente_prestamo.nombre if libro.cliente_prestamo else ""
        libro.devolver()

        self._refrescar_libros()
        self._refrescar_dropdowns_prestamo()
        self._mostrar_snack(
            f"Libro '{libro.titulo}' devuelto (estaba con {nombre_cliente})",
            ft.Colors.GREEN,
        )

    def _refrescar_prestamos_activos(self):
        self.lista_prestamos.controls.clear()
        prestados = [l for l in self.libros if not l.esta_disponible()]
        if not prestados:
            self.lista_prestamos.controls.append(
                ft.Text("No hay préstamos activos.", italic=True, color=ft.Colors.GREY)
            )
        else:
            for libro in prestados:
                self.lista_prestamos.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.BOOKMARK, color=ft.Colors.ORANGE_700),
                                ft.Column(
                                    [
                                        ft.Text(
                                            libro.titulo, weight=ft.FontWeight.BOLD, size=14
                                        ),
                                        ft.Text(
                                            f"Prestado a: {libro.cliente_prestamo.nombre} "
                                            f"(Cédula: {libro.cliente_prestamo.cedula})",
                                            size=12,
                                            color=ft.Colors.GREY_700,
                                        ),
                                    ],
                                    spacing=2,
                                ),
                            ]
                        ),
                        padding=10,
                        border=ft.border.all(1, ft.Colors.ORANGE_200),
                        border_radius=8,
                        bgcolor=ft.Colors.ORANGE_50,
                    )
                )

    # =========================================================
    # UTILIDADES
    # =========================================================
    def _mostrar_snack(self, mensaje: str, color):
        """Muestra una notificación temporal al usuario."""
        snack = ft.SnackBar(
            content=ft.Text(mensaje, color=ft.Colors.WHITE),
            bgcolor=color,
        )
        self.page.open(snack)
        self.page.update()


def main(page: ft.Page):
    app = BibliotecaApp(page)
    # Inicializar las vistas
    app._refrescar_libros()
    app._refrescar_clientes()
    app._refrescar_dropdowns_prestamo()


if __name__ == "__main__":
    ft.app(target=main)
