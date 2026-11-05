"""
vista_gauss.py
--------------
Interfaz gráfica del módulo "Eliminación Gaussiana": resuelve la ecuación
matricial A*x = b usando Gauss-Jordan, mostrando el procedimiento paso a
paso (operaciones elementales de fila) y el tipo de solución.
"""

import customtkinter as ctk
from core.matrices import parsear_matriz, dimensiones, resolver_ecuacion_matricial
from core.vectores import parsear_vector, vector_a_texto
from ui import tema


class VistaGauss(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=tema.COLOR_FONDO)
        self._construir_interfaz()

    def _construir_interfaz(self):
        tema.crear_encabezado(
            self,
            "⇥",
            "Eliminación Gaussiana",
            "Resuelve el sistema A·x = b usando Gauss-Jordan y muestra el procedimiento.",
        )

        self.tarjeta_entrada = tema.crear_tarjeta(self)
        self.tarjeta_entrada.pack(fill="x", padx=28)

        contenedor = ctk.CTkFrame(self.tarjeta_entrada, fg_color="transparent")
        contenedor.pack(fill="x", padx=20, pady=18)

        ctk.CTkLabel(contenedor, text="Matriz de coeficientes A =", font=tema.FUENTE_ETIQUETA, anchor="w").pack(anchor="w")
        self.campo_A = ctk.CTkTextbox(contenedor, font=tema.FUENTE_MONO, height=90, fg_color=tema.COLOR_FONDO)
        self.campo_A.pack(fill="x", pady=(4, 12))

        ctk.CTkLabel(contenedor, text="Vector de términos independientes b =", font=tema.FUENTE_ETIQUETA, anchor="w").pack(anchor="w")
        self.campo_b = ctk.CTkEntry(contenedor, font=tema.FUENTE_TEXTO, fg_color=tema.COLOR_FONDO)
        self.campo_b.pack(fill="x", pady=(4, 4))

        ayuda = (
            "Ejemplo de A (una fila por línea):\n2, 1, -1\n-3, -1, 2\n-2, 1, 2\n"
            "Ejemplo de b: 8, -11, -3"
        )
        ctk.CTkLabel(contenedor, text=ayuda, font=("Segoe UI", 11), text_color=tema.COLOR_TEXTO_SUAVE, justify="left").pack(anchor="w", pady=(6, 0))

        self.boton_calcular = ctk.CTkButton(
            self.tarjeta_entrada,
            text="Resolver sistema  →",
            font=tema.FUENTE_BOTON,
            fg_color=tema.COLOR_PRIMARIO,
            hover_color=tema.COLOR_PRIMARIO_HOVER,
            height=38,
            command=self._calcular,
        )
        self.boton_calcular.pack(anchor="e", padx=20, pady=(0, 18))

        _, self.caja_resultado = tema.crear_caja_resultado(self)

    def _mostrar_error(self, texto):
        tema.mostrar_texto_resultado(self.caja_resultado, f"⚠ {texto}", es_error=True)

    def _calcular(self):
        try:
            A = parsear_matriz(self.campo_A.get("1.0", "end"))
            b = parsear_vector(self.campo_b.get())
            fa, ca = dimensiones(A)

            resultado = resolver_ecuacion_matricial(A, b)

            lineas = [f"A es {fa}x{ca}   |   b = {vector_a_texto(b)}\n"]
            lineas.append("Procedimiento (operaciones elementales de fila):")
            if resultado["pasos"]:
                for paso in resultado["pasos"]:
                    lineas.append(f"  {paso}")
            else:
                lineas.append("  (la matriz ya estaba en su forma reducida)")

            lineas.append("\nForma escalonada reducida [A | b]:")
            lineas.append(tema.renderizar_matriz_bracket(resultado["rref"]))

            lineas.append("")
            if resultado["tipo"] == "sin_solucion":
                lineas.append("❌ El sistema NO tiene solución (es inconsistente).")
            elif resultado["tipo"] == "unica":
                lineas.append("✅ El sistema tiene SOLUCIÓN ÚNICA:")
                lineas.append(f"  x = {vector_a_texto(resultado['solucion_particular'])}")
            else:
                lineas.append("♾️ El sistema tiene INFINITAS SOLUCIONES.")
                lineas.append(f"  Una solución particular es: x = {vector_a_texto(resultado['solucion_particular'])}")

            tema.mostrar_texto_resultado(self.caja_resultado, "\n".join(lineas))

        except (ValueError, ZeroDivisionError) as error:
            self._mostrar_error(str(error))
