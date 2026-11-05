"""Interfaz del método de bisección, con tabla de iteraciones y validación."""
import customtkinter as ctk
from core.biseccion import resolver_biseccion
from ui import tema


class VistaBiseccion(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=tema.COLOR_FONDO)
        tema.crear_encabezado(self, 'ƒ', 'Método de Bisección',
                              'Aproxima raíces reales mediante intervalos y cambio de signo.')
        tarjeta = tema.crear_tarjeta(self)
        tarjeta.pack(fill='x', padx=28)
        ctk.CTkLabel(tarjeta, text='CONFIGURACIÓN DEL CÁLCULO', font=tema.FUENTE_ETIQUETA,
                     text_color=tema.COLOR_TEXTO_SUAVE).pack(anchor='w', padx=22, pady=(18, 10))
        ctk.CTkLabel(tarjeta, text='Función f(x)', font=tema.FUENTE_ETIQUETA).pack(anchor='w', padx=22)
        self.funcion = ctk.CTkEntry(tarjeta, height=42, fg_color=tema.COLOR_FONDO,
                                   border_color=tema.COLOR_BORDE, font=tema.FUENTE_MONO,
                                   placeholder_text='Ej.: x^4 - 5*x^3 + 0.5*x^2 - 11*x + 10')
        self.funcion.pack(fill='x', padx=22, pady=(6, 13))
        self.funcion.insert(0, 'x^4 - 5*x^3 + 0.5*x^2 - 11*x + 10')
        fila = ctk.CTkFrame(tarjeta, fg_color='transparent')
        fila.pack(fill='x', padx=22)
        self.campos = {}
        for titulo, clave, defecto in [('Extremo a', 'a', '0.6'), ('Extremo b', 'b', '1'),
                                       ('Tolerancia', 'tol', '0.0001'), ('Máx. iteraciones', 'max', '100')]:
            bloque = ctk.CTkFrame(fila, fg_color='transparent')
            bloque.pack(side='left', fill='x', expand=True, padx=(0, 10))
            ctk.CTkLabel(bloque, text=titulo, font=tema.FUENTE_ETIQUETA).pack(anchor='w')
            campo = ctk.CTkEntry(bloque, height=39, fg_color=tema.COLOR_FONDO,
                                 border_color=tema.COLOR_BORDE, font=tema.FUENTE_MONO)
            campo.pack(fill='x', pady=(6, 0))
            campo.insert(0, defecto)
            self.campos[clave] = campo
        botones = ctk.CTkFrame(tarjeta, fg_color='transparent')
        botones.pack(fill='x', padx=22, pady=(16, 18))
        ctk.CTkLabel(botones, text='Usa * para multiplicar; admite ^, sin, cos, sqrt, log, pi.',
                     font=('Arial', 11), text_color=tema.COLOR_TEXTO_SUAVE).pack(side='left')
        ctk.CTkButton(botones, text='CALCULAR RAÍZ  →', width=175, height=42,
                      fg_color=tema.COLOR_PRIMARIO, hover_color=tema.COLOR_PRIMARIO_HOVER,
                      font=tema.FUENTE_BOTON, command=self._calcular).pack(side='right')
        _, self.resultado = tema.crear_caja_resultado(self)
        tema.mostrar_texto_resultado(self.resultado,
            'PANTALLA DE RESULTADOS\n\nIntroduce la función y el intervalo [a, b].\n'
            'Se requiere f(a) · f(b) < 0, salvo que un extremo sea raíz exacta.\n\n'
            'Ejemplo del profesor: x^4-5*x^3+0.5*x^2-11*x+10, [0.6, 1].')

    def _calcular(self):
        try:
            expresion = self.funcion.get().strip()
            a = float(self.campos['a'].get().replace(',', '.'))
            b = float(self.campos['b'].get().replace(',', '.'))
            tol = float(self.campos['tol'].get().replace(',', '.'))
            maximo = int(self.campos['max'].get())
            r = resolver_biseccion(expresion, a, b, tol, maximo)
            lineas = ['MÉTODO DE BISECCIÓN  /  REPORTE', '━' * 64,
                      f'f(x) = {expresion}', f'Intervalo inicial: [{a:g}, {b:g}]',
                      f'Tolerancia: {tol:g}   |   Máximo: {maximo}', '',
                      f'RAÍZ APROXIMADA:  x ≈ {r["raiz"]:.12g}',
                      f'ERROR |f(c)|:    {abs(r["valor"]):.8g}',
                      f'ITERACIONES:      {len(r["pasos"])}',
                      f'ESTADO:           {r["mensaje"]}', '',
                      'TABLA DEL PROFESOR: it | a | b | c | f(a) | f(b) | f(c) | error', '━' * 64,
                      'En cada iteración: xm = (a+b)/2; conservar el subintervalo',
                      'donde f cambia de signo. Error del profesor = |f(c)|.', '']
            for paso in r['pasos']:
                lineas.append(
                    f'{paso["n"]:>2} | {paso["a"]:.9g} | {paso["b"]:.9g} | '
                    f'{paso["medio"]:.9g} | {paso["fa"]:.7g} | {paso["fb"]:.7g} | '
                    f'{paso["fm"]:.7g} | {paso["error"]:.7g}')
            tema.mostrar_texto_resultado(self.resultado, '\n'.join(lineas))
        except (ValueError, OverflowError, ArithmeticError) as exc:
            tema.mostrar_texto_resultado(self.resultado, f'No se pudo calcular:\n{exc}', es_error=True)
