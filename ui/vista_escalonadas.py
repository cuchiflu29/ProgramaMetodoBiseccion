"""
vista_escalonadas.py
---------------------
Interfaz gráfica del módulo "Formas Escalonadas": lleva cualquier matriz a
su Forma Escalonada (REF) y a su Forma Escalonada Reducida (RREF), mostrando
el procedimiento paso a paso.
"""

import customtkinter as ctk
from core.matrices import parsear_matriz, dimensiones
from core.gauss import forma_escalonada, forma_escalonada_reducida
from ui import tema


class VistaEscalonadas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=tema.COLOR_FONDO)
        self.modo_actual = "Forma Escalonada (REF)"
        self._construir_interfaz()

    def _construir_interfaz(self):
        tema.crear_encabezado(
            self,
            "≣",
            "Formas Escalonadas",
            "Reduce una matriz a su forma escalonada o a su forma escalonada reducida.",
        )

        self.selector = tema.crear_selector_operaciones(
            self, ["Forma Escalonada (REF)", "Forma Escalonada Reducida (RREF)"], self._cambiar_modo
        )
        self.selector.pack(fill="x", padx=28, pady=(0, 14))

        self.tarjeta_entrada = tema.crear_tarjeta(self)
        self.tarjeta_entrada.pack(fill="x", padx=28)

        contenedor = ctk.CTkFrame(self.tarjeta_entrada, fg_color="transparent")
        contenedor.pack(fill="x", padx=20, pady=18)

        ctk.CTkLabel(contenedor, text="Matriz (o matriz aumentada) =", font=tema.FUENTE_ETIQUETA, anchor="w").pack(anchor="w")
        self.campo_matriz = ctk.CTkTextbox(contenedor, font=tema.FUENTE_MONO, height=110, fg_color=tema.COLOR_FONDO)
        self.campo_matriz.pack(fill="x", pady=(4, 4))

        ayuda = "Escribe cada fila en una línea; separa columnas con comas o espacios."
        ctk.CTkLabel(contenedor, text=ayuda, font=("Segoe UI", 11), text_color=tema.COLOR_TEXTO_SUAVE, justify="left").pack(anchor="w", pady=(6, 0))

        self.boton_calcular = ctk.CTkButton(
            self.tarjeta_entrada,
            text="Reducir  →",
            font=tema.FUENTE_BOTON,
            fg_color=tema.COLOR_PRIMARIO,
            hover_color=tema.COLOR_PRIMARIO_HOVER,
            height=38,
            command=self._calcular,
        )
        self.boton_calcular.pack(anchor="e", padx=20, pady=(0, 18))

        _, self.caja_resultado = tema.crear_caja_resultado(self)

    def _cambiar_modo(self, valor):
        self.modo_actual = valor

    def _mostrar_error(self, texto):
        tema.mostrar_texto_resultado(self.caja_resultado, f"⚠ {texto}", es_error=True)

    def _calcular(self):
        try:
            matriz = parsear_matriz(self.campo_matriz.get("1.0", "end"))
            filas, columnas = dimensiones(matriz)

            if self.modo_actual == "Forma Escalonada (REF)":
                resultado, pasos = forma_escalonada(matriz, registrar_pasos=True)
                nombre = "Forma Escalonada (REF)"
            else:
                resultado, pasos = forma_escalonada_reducida(matriz, registrar_pasos=True)
                nombre = "Forma Escalonada Reducida (RREF)"

            lineas = [f"Matriz original ({filas}x{columnas}):"]
            lineas.append(tema.renderizar_matriz_bracket(matriz))
            lineas.append("\nOperaciones elementales de fila aplicadas:")
            if pasos:
                for paso in pasos:
                    lineas.append(f"  {paso}")
            else:
                lineas.append("  (la matriz ya estaba en la forma pedida)")

            lineas.append(f"\n{nombre}:")
            lineas.append(tema.renderizar_matriz_bracket(resultado))

            tema.mostrar_texto_resultado(self.caja_resultado, "\n".join(lineas))

        except (ValueError, ZeroDivisionError) as error:
            self._mostrar_error(str(error))
