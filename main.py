"""
main.py
-------
Punto de entrada de la aplicación "Calculadora de Álgebra Lineal" (MTM0120).

Proyecto Integrador - Universidad Americana (UAM)
Facultad de Ingeniería y Arquitectura (FIA)
Asignatura: Álgebra Lineal (MTM0120)

Módulos incluidos (navegables desde la barra lateral):
  - Vectores en R^n (suma, resta, escalar, combinación lineal)
  - Operaciones Matriciales (suma, resta, escalar, producto de matrices)
  - Eliminación Gaussiana (resolución de A·x = b)
  - Formas Escalonadas (REF y RREF de una matriz)
  - Inversa de una Matriz (Gauss-Jordan [A|I], fórmula 2x2, verificación, x = A^-1 b)
  - Sistemas Numéricos (conversión entre bases)

Restricción del Contrato Didáctico: todo el cálculo algebraico (core/) está
escrito con Python estándar (listas, condicionales, bucles y funciones),
sin usar NumPy, SciPy ni funciones avanzadas de 'math'.

Para ejecutar:
    pip install -r requirements.txt
    python main.py
"""

import customtkinter as ctk

from ui import tema
from ui.vista_vectores import VistaVectores
from ui.vista_matrices import VistaMatrices
from ui.vista_gauss import VistaGauss
from ui.vista_escalonadas import VistaEscalonadas
from ui.vista_inversa import VistaInversa
from ui.vista_numeros import VistaNumeros
from ui.vista_determinantes import VistaDeterminantes
from ui.vista_biseccion import VistaBiseccion


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Aplicacion(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Álgebra Lineal · MTM0120")
        self.geometry("1280x820")
        self.minsize(1050, 690)
        self.configure(fg_color=tema.COLOR_FONDO)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._construir_sidebar()
        self._construir_area_contenido()

        # Se crean todas las vistas una sola vez y se muestran/ocultan
        # (evita reconstruir la interfaz cada vez que se cambia de sección).
        self.vistas = {
            "vectores": VistaVectores(self.contenedor_vistas),
            "matrices": VistaMatrices(self.contenedor_vistas),
            "gauss": VistaGauss(self.contenedor_vistas),
            "escalonadas": VistaEscalonadas(self.contenedor_vistas),
            "inversa": VistaInversa(self.contenedor_vistas),
            "numeros": VistaNumeros(self.contenedor_vistas),
            "determinantes": VistaDeterminantes(self.contenedor_vistas),
            "biseccion": VistaBiseccion(self.contenedor_vistas),
        }
        for vista in self.vistas.values():
            vista.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._mostrar_vista("vectores")

        # --- Corrección para un bug conocido de Tkinter en macOS ---
        # En algunas versiones de macOS, la ventana aparece en blanco al
        # abrir. Se corrige ocultándola y volviéndola a mostrar una sola
        # vez, apenas termina de construirse (sin bucles ni repeticiones,
        # para evitar recursión).
        self.after(150, self._forzar_redibujado_inicial)

    def _forzar_redibujado_inicial(self):
        self.withdraw()
        self.after(10, self.deiconify)

    # ---------------------------------------------------------------
    def _construir_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=tema.COLOR_SIDEBAR, width=266, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_propagate(False)

        encabezado = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        encabezado.pack(fill="x", padx=20, pady=(30, 24))

        icono = ctk.CTkLabel(
            encabezado, text="∑", font=("Arial", 24, "bold"), text_color="white",
            fg_color=tema.COLOR_PRIMARIO, width=46, height=46, corner_radius=14,
        )
        icono.pack(side="left")

        textos = ctk.CTkFrame(encabezado, fg_color="transparent")
        textos.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(textos, text="MATH LAB", font=("Arial", 16, "bold"), text_color=tema.COLOR_TEXTO).pack(anchor="w")
        ctk.CTkLabel(textos, text="CALCULADORA CIENTÍFICA", font=("Arial", 11), text_color=tema.COLOR_TEXTO_SUAVE).pack(anchor="w")

        separador = ctk.CTkFrame(self.sidebar, fg_color=tema.COLOR_BORDE, height=1)
        separador.pack(fill="x", padx=20, pady=(0, 12))

        self.botones_sidebar = {}
        opciones = [
            ("vectores", "↗", "Vectores"),
            ("matrices", "▦", "Operaciones Matriciales"),
            ("gauss", "⇥", "Eliminación Gaussiana"),
            ("escalonadas", "≣", "Formas Escalonadas"),
            ("inversa", "⁻¹", "Inversa de una Matriz"),
            ("numeros", "⇄", "Sistemas Numéricos"),
            ("determinantes", "det", "Determinantes"),
            ("biseccion", "ƒ", "Método de Bisección"),
        ]
        for clave, icono_texto, etiqueta in opciones:
            boton = ctk.CTkButton(
                self.sidebar,
                text=f"  {icono_texto}   {etiqueta}",
                anchor="w",
                font=tema.FUENTE_TEXTO,
                fg_color="transparent",
                text_color=tema.COLOR_TEXTO,
                hover_color=tema.COLOR_FONDO,
                corner_radius=11,
                height=45,
                command=lambda c=clave: self._mostrar_vista(c),
            )
            boton.pack(fill="x", padx=14, pady=4)
            self.botones_sidebar[clave] = boton

        ctk.CTkLabel(self.sidebar, text="UAM  •  MTM0120  •  PYTHON",
                     font=("Arial", 10, "bold"), text_color=tema.COLOR_TEXTO_SUAVE).pack(side="bottom", pady=24)

    def _construir_area_contenido(self):
        self.contenedor_vistas = ctk.CTkFrame(self, fg_color=tema.COLOR_FONDO, corner_radius=0)
        self.contenedor_vistas.grid(row=0, column=1, sticky="nswe")

    # ---------------------------------------------------------------
    def _mostrar_vista(self, clave):
        for nombre, boton in self.botones_sidebar.items():
            if nombre == clave:
                boton.configure(fg_color=tema.COLOR_PRIMARIO, text_color="white", hover_color=tema.COLOR_PRIMARIO_HOVER)
            else:
                boton.configure(fg_color="transparent", text_color=tema.COLOR_TEXTO, hover_color=tema.COLOR_FONDO)

        self.vistas[clave].tkraise()


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
