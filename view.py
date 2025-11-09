import os
from gi import require_version
require_version('Gtk', '4.0')
from gi.repository import Gtk

class View(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="SplitWithMe")
        self.set_default_size(1000, 500)

        self.stack = Gtk.Stack()
        self.set_child(self.stack)

        # Páginas principales
        self.stack.add_titled(self.page_home(), "home", "Inicio")
        self.stack.add_titled(self.page_amigos(), "amigos", "Amigos")
        self.stack.add_titled(self.page_gastos(), "gastos", "Gastos")
        self.stack.add_titled(self.page_balance(), "balance", "Balance")

        # Páginas amigos
        self.stack.add_titled(self.page_crear_amigo(), "crear_amigo", "Crear amigo")
        self.stack.add_titled(self.page_editar_amigo(), "editar_amigo", "Editar amigo")
        self.stack.add_titled(self.page_detalles_amigo(), "detalles_amigo", "Detalles del amigo")
        self.stack.add_titled(self.page_gastos_amigo(), "gastos_amigo", "Gastos del amigo")

        # Páginas ver gastos 
        self.stack.add_titled(self.page_crear_gasto(), "crear_gasto", "Crear gasto")
        self.stack.add_titled(self.page_participantes_gasto(), "participantes_gasto", "Participantes del gasto")
        self.stack.add_titled(self.page_detalles_gasto(), "detalles_gasto", "Detalles del gasto")

        self.stack.add_titled(self.page_añadir_participante(), "añadir_participante", "Añadir participante")

        # Conectar un handler cuando cambie la página visible
        # Cuando volvamos a "amigos" o a "gastos" queremos limpiar las opciones abiertas
        self.stack.connect("notify::visible-child-name", self.on_stack_visible_child_changed)

        self.stack.set_visible_child_name("home")

    # -------------------------------------------------------------------------
    # Handler para cambios de página en el Stack
    # -------------------------------------------------------------------------
    def on_stack_visible_child_changed(self, stack, pspec):
        """
        Se ejecuta cada vez que cambia la página visible del Stack.
        Si la página visible es 'amigos' o 'gastos', limpia las cajas de
        opciones correspondientes para que no queden abiertas al volver.
        """
        name = stack.get_visible_child_name()
        if name == "amigos":
            self._clear_contenedor_opciones_amigo()
        elif name == "gastos":
            self._clear_contenedor_opciones_gasto()

    def _clear_contenedor_opciones_amigo(self):
        """Elimina todos los children del contenedor de opciones de amigo (si existe)."""
        if hasattr(self, "contenedor_opciones_amigo") and self.contenedor_opciones_amigo is not None:
            for child in list(self.contenedor_opciones_amigo):
                try:
                    self.contenedor_opciones_amigo.remove(child)
                except Exception:
                    pass

    def _clear_contenedor_opciones_gasto(self):
        """Elimina todos los children del contenedor de opciones de gasto (si existe)."""
        if hasattr(self, "contenedor_opciones_gasto") and self.contenedor_opciones_gasto is not None:
            for child in list(self.contenedor_opciones_gasto):
                try:
                    self.contenedor_opciones_gasto.remove(child)
                except Exception:
                    pass

    # -------------------------------------------------------------------------
    # Página de inicio
    # -------------------------------------------------------------------------
    def page_home(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)

        # Logo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        image_path = os.path.join(project_root, "Images", "logo.png")

        if os.path.exists(image_path):
            picture = Gtk.Picture.new_for_filename(image_path)
            box.append(picture)

        # Botones de navegación
        btn_amigos = Gtk.Button(label="Lista de amigos")
        btn_amigos.connect("clicked", lambda b: self.stack.set_visible_child_name("amigos"))
        box.append(btn_amigos)

        btn_gastos = Gtk.Button(label="Mis gastos")
        btn_gastos.connect("clicked", lambda b: self.stack.set_visible_child_name("gastos"))
        box.append(btn_gastos)

        btn_balance = Gtk.Button(label="Mi balance")
        btn_balance.connect("clicked", lambda b: self.stack.set_visible_child_name("balance"))
        box.append(btn_balance)

        return box

    # -------------------------------------------------------------------------
    # Página de amigos
    # -------------------------------------------------------------------------
    def page_amigos(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        # Cuadrícula para los amigos
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)

        amigos = ["Juan", "María", "Pedro", "Ana"]
        for i, nombre in enumerate(amigos):
            btn_amigo = Gtk.Button(label=nombre)
            btn_amigo.connect("clicked", self.mostrar_opciones_amigo)
            grid.attach(btn_amigo, i % 2, i // 2, 1, 1)

        main_box.append(grid)

        # Contenedor para las opciones de un amigo
        # Se crea aquí una sola vez y se reutiliza; se vacía al volver a la página
        self.contenedor_opciones_amigo = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        main_box.append(self.contenedor_opciones_amigo)

        # Botones inferiores
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_crear = Gtk.Button(label="Crear amigo")
        btn_crear.connect("clicked", lambda b: self.stack.set_visible_child_name("crear_amigo"))
        button_box.append(btn_crear)

        button_box.append(Gtk.Box())  # espaciador
        btn_volver = Gtk.Button(label="Volver al inicio")
        btn_volver.connect("clicked", lambda b: self.stack.set_visible_child_name("home"))
        button_box.append(btn_volver)

        main_box.append(button_box)

        return main_box

    # -------------------------------------------------------------------------
    # Mostrar opciones de un amigo
    # -------------------------------------------------------------------------
    def mostrar_opciones_amigo(self, button):
        """Muestra los botones de opciones para un amigo"""
        # Vaciar primero el contenedor (por si ya tenía opciones de otro amigo)
        self._clear_contenedor_opciones_amigo()

        btn_ver_gastos = Gtk.Button(label="Ver gastos")
        btn_ver_gastos.connect("clicked", lambda b: self.stack.set_visible_child_name("gastos_amigo"))

        btn_editar = Gtk.Button(label="Editar")
        btn_editar.connect("clicked", lambda b: self.stack.set_visible_child_name("editar_amigo"))

        btn_ver_detalles = Gtk.Button(label="Ver detalles")
        btn_ver_detalles.connect("clicked", lambda b: self.stack.set_visible_child_name("detalles_amigo"))

        btn_eliminar = Gtk.Button(label="Eliminar amigo")
        btn_eliminar.connect("clicked", self.mostrar_confirmacion_eliminar)

        self.contenedor_opciones_amigo.append(btn_ver_gastos)
        self.contenedor_opciones_amigo.append(btn_editar)
        self.contenedor_opciones_amigo.append(btn_ver_detalles)
        self.contenedor_opciones_amigo.append(btn_eliminar)

    # -------------------------------------------------------------------------
    # Página Crear Amigo
    # -------------------------------------------------------------------------
    def page_crear_amigo(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        self.entry_nombre = Gtk.Entry()
        self.entry_nombre.set_placeholder_text("Nombre del amigo")
        main_box.append(self.entry_nombre)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_añadir = Gtk.Button(label="Añadir")
        button_box.append(btn_añadir)

        button_box.append(Gtk.Box())  # espaciador
        btn_volver = Gtk.Button(label="Volver")
        btn_volver.connect("clicked", lambda b: self.stack.set_visible_child_name("amigos"))
        button_box.append(btn_volver)

        main_box.append(button_box)
        return main_box

    # -------------------------------------------------------------------------
    # Página Editar Amigo
    # -------------------------------------------------------------------------
    def page_editar_amigo(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        label_titulo = Gtk.Label(label="Editar Amigo")
        main_box.append(label_titulo)

        entry_nombre = Gtk.Entry()
        entry_nombre.set_placeholder_text("Nuevo nombre")
        main_box.append(entry_nombre)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_confirmar = Gtk.Button(label="Confirmar")
        button_box.append(btn_confirmar)

        button_box.append(Gtk.Box())  # espaciador
        btn_volver = Gtk.Button(label="Volver")
        btn_volver.connect("clicked", lambda b: self.stack.set_visible_child_name("amigos"))
        button_box.append(btn_volver)

        main_box.append(button_box)
        return main_box

    # -------------------------------------------------------------------------
    # Página Detalles Amigo
    # -------------------------------------------------------------------------
    def page_detalles_amigo(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        label_titulo = Gtk.Label(label="Detalles del Amigo")
        main_box.append(label_titulo)

        campos = ["Nombre", "ID", "Datos", "Balance"]
        for campo in campos:
            label_t = Gtk.Label(label=f"{campo}:")
            label_v = Gtk.Label(label="")  # vacío por ahora
            fila = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            fila.append(label_t)
            fila.append(label_v)
            main_box.append(fila)

        btn_volver = Gtk.Button(label="Volver")
        btn_volver.connect("clicked", lambda b: self.stack.set_visible_child_name("amigos"))
        main_box.append(btn_volver)

        return main_box
    
    # -------------------------------------------------------------------------
    # Página Gastos Amigo
    # -------------------------------------------------------------------------
    def page_gastos_amigo(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
            for campo in campos:
            label_t = Gtk.Label(label=f"{campo}:")
            label_v = Gtk.Label(label="")  # vacío por ahora
            fila = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            fila.append(label_t)
            fila.append(label_v)
            main_box.append(fila)

        btn_volver = Gtk.Button(label="Volver")
        btn_volver.connect("clicked", lambda b: self.stack.set_visible_child_name("amigos"))
        main_box.append(btn_volver)

        return main_box

    # -------------------------------------------------------------------------
    # Diálogo Confirmar Eliminación
    # -------------------------------------------------------------------------
    def mostrar_confirmacion_eliminar(self, button):
        dialog = Gtk.Dialog(
            title="Confirmar eliminación",
            transient_for=self,
            modal=True
        )

        box = dialog.get_content_area()
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        box.set_spacing(10)

        label_texto = Gtk.Label(label="¿Desea eliminar al amigo?\n\nAVISO: El balance del amigo debe estar a 0")
        box.append(label_texto)

        botones_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_si = Gtk.Button(label="Sí")
        btn_no = Gtk.Button(label="No")

        btn_si.connect("clicked", lambda b: dialog.close())
        btn_no.connect("clicked", lambda b: dialog.close())

        botones_box.append(btn_si)
        botones_box.append(btn_no)
        box.append(botones_box)

        dialog.show()

    # -------------------------------------------------------------------------
    # Página Gastos (principal)
    # -------------------------------------------------------------------------
    def page_gastos(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label(label="Mis Gastos")
        box.append(label)

        back = Gtk.Button(label="Volver al inicio")
        back.connect("clicked", lambda b: self.stack.set_visible_child_name("home"))
        box.append(back)
        return box

    # -------------------------------------------------------------------------
    # Página Balance
    # -------------------------------------------------------------------------
    def page_balance(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label(label="Mi Balance")
        box.append(label)

        back = Gtk.Button(label="Volver al inicio")
        back.connect("clicked", lambda b: self.stack.set_visible_child_name("home"))
        box.append(back)
        return box
    
    
    def page_gastos(self):
        """Página de gastos"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        label = Gtk.Label(label="Mis Gastos")
        main_box.append(label)

        # Contenedor con lista de gastos (de momento, de ejemplo)
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)

        # Lista simulada de gastos (en el futuro vendrá de la base de datos)
        gastos = ["Compra supermercado", "Cena grupo", "Gasolina", "Viaje Madrid"]

        for i, nombre in enumerate(gastos):
            btn_gasto = Gtk.Button(label=nombre)
            btn_gasto.connect("clicked", self.mostrar_opciones_gasto)
            grid.attach(btn_gasto, i % 2, i // 2, 1, 1)

        main_box.append(grid)

        # Contenedor para las opciones de gasto
        self.contenedor_opciones_gasto = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        main_box.append(self.contenedor_opciones_gasto)

        # Botón para crear un nuevo gasto (ya tienes esta vista creada)
        btn_nuevo = Gtk.Button(label="Añadir nuevo gasto")
        btn_nuevo.connect("clicked", lambda b: self.stack.set_visible_child_name("crear_gasto"))
        main_box.append(btn_nuevo)

        # Botón volver
        btn_volver = Gtk.Button(label="Volver al inicio")
        btn_volver.connect("clicked", lambda b: self.stack.set_visible_child_name("home"))
        main_box.append(btn_volver)

        return main_box

    def mostrar_opciones_gasto(self, button):
        """Muestra los botones de opciones para un gasto"""
        # Vaciar contenedor antes de añadir nuevas opciones
        self._clear_contenedor_opciones_gasto()

        btn_editar = Gtk.Button(label="Editar")
        btn_mi_balance = Gtk.Button(label="Mi balance")
        btn_ver_detalles = Gtk.Button(label="Ver detalles")
        btn_participantes = Gtk.Button(label="Participantes")
        btn_eliminar = Gtk.Button(label="Eliminar gasto")

        # Conexiones
        btn_ver_detalles.connect("clicked", lambda b: self.stack.set_visible_child_name("detalles_gasto"))
        btn_participantes.connect("clicked", lambda b: self.stack.set_visible_child_name("participantes_gasto"))
        btn_eliminar.connect("clicked", self.mostrar_confirmacion_eliminar_gasto)

        self.contenedor_opciones_gasto.append(btn_editar)
        self.contenedor_opciones_gasto.append(btn_mi_balance)
        self.contenedor_opciones_gasto.append(btn_ver_detalles)
        self.contenedor_opciones_gasto.append(btn_participantes)
        self.contenedor_opciones_gasto.append(btn_eliminar)

    def page_detalles_gasto(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        label_titulo = Gtk.Label(label="Detalles del Gasto")
        main_box.append(label_titulo)

        campos = ["Nombre", "Descripción", "Fecha", "Cantidad"]
        for campo in campos:
            label_t = Gtk.Label(label=f"{campo}:")
            label_v = Gtk.Label(label="")  # vacío por ahora
            fila = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            fila.append(label_t)
            fila.append(label_v)
            main_box.append(fila)

        btn_volver = Gtk.Button(label="Volver")
        btn_volver.connect("clicked", lambda b: self.stack.set_visible_child_name("gastos"))
        main_box.append(btn_volver)

        return main_box
    
    def mostrar_confirmacion_eliminar_gasto(self, button):
        dialog = Gtk.Dialog(
            title="Confirmar eliminación de gasto",
            transient_for=self,
            modal=True
        )

        box = dialog.get_content_area()
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        box.set_spacing(10)

        label_texto = Gtk.Label(label="¿Desea eliminar el gasto?\n\nAVISO: Esta acción no se puede deshacer")
        box.append(label_texto)

        botones_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_si = Gtk.Button(label="Sí")
        btn_no = Gtk.Button(label="No")

        btn_si.connect("clicked", lambda b: dialog.close())
        btn_no.connect("clicked", lambda b: dialog.close())

        botones_box.append(btn_si)
        botones_box.append(btn_no)
        box.append(botones_box)

        dialog.show()


    def page_crear_gasto(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        # Campos de entrada
        entry_nombre = Gtk.Entry()
        entry_nombre.set_placeholder_text("Nombre del gasto")
        main_box.append(entry_nombre)

        entry_descripcion = Gtk.Entry()
        entry_descripcion.set_placeholder_text("Descripción")
        main_box.append(entry_descripcion)

        entry_cantidad = Gtk.Entry()
        entry_cantidad.set_placeholder_text("Cantidad (€)")
        main_box.append(entry_cantidad)

        entry_fecha = Gtk.Entry()
        entry_fecha.set_placeholder_text("Fecha (dd/mm/yyyy)")
        main_box.append(entry_fecha)

        # Botones
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        btn_añadir = Gtk.Button(label="Añadir gasto")
        button_box.append(btn_añadir)

        button_box.append(Gtk.Box())
        btn_volver = Gtk.Button(label="Volver")
        btn_volver.connect("clicked", lambda b: self.stack.set_visible_child_name("gastos"))
        button_box.append(btn_volver)

        main_box.append(button_box)

        return main_box
    
    def page_participantes_gasto(self):
        """Página para mostrar los participantes de un gasto"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        label = Gtk.Label(label="Participantes del gasto")
        main_box.append(label)

        # Participantes de ejemplo (en el futuro de la BBDD)
        self.participantes = ["Juan", "Ana", "Pedro"]

        # Contenedor donde estarán los botones de participantes
        self.grid_participantes = Gtk.Grid()
        self.grid_participantes.set_row_spacing(5)
        self.grid_participantes.set_column_spacing(5)

        for i, nombre in enumerate(self.participantes):
            btn_part = Gtk.Button(label=nombre)
            btn_part.connect("clicked", self.mostrar_opciones_participante)
            self.grid_participantes.attach(btn_part, i % 2, i // 2, 1, 1)

        main_box.append(self.grid_participantes)

        # Contenedor para las opciones del participante seleccionado
        self.contenedor_opciones_participante = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        main_box.append(self.contenedor_opciones_participante)

        # Botones inferiores
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        btn_añadir = Gtk.Button(label="Añadir participante")
        btn_añadir.connect("clicked", lambda b: self.stack.set_visible_child_name("añadir_participante"))
        button_box.append(btn_añadir)

        button_box.append(Gtk.Box())  # Espaciador
        btn_volver = Gtk.Button(label="Volver")
        btn_volver.connect("clicked", lambda b: self.stack.set_visible_child_name("gastos"))
        button_box.append(btn_volver)

        main_box.append(button_box)
        return main_box

        btn_eliminar.connect("clicked", self.mostrar_confirmacion_eliminar_participante)

        self.contenedor_opciones_participante.append(btn_eliminar)


    def page_añadir_participante(self):
        """Ventana para añadir un nuevo participante"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        label_titulo = Gtk.Label(label="Añadir participante")
        main_box.append(label_titulo)

        entry_nombre = Gtk.Entry()
        entry_nombre.set_placeholder_text("Nombre del participante")
        main_box.append(entry_nombre)

        # Botones confirmar y volver
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_confirmar = Gtk.Button(label="Confirmar")
        button_box.append(btn_confirmar)

        button_box.append(Gtk.Box())  # Espaciador
        btn_volver = Gtk.Button(label="Volver")
        btn_volver.connect("clicked", lambda b: self.stack.set_visible_child_name("participantes_gasto"))
        button_box.append(btn_volver)

        main_box.append(button_box)
        return main_box
    
    def mostrar_confirmacion_eliminar_participante(self, button):
        dialog = Gtk.Dialog(
            title="Confirmar eliminación de participante",
            transient_for=self,
            modal=True
        )

        box = dialog.get_content_area()
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        box.set_spacing(10)

        label_texto = Gtk.Label(
            label="¿Desea eliminar al participante?\n\nAVISO: Esta acción no se puede deshacer"
        )
        box.append(label_texto)

        botones_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_si = Gtk.Button(label="Sí")
        btn_no = Gtk.Button(label="No")

        btn_si.connect("clicked", lambda b: dialog.close())
        btn_no.connect("clicked", lambda b: dialog.close())

        botones_box.append(btn_si)
        botones_box.append(btn_no)
        box.append(botones_box)

        dialog.show()