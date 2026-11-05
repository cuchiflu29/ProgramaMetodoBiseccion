"""
vista_matrices.py
------------------
Interfaz gráfica del módulo "Operaciones Matriciales Básicas": suma, resta,
multiplicación por escalar y multiplicación de matrices.
"""

import customtkinter as ctk
from core.fraccion import Fraccion
from core.matrices import (
    parsear_matriz,
    sumar_matrices,
    restar_matrices,
    escalar_por_matriz,
    multiplicar_matrices,
    matriz_a_texto,
    dimensiones,
)
from ui import tema


class VistaMatrices(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=tema.COLOR_FONDO)
        self.operacion_actual = "A + B"
        self._construir_interfaz()

    def _construir_interfaz(self):
        tema.crear_encabezado(
            self,
            "▦",
            "Operaciones Matriciales",
            "Suma, resta, multiplicación por escalar y multiplicación de matrices.",
        )

        self.selector = tema.crear_selector_operaciones(
            self, ["A + B", "A - B", "k · A", "A × B"], self._cambiar_operacion
        )
        self.selector.pack(fill="x", padx=28, pady=(0, 14))

        self.tarjeta_entrada = tema.crear_tarjeta(self)
        self.tarjeta_entrada.pack(fill="x", padx=28)

        self.contenedor_campos = ctk.CTkFrame(self.tarjeta_entrada, fg_color="transparent")
        self.contenedor_campos.pack(fill="x", padx=20, pady=18)

        self.boton_calcular = ctk.CTkButton(
            self.tarjeta_entrada,
            text="Calcular  →",
            font=tema.FUENTE_BOTON,
            fg_color=tema.COLOR_PRIMARIO,
            hover_color=tema.COLOR_PRIMARIO_HOVER,
            height=38,
            command=self._calcular,
        )
        self.boton_calcular.pack(anchor="e", padx=20, pady=(0, 18))

        _, self.caja_resultado = tema.crear_caja_resultado(self)

        self._dibujar_campos()

    def _cambiar_operacion(self, valor):
        self.operacion_actual = valor
        self._dibujar_campos()

    def _dibujar_campos(self):
        for hijo in self.contenedor_campos.winfo_children():
            hijo.destroy()

        self.campo_A = self._crear_campo_matriz("Matriz A =")
        if self.operacion_actual == "k · A":
            self.campo_k = self._crear_campo_texto_corto("k =")
        else:
            self.campo_B = self._crear_campo_matriz("Matriz B =")

        ayuda = (
            "Escribe cada fila en una línea; separa columnas con comas o espacios.\n"
            "Ejemplo:\n1, 2, 3\n4, 5, 6"
        )
        ctk.CTkLabel(
            self.contenedor_campos, text=ayuda, font=("Segoe UI", 11), text_color=tema.COLOR_TEXTO_SUAVE, justify="left"
        ).pack(anchor="w", pady=(6, 0))

    def _crear_campo_matriz(self, etiqueta):
        contenedor = ctk.CTkFrame(self.contenedor_campos, fg_color="transparent")
        contenedor.pack(fill="x", pady=6)
        ctk.CTkLabel(contenedor, text=etiqueta, font=tema.FUENTE_ETIQUETA, anchor="w").pack(anchor="w")
        caja = ctk.CTkTextbox(contenedor, font=tema.FUENTE_MONO, height=90, fg_color=tema.COLOR_FONDO)
        caja.pack(fill="x", pady=(4, 0))
        return caja

    def _crear_campo_texto_corto(self, etiqueta):
        fila = ctk.CTkFrame(self.contenedor_campos, fg_color="transparent")
        fila.pack(fill="x", pady=6)
        ctk.CTkLabel(fila, text=etiqueta, font=tema.FUENTE_ETIQUETA, width=60, anchor="w").pack(side="left")
        entrada = ctk.CTkEntry(fila, font=tema.FUENTE_TEXTO, width=120, fg_color=tema.COLOR_FONDO)
        entrada.pack(side="left")
        return entrada

    def _mostrar_error(self, texto):
        tema.mostrar_texto_resultado(self.caja_resultado, f"⚠ {texto}", es_error=True)

    def _calcular(self):
        try:
            A = parsear_matriz(self.campo_A.get("1.0", "end"))
            fa, ca = dimensiones(A)

            if self.operacion_actual == "k · A":
                k = Fraccion.desde_texto(self.campo_k.get())
                resultado = escalar_por_matriz(k, A)
                texto = (
                    f"A es de tamaño {fa}x{ca}\n\n"
                    f"A =\n{tema.renderizar_matriz_bracket(A)}\n\n"
                    f"{k} · A =\n{tema.renderizar_matriz_bracket(resultado)}"
                )
            else:
                B = parsear_matriz(self.campo_B.get("1.0", "end"))
                fb, cb = dimensiones(B)

                if self.operacion_actual == "A + B":
                    resultado = sumar_matrices(A, B)
                    simbolo = "+"
                elif self.operacion_actual == "A - B":
                    resultado = restar_matrices(A, B)
                    simbolo = "-"
                else:  # A x B
                    resultado = multiplicar_matrices(A, B)
                    simbolo = "×"

                fr, cr = dimensiones(resultado)
                texto = (
                    f"A es {fa}x{ca}   |   B es {fb}x{cb}   |   Resultado es {fr}x{cr}\n\n"
                    f"A =\n{tema.renderizar_matriz_bracket(A)}\n\n"
                    f"B =\n{tema.renderizar_matriz_bracket(B)}\n\n"
                    f"A {simbolo} B =\n{tema.renderizar_matriz_bracket(resultado)}"
                )

            tema.mostrar_texto_resultado(self.caja_resultado, texto)

        except (ValueError, ZeroDivisionError) as error:
            self._mostrar_error(str(error))
