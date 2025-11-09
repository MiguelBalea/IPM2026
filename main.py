import sys
from gi import require_version
require_version('Gtk', '4.0')
from gi.repository import Gtk
from model import Model
from view import View
from presenter import Presenter

class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.MVPExample")

    def do_activate(self):
        model = Model(base_url="http://127.0.0.1:8000")
        view = View(self)
        presenter = Presenter(model, view)

        # Health check seguro: si model no define health_check o falla, lo capturamos
        try:
            if hasattr(model, "health_check"):
                ok = model.health_check()
                if ok:
                    print("[Model] Server reachable:", model.base_url)
                else:
                    print("[Model] No responde en:", model.base_url)
            else:
                print("[Model] health_check no definido en Model")
        except Exception as e:
            # Evitamos que un fallo de red bloquee la UI; el presenter debe manejar errores en llamadas reales
            print("[Model] No se pudo conectar con el servidor:", e)

        view.show()

if __name__ == "__main__":
    app = App()
    app.run(sys.argv)