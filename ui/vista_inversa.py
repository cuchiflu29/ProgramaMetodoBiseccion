"""
vista_inversa.py
----------------
Interfaz gráfica del módulo "Inversa de una Matriz" (Unidad 2.2):
  - Gauss-Jordan sobre [A | I] paso a paso.
  - Fórmula directa para matrices 2x2 (ad - bc).
  - Resolución de A·x = b mediante x = A^-1·b.
Todos los casos incluyen la verificación A·A^-1 = I.
"""

import customtkinter as ctk
from core.matrices import parsear_matriz, dimensiones
from core.vectores import parsear_vector, vector_a_texto
from core.inversa import (
    inversa_gauss_jordan,
    inversa_formula_2x2,
    verificar_inversa,
    resolver_con_inversa,
    validar_cuadrada,
)
from ui import tema

MODO_GAUSS = "Gauss-Jordan [A | I]"
MODO_FORMULA = "Fórmula 2×2"
MODO_SISTEMA = "Resolver A·x = b"


def _aumentada_a_texto(matriz, n):
    """Dibuja una matriz aumentada [bloque izquierdo | bloque derecho] con una barra vertical."""
    con_barra = []
    for fila in matriz:
        con_barra.append([str(v) for v in fila[:n]] + ["|"] + [str(v) for v in fila[n:]])
    return tema.renderizar_matriz_bracket(con_barra)


