"""
vista_vectores.py
------------------
Interfaz gráfica del módulo "Vectores en R^n": suma, resta, multiplicación
por escalar y verificación de combinación lineal.
"""

import customtkinter as ctk
from core.fraccion import Fraccion
from core.vectores import (
    parsear_vector,
    sumar_vectores,
    restar_vectores,
    escalar_por_vector,
    es_combinacion_lineal,
    vector_a_texto,
)
from ui import tema


class VistaVectores(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=tema.COLOR_FONDO)
        self.operacion_actual = "u + v"
        self._construir_interfaz()

    # ---------------------------------------------------------------
    def _construir_interfaz(self):
        tema.crear_encabezado(
            self,
            "↗",
            "Vectores en Rⁿ",
            "Operaciones algebraicas con vectores: suma, resta, escalar y combinación lineal.",
        )

        self.selector = tema.crear_selector_operaciones(
            self,
            ["u + v", "u - v", "k · u", "Combinación lineal"],
            self._cambiar_operacion,
        )
        self.selector.pack(fill="x", padx=28, pady=(0, 14))

        self.tarjeta_entrada = tema.crear_tarjeta(self)
        self.tarjeta_entrada.pack(fill="x", padx=28)

        self.contenedor_campos = ctk.CTkFrame(self.tarjeta_entrada, fg_color="transparent")
        self.contenedor_campos.pack(fill="x", padx=20, pady=18)

        self.etiqueta_error_widget = None

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

    # ---------------------------------------------------------------
    def _cambiar_operacion(self, valor):
        self.operacion_actual = valor
        self._dibujar_campos()

    def _dibujar_campos(self):
        for hijo in self.contenedor_campos.winfo_children():
            hijo.destroy()

        ayuda = (
            "Separa las componentes con comas o espacios, y usa punto decimal: 1, -2, 0.5, 1/3.\n"
            "No hace falta decir la dimensión n: es la cantidad de componentes que escribas."
        )

        if self.operacion_actual in ("u + v", "u - v"):
            self.campo_u = self._crear_campo_texto("u =")
            self.campo_v = self._crear_campo_texto("v =")
        elif self.operacion_actual == "k · u":
            self.campo_k = self._crear_campo_texto("k =", ancho=120)
            self.campo_u = self._crear_campo_texto("u =")
        else:  # Combinación lineal
            self.campo_objetivo = self._crear_campo_texto("Vector objetivo b =")
            self.campo_conjunto = self._crear_campo_texto_multilinea(
                "Vectores v1, v2, ... (uno por línea) ="
            )
            ayuda = (
                "Escribe un vector por línea, ej.:\n1, 0, 0\n0, 1, 0\n"
                "Se verificará si 'b' puede escribirse como c1*v1 + c2*v2 + ..."
            )

        ctk.CTkLabel(
            self.contenedor_campos, text=ayuda, font=("Segoe UI", 11), text_color=tema.COLOR_TEXTO_SUAVE, justify="left"
        ).pack(anchor="w", pady=(6, 0))

    def _crear_campo_texto(self, etiqueta, ancho=None):
        fila = ctk.CTkFrame(self.contenedor_campos, fg_color="transparent")
        fila.pack(fill="x", pady=6)
        ctk.CTkLabel(fila, text=etiqueta, font=tema.FUENTE_ETIQUETA, width=140, anchor="w").pack(side="left")
        entrada = ctk.CTkEntry(fila, font=tema.FUENTE_TEXTO, width=ancho or 400, fg_color=tema.COLOR_FONDO, border_color=tema.COLOR_BORDE)
        entrada.pack(side="left", fill="x", expand=(ancho is None))
        return entrada

    def _crear_campo_texto_multilinea(self, etiqueta):
        contenedor = ctk.CTkFrame(self.contenedor_campos, fg_color="transparent")
        contenedor.pack(fill="x", pady=6)
        ctk.CTkLabel(contenedor, text=etiqueta, font=tema.FUENTE_ETIQUETA, anchor="w").pack(anchor="w")
        caja = ctk.CTkTextbox(contenedor, font=tema.FUENTE_TEXTO, height=90, fg_color=tema.COLOR_FONDO)
        caja.pack(fill="x", pady=(4, 0))
        return caja

    # ---------------------------------------------------------------
    def _mostrar_error(self, texto):
        tema.mostrar_texto_resultado(self.caja_resultado, f"⚠ {texto}", es_error=True)

    def _calcular(self):
        try:
            if self.operacion_actual == "u + v":
                u = parsear_vector(self.campo_u.get())
                v = parsear_vector(self.campo_v.get())
                resultado = sumar_vectores(u, v)
                texto = (
                    f"n = {len(u)}\n\n"
                    f"u =\n{tema.renderizar_vector_bracket(u)}\n\n"
                    f"v =\n{tema.renderizar_vector_bracket(v)}\n\n"
                    f"u + v =\n{tema.renderizar_vector_bracket(resultado)}\n\n"
                    f"u + v = {vector_a_texto(resultado)}"
                )

            elif self.operacion_actual == "u - v":
                u = parsear_vector(self.campo_u.get())
                v = parsear_vector(self.campo_v.get())
                resultado = restar_vectores(u, v)
                texto = (
                    f"n = {len(u)}\n\n"
                    f"u =\n{tema.renderizar_vector_bracket(u)}\n\n"
                    f"v =\n{tema.renderizar_vector_bracket(v)}\n\n"
                    f"u - v =\n{tema.renderizar_vector_bracket(resultado)}\n\n"
                    f"u - v = {vector_a_texto(resultado)}"
                )

            elif self.operacion_actual == "k · u":
                k = Fraccion.desde_texto(self.campo_k.get())
                u = parsear_vector(self.campo_u.get())
                resultado = escalar_por_vector(k, u)
                pasos = "\n".join(f"  {k} * {u[i]} = {resultado[i]}" for i in range(len(u)))
                texto = (
                    f"n = {len(u)}\n\n"
                    f"u =\n{tema.renderizar_vector_bracket(u)}\n\n"
                    f"k · u =\n{tema.renderizar_vector_bracket(resultado)}\n\n"
                    f"Componente a componente:\n{pasos}\n\n"
                    f"{k}·u = {vector_a_texto(resultado)}"
                )

            else:  # Combinación lineal
                objetivo = parsear_vector(self.campo_objetivo.get())
                texto_conjunto = self.campo_conjunto.get("1.0", "end")
                lineas = [l for l in texto_conjunto.split("\n") if l.strip() != ""]
                if len(lineas) == 0:
                    raise ValueError("Debes escribir al menos un vector v1.")
                vectores = [parsear_vector(l) for l in lineas]
                resultado = es_combinacion_lineal(objetivo, vectores)

                lista_vectores = "\n".join(f"  v{i+1} = {vector_a_texto(v)}" for i, v in enumerate(vectores))
                texto = (
                    f"n = {len(objetivo)}   |   vectores dados: {len(vectores)}\n\n"
                    f"b = {vector_a_texto(objetivo)}\n{lista_vectores}\n\n"
                    f"{resultado['mensaje']}"
                )

            tema.mostrar_texto_resultado(self.caja_resultado, texto)

        except (ValueError, ZeroDivisionError) as error:
            self._mostrar_error(str(error))
