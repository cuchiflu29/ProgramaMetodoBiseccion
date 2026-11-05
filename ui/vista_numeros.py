"""
vista_numeros.py
------------------
Interfaz gráfica del módulo "Sistemas Numéricos": conversión de decimal a
otra base (binario, octal, hexadecimal o base 2-36) y de otra base a
decimal, mostrando el procedimiento (divisiones sucesivas o combinación
lineal por posiciones).
"""

import customtkinter as ctk
from core.sistemas_numericos import decimal_a_base, base_a_decimal, texto_combinacion_lineal
from core.numeros_romanos import decimal_a_romano, romano_a_decimal
from ui import tema


class VistaNumeros(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=tema.COLOR_FONDO)
        self.modo_actual = "Decimal → otra base"
        self.base_destino_predefinida = "Binario (2)"
        self._construir_interfaz()

    # ---------------------------------------------------------------
    def _construir_interfaz(self):
        tema.crear_encabezado(
            self,
            "⇄",
            "Sistemas Numéricos",
            "Conversión entre decimal, binario/octal/hex/base-b, y números romanos.",
        )

        self.selector = tema.crear_selector_operaciones(
            self,
            ["Decimal → otra base", "Otra base → decimal", "Decimal → Romano", "Romano → Decimal"],
            self._cambiar_modo,
        )
        self.selector.pack(fill="x", padx=28, pady=(0, 14))

        self.tarjeta_entrada = tema.crear_tarjeta(self)
        self.tarjeta_entrada.pack(fill="x", padx=28)

        self.contenedor_campos = ctk.CTkFrame(self.tarjeta_entrada, fg_color="transparent")
        self.contenedor_campos.pack(fill="x", padx=20, pady=18)

        self.boton_calcular = ctk.CTkButton(
            self.tarjeta_entrada,
            text="Convertir  →",
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

        if self.modo_actual == "Decimal → otra base":
            fila1 = ctk.CTkFrame(self.contenedor_campos, fg_color="transparent")
            fila1.pack(fill="x", pady=6)
            ctk.CTkLabel(fila1, text="NÚMERO DECIMAL", font=("Segoe UI", 11, "bold"), text_color=tema.COLOR_TEXTO_SUAVE, anchor="w").pack(anchor="w")
            self.campo_numero = ctk.CTkEntry(fila1, font=tema.FUENTE_TEXTO, fg_color=tema.COLOR_FONDO)
            self.campo_numero.pack(fill="x", pady=(4, 0))

            ctk.CTkLabel(self.contenedor_campos, text="CONVERTIR A", font=("Segoe UI", 11, "bold"), text_color=tema.COLOR_TEXTO_SUAVE, anchor="w").pack(anchor="w", pady=(14, 4))

            fila_bases = ctk.CTkFrame(self.contenedor_campos, fg_color="transparent")
            fila_bases.pack(fill="x")
            self.selector_base = ctk.CTkSegmentedButton(
                fila_bases,
                values=["Binario (2)", "Octal (8)", "Hexadecimal (16)", "Otra base"],
                fg_color=tema.COLOR_FONDO,
                selected_color=tema.COLOR_PRIMARIO,
                selected_hover_color=tema.COLOR_PRIMARIO_HOVER,
                unselected_color=tema.COLOR_TARJETA,
                command=self._cambiar_base_destino,
            )
            self.selector_base.set(self.base_destino_predefinida)
            self.selector_base.pack(side="left")

            self.campo_base_otra = ctk.CTkEntry(fila_bases, font=tema.FUENTE_TEXTO, width=60, fg_color=tema.COLOR_FONDO, placeholder_text="b")
            self.etiqueta_entre = ctk.CTkLabel(fila_bases, text="entre 2 y 36", font=("Segoe UI", 11), text_color=tema.COLOR_TEXTO_SUAVE)
            if self.base_destino_predefinida == "Otra base":
                self.campo_base_otra.pack(side="left", padx=(10, 4))
                self.etiqueta_entre.pack(side="left")

        elif self.modo_actual == "Otra base → decimal":
            fila1 = ctk.CTkFrame(self.contenedor_campos, fg_color="transparent")
            fila1.pack(fill="x", pady=6)
            ctk.CTkLabel(fila1, text="NÚMERO A CONVERTIR", font=("Segoe UI", 11, "bold"), text_color=tema.COLOR_TEXTO_SUAVE, anchor="w").pack(anchor="w")
            self.campo_numero = ctk.CTkEntry(fila1, font=tema.FUENTE_TEXTO, fg_color=tema.COLOR_FONDO)
            self.campo_numero.pack(fill="x", pady=(4, 0))

            fila2 = ctk.CTkFrame(self.contenedor_campos, fg_color="transparent")
            fila2.pack(fill="x", pady=(14, 0))
            ctk.CTkLabel(fila2, text="BASE DE ORIGEN (2 a 36)", font=("Segoe UI", 11, "bold"), text_color=tema.COLOR_TEXTO_SUAVE, anchor="w").pack(anchor="w")
            self.campo_base_origen = ctk.CTkEntry(fila2, font=tema.FUENTE_TEXTO, width=100, fg_color=tema.COLOR_FONDO)
            self.campo_base_origen.pack(anchor="w", pady=(4, 0))

        elif self.modo_actual == "Decimal → Romano":
            fila1 = ctk.CTkFrame(self.contenedor_campos, fg_color="transparent")
            fila1.pack(fill="x", pady=6)
            ctk.CTkLabel(fila1, text="NÚMERO DECIMAL (1 a 3999)", font=("Segoe UI", 11, "bold"), text_color=tema.COLOR_TEXTO_SUAVE, anchor="w").pack(anchor="w")
            self.campo_numero = ctk.CTkEntry(fila1, font=tema.FUENTE_TEXTO, fg_color=tema.COLOR_FONDO)
            self.campo_numero.pack(fill="x", pady=(4, 0))

            ayuda = (
                "El sistema romano clásico solo representa enteros positivos del 1 al 3999.\n"
                "Si escribes un número con decimales, se convertirá únicamente su parte entera."
            )
            ctk.CTkLabel(self.contenedor_campos, text=ayuda, font=("Segoe UI", 11), text_color=tema.COLOR_TEXTO_SUAVE, justify="left").pack(anchor="w", pady=(10, 0))

        else:  # Romano → Decimal
            fila1 = ctk.CTkFrame(self.contenedor_campos, fg_color="transparent")
            fila1.pack(fill="x", pady=6)
            ctk.CTkLabel(fila1, text="NÚMERO ROMANO", font=("Segoe UI", 11, "bold"), text_color=tema.COLOR_TEXTO_SUAVE, anchor="w").pack(anchor="w")
            self.campo_romano = ctk.CTkEntry(fila1, font=tema.FUENTE_TEXTO, fg_color=tema.COLOR_FONDO, placeholder_text="Ej: MCMXCIV")
            self.campo_romano.pack(fill="x", pady=(4, 0))

    def _cambiar_base_destino(self, valor):
        self.base_destino_predefinida = valor
        if valor == "Otra base":
            self.campo_base_otra.pack(side="left", padx=(10, 4))
            self.etiqueta_entre.pack(side="left")
        else:
            self.campo_base_otra.pack_forget()
            self.etiqueta_entre.pack_forget()

    # ---------------------------------------------------------------
    def _mostrar_error(self, texto):
        tema.mostrar_texto_resultado(self.caja_resultado, f"⚠ {texto}", es_error=True)

    def _obtener_base_destino(self):
        mapa = {"Binario (2)": 2, "Octal (8)": 8, "Hexadecimal (16)": 16}
        if self.base_destino_predefinida in mapa:
            return mapa[self.base_destino_predefinida]
        texto_base = self.campo_base_otra.get().strip()
        if texto_base == "":
            raise ValueError("Debes indicar la base destino (entre 2 y 36).")
        return int(texto_base)

    def _calcular(self):
        try:
            if self.modo_actual == "Decimal → otra base":
                texto_numero = self.campo_numero.get().strip()
                if texto_numero == "":
                    raise ValueError("Debes escribir un número decimal.")
                numero = int(texto_numero)
                base = self._obtener_base_destino()

                resultado, pasos = decimal_a_base(numero, base)

                lineas = [f"Convertir {numero} (decimal) a base {base}, por divisiones sucesivas:\n"]
                lineas.append(f"{'Dividendo':>10} {'÷ Base':>8} {'= Cociente':>12} {'  Residuo':>10}")
                for dividendo, b, cociente, residuo in pasos:
                    lineas.append(f"{dividendo:>10} {b:>8} {cociente:>12} {residuo:>10}")
                lineas.append("\nLeyendo los residuos de abajo hacia arriba:")
                lineas.append(f"\n{numero} en base {base} = {resultado}")

                tema.mostrar_texto_resultado(self.caja_resultado, "\n".join(lineas))

            elif self.modo_actual == "Otra base → decimal":
                texto_numero = self.campo_numero.get().strip()
                if texto_numero == "":
                    raise ValueError("Debes escribir el número a convertir.")
                base_texto = self.campo_base_origen.get().strip()
                if base_texto == "":
                    raise ValueError("Debes indicar la base de origen (entre 2 y 36).")
                base = int(base_texto)

                valor_decimal, pasos = base_a_decimal(texto_numero, base)
                combinacion = texto_combinacion_lineal(pasos, base)

                lineas = [
                    f"Convertir {texto_numero.upper()} (base {base}) a decimal:\n",
                    "Combinación lineal por posiciones:",
                    f"  {combinacion}",
                    f"\n{texto_numero.upper()} en base {base} = {valor_decimal} (decimal)",
                ]

                tema.mostrar_texto_resultado(self.caja_resultado, "\n".join(lineas))

            elif self.modo_actual == "Decimal → Romano":
                texto_numero = self.campo_numero.get().strip()
                if texto_numero == "":
                    raise ValueError("Debes escribir un número decimal.")
                # Si escriben un decimal (ej. "54.7"), solo se usa la parte entera,
                # ya que el sistema romano no representa decimales.
                numero = int(float(texto_numero))

                resultado, pasos = decimal_a_romano(numero)

                lineas = [f"Convertir {numero} (decimal) a número romano, restando el valor más grande posible en cada paso:\n"]
                lineas.append(f"{'Número antes':>14} {'- Valor':>10} {'Símbolo':>9} {'= Restante':>12}")
                for valor, simbolo, antes, despues in pasos:
                    lineas.append(f"{antes:>14} {valor:>10} {simbolo:>9} {despues:>12}")
                lineas.append(f"\n{numero} en números romanos = {resultado}")

                tema.mostrar_texto_resultado(self.caja_resultado, "\n".join(lineas))

            else:  # Romano → Decimal
                texto_romano = self.campo_romano.get().strip()
                if texto_romano == "":
                    raise ValueError("Debes escribir un número romano.")

                valor_decimal, pasos = romano_a_decimal(texto_romano)

                lineas = [f"Convertir {texto_romano.upper()} (romano) a decimal, sumando o restando cada símbolo:\n"]
                for simbolo, valor, operacion in pasos:
                    signo = "-" if operacion == "resta" else "+"
                    lineas.append(f"  {simbolo} = {signo}{valor}")
                lineas.append(f"\n{texto_romano.upper()} en decimal = {valor_decimal}")

                tema.mostrar_texto_resultado(self.caja_resultado, "\n".join(lineas))

        except (ValueError, ZeroDivisionError) as error:
            self._mostrar_error(str(error))