class VistaInversa(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=tema.COLOR_FONDO)
        self.modo_actual = MODO_GAUSS
        self._construir_interfaz()

    def _construir_interfaz(self):
        tema.crear_encabezado(
            self,
            "⁻¹",
            "Inversa de una Matriz",
            "Calcula A⁻¹ por Gauss-Jordan o con la fórmula 2×2, y verifica que A·A⁻¹ = I.",
        )

        self.selector = tema.crear_selector_operaciones(
            self, [MODO_GAUSS, MODO_FORMULA, MODO_SISTEMA], self._cambiar_modo
        )
        self.selector.pack(fill="x", padx=28, pady=(0, 14))

        self.tarjeta_entrada = tema.crear_tarjeta(self)
        self.tarjeta_entrada.pack(fill="x", padx=28)

        self.contenedor_campos = ctk.CTkFrame(self.tarjeta_entrada, fg_color="transparent")
        self.contenedor_campos.pack(fill="x", padx=20, pady=18)

        self.boton_calcular = ctk.CTkButton(
            self.tarjeta_entrada,
            text="Calcular inversa  →",
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
    def _cambiar_modo(self, valor):
        self.modo_actual = valor
        self._dibujar_campos()

    def _dibujar_campos(self):
        for hijo in self.contenedor_campos.winfo_children():
            hijo.destroy()

        ctk.CTkLabel(
            self.contenedor_campos, text="Matriz cuadrada A =", font=tema.FUENTE_ETIQUETA, anchor="w"
        ).pack(anchor="w")
        self.campo_A = ctk.CTkTextbox(
            self.contenedor_campos, font=tema.FUENTE_MONO, height=90, fg_color=tema.COLOR_FONDO
        )
        self.campo_A.pack(fill="x", pady=(4, 10))

        self.campo_b = None
        if self.modo_actual == MODO_SISTEMA:
            ctk.CTkLabel(
                self.contenedor_campos,
                text="Vector de términos independientes b =",
                font=tema.FUENTE_ETIQUETA,
                anchor="w",
            ).pack(anchor="w")
            self.campo_b = ctk.CTkEntry(self.contenedor_campos, font=tema.FUENTE_TEXTO, fg_color=tema.COLOR_FONDO)
            self.campo_b.pack(fill="x", pady=(4, 4))

        if self.modo_actual == MODO_FORMULA:
            ayuda = "Solo para matrices 2×2.  Ejemplo:\n3, 4\n5, 6"
        elif self.modo_actual == MODO_SISTEMA:
            ayuda = "Ejemplo:  A =  3, 4 / 5, 6   y   b = 3, 7   (A en dos líneas)"
        else:
            ayuda = (
                "Escribe cada fila en una línea; separa columnas con comas o espacios.\n"
                "Ejemplo:\n1, -2, -1\n-1, 5, 6\n5, -4, 5"
            )
        ctk.CTkLabel(
            self.contenedor_campos, text=ayuda, font=(
                "Segoe UI", 11), text_color=tema.COLOR_TEXTO_SUAVE, justify="left"
        ).pack(anchor="w", pady=(6, 0))

    def _mostrar_error(self, texto):
        tema.mostrar_texto_resultado(self.caja_resultado, f"⚠ {texto}", es_error=True)

    # ---------------------------------------------------------------
    def _calcular(self):
        try:
            A = parsear_matriz(self.campo_A.get("1.0", "end"))
            n = validar_cuadrada(A)

            if self.modo_actual == MODO_GAUSS:
                texto = self._texto_gauss(A, n)
            elif self.modo_actual == MODO_FORMULA:
                texto = self._texto_formula(A)
            else:
                texto = self._texto_sistema(A, n)

            tema.mostrar_texto_resultado(self.caja_resultado, texto)

        except (ValueError, ZeroDivisionError) as error:
            self._mostrar_error(str(error))

    def _texto_verificacion(self, A, inversa):
        derecho, izquierdo, ok = verificar_inversa(A, inversa)
        lineas = [
            "\nVerificación:",
            "A · A⁻¹ =",
            tema.renderizar_matriz_bracket(derecho),
            "A⁻¹ · A =",
            tema.renderizar_matriz_bracket(izquierdo),
            "✅ Ambos productos dan la identidad: A⁻¹ es correcta." if ok
            else "❌ Los productos no dan la identidad: revisa el cálculo.",
        ]
        return lineas

    def _texto_gauss(self, A, n):
        resultado = inversa_gauss_jordan(A)
        lineas = [f"A es {n}x{n}\n", "Matriz aumentada [A | I]:", _aumentada_a_texto(resultado["inicial"], n), ""]

        lineas.append("Operaciones elementales de fila:")
        for descripcion, matriz in resultado["pasos"]:
            lineas.append(f"\n  {descripcion}")
            lineas.append(_aumentada_a_texto(matriz, n))

        lineas.append("")
        if not resultado["invertible"]:
            lineas.append(
                f"❌ La columna {resultado['columna_sin_pivote']} no tiene pivote: "
                "A es SINGULAR (no es invertible)."
            )
            return "\n".join(lineas)

        lineas.append("Resultado [I | A⁻¹]:")
        lineas.append(_aumentada_a_texto(resultado["final"], n))
        lineas.append("\n✅ A es INVERTIBLE (matriz no singular).")
        lineas.append("A⁻¹ =")
        lineas.append(tema.renderizar_matriz_bracket(resultado["inversa"]))
        lineas.extend(self._texto_verificacion(A, resultado["inversa"]))
        return "\n".join(lineas)

    def _texto_formula(self, A):
        det, inversa = inversa_formula_2x2(A)
        a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
        lineas = [
            "A =",
            tema.renderizar_matriz_bracket(A),
            "",
            f"ad - bc = ({a})({d}) - ({b})({c}) = {det}",
            "",
        ]
        if inversa is None:
            lineas.append("❌ ad - bc = 0, así que A NO es invertible (es singular).")
            return "\n".join(lineas)

        lineas.append("Como ad - bc ≠ 0, A es invertible y")
        lineas.append(f"A⁻¹ = 1/({det}) · [[ {d}, {-b} ], [ {-c}, {a} ]]")
        lineas.append("A⁻¹ =")
        lineas.append(tema.renderizar_matriz_bracket(inversa))
        lineas.extend(self._texto_verificacion(A, inversa))
        return "\n".join(lineas)

    def _texto_sistema(self, A, n):
        b = parsear_vector(self.campo_b.get())
        inversa, x = resolver_con_inversa(A, b)
        lineas = [f"A es {n}x{n}   |   b = {vector_a_texto(b)}\n"]
        if inversa is None:
            lineas.append("❌ A es singular (no es invertible), así que no se puede usar x = A⁻¹·b.")
            lineas.append("Prueba el módulo de Eliminación Gaussiana para analizar el sistema.")
            return "\n".join(lineas)

        lineas.append("A⁻¹ =")
        lineas.append(tema.renderizar_matriz_bracket(inversa))
        lineas.append("\nComo A es invertible, A·x = b tiene solución única: x = A⁻¹·b")
        lineas.append(f"x = {vector_a_texto(x)}")
        lineas.append("x =")
        lineas.append(tema.renderizar_vector_bracket(x))
        return "\n".join(lineas)
