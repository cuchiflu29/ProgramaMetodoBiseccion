"""Interfaz de determinantes integrada con el tema original de la calculadora."""
import customtkinter as ctk
from threading import Thread
from queue import Queue, Empty
from core.determinantes import leer_matriz, recomendar_metodo, determinante_cofactores, determinante_lu
from ui import tema


class VistaDeterminantes(ctk.CTkFrame):
    """Solicita la matriz, recomienda un método y después habilita la elección."""

    def __init__(self, parent):
        """Construye los controles con los colores y fuentes existentes."""
        super().__init__(parent, fg_color=tema.COLOR_FONDO)
        self.matriz_preparada = None
        self.ocupado = False
        tema.crear_encabezado(self, 'det', 'Determinantes', 'Calcula el determinante por cofactores o descomposición LU.')
        tarjeta = tema.crear_tarjeta(self)
        tarjeta.pack(fill='x', padx=28)
        ctk.CTkLabel(tarjeta, text='Matriz cuadrada A =', font=tema.FUENTE_ETIQUETA).pack(anchor='w', padx=20, pady=(12, 0))
        self.campo_matriz = ctk.CTkTextbox(tarjeta, font=tema.FUENTE_MONO, height=95, fg_color=tema.COLOR_FONDO)
        self.campo_matriz.pack(fill='x', padx=20, pady=5)
        ctk.CTkLabel(tarjeta, text='Una fila por línea; separa valores con espacios o comas. Admite 2, -0.5 y 1/3.', font=('Segoe UI', 11), wraplength=650, justify='left').pack(anchor='w', padx=20)
        self.boton_analizar = ctk.CTkButton(tarjeta, text='1. Analizar y recomendar', command=self._analizar, font=tema.FUENTE_BOTON, fg_color=tema.COLOR_PRIMARIO)
        self.boton_analizar.pack(anchor='w', padx=20, pady=8)
        self.recomendacion = ctk.CTkLabel(tarjeta, text='Primero ingresa y analiza la matriz para ver la recomendación.', wraplength=650, justify='left', font=tema.FUENTE_TEXTO)
        self.recomendacion.pack(anchor='w', padx=20, pady=(0, 5))
        fila = ctk.CTkFrame(tarjeta, fg_color='transparent')
        fila.pack(fill='x', padx=20, pady=(0, 12))
        self.botones = []
        for metodo in ('Cofactores', 'LU'):
            boton = ctk.CTkButton(fila, text=f'2. Calcular por {metodo}', command=lambda m=metodo: self._calcular(m), state='disabled', font=tema.FUENTE_BOTON, fg_color=tema.COLOR_PRIMARIO)
            boton.pack(side='left', padx=(0, 10))
            self.botones.append(boton)
        _, self.caja_resultado = tema.crear_caja_resultado(self)
        # El evento de Tk detecta escritura, pegado, corte y deshacer.
        self.campo_matriz._textbox.bind('<<Modified>>', self._editar)
        self.campo_matriz._textbox.edit_modified(False)

    def _editar(self, evento=None):
        """Invalida la recomendación si cambia la matriz ingresada."""
        if not self.campo_matriz._textbox.edit_modified():
            return
        self.campo_matriz._textbox.edit_modified(False)
        self.matriz_preparada = None
        for boton in self.botones:
            boton.configure(state='disabled')
        self.recomendacion.configure(text='La matriz cambió. Analízala para actualizar la recomendación.')

    def _analizar(self):
        """Valida la entrada y presenta la recomendación antes de habilitar métodos."""
        try:
            self.matriz_preparada = leer_matriz(self.campo_matriz.get('1.0', 'end'))
            metodo, motivo = recomendar_metodo(self.matriz_preparada)
            self.recomendacion.configure(text=f'Recomendado: {metodo}. {motivo}')
            for boton in self.botones:
                boton.configure(state='normal')
            tema.mostrar_texto_resultado(self.caja_resultado, 'Recomendación disponible. Ahora puedes elegir cualquiera de los dos métodos.')
        except ValueError as error:
            self.matriz_preparada = None
            for boton in self.botones:
                boton.configure(state='disabled')
            tema.mostrar_texto_resultado(self.caja_resultado, str(error), es_error=True)

    def _calcular(self, metodo):
        """Calcula en segundo plano; solo el hilo principal modifica la interfaz."""
        if self.ocupado or self.matriz_preparada is None:
            return
        matriz = self.matriz_preparada
        self.ocupado = True
        self.campo_matriz.configure(state='disabled')
        self.boton_analizar.configure(state='disabled')
        for boton in self.botones:
            boton.configure(state='disabled')
        tema.mostrar_texto_resultado(self.caja_resultado, f'Calculando por {metodo}…')
        cola = Queue()

        def trabajar():
            """Produce el resultado o un error controlado sin acceder a los controles."""
            try:
                if metodo == 'Cofactores':
                    resultado, pasos = determinante_cofactores(matriz)
                    adicionales = []
                else:
                    resultado, pasos, l, u, p = determinante_lu(matriz)
                    adicionales = ['\nDescomposición P·A = L·U:', 'P:', tema.renderizar_matriz_bracket(p), 'L:', tema.renderizar_matriz_bracket(l), 'U:', tema.renderizar_matriz_bracket(u)]
                lineas = ['Matriz A:', tema.renderizar_matriz_bracket(matriz), f'\nMétodo: {metodo}', '\nProcedimiento:'] + pasos + adicionales + [f'\nDETERMINANTE: {resultado}']
                lineas.append('La matriz no tiene inversa.' if resultado.es_cero() else 'La matriz tiene inversa.')
                cola.put(('\n'.join(lineas), False))
            except Exception as error:
                cola.put((f'No se pudo completar el cálculo: {error}', True))
        Thread(target=trabajar, daemon=True).start()
        self.after(80, lambda: self._recibir(cola))

    def _recibir(self, cola):
        """Consulta la respuesta sin bloquear la ventana y restaura los controles."""
        try:
            texto, es_error = cola.get_nowait()
        except Empty:
            self.after(80, lambda: self._recibir(cola))
            return
        tema.mostrar_texto_resultado(self.caja_resultado, texto, es_error=es_error)
        self.ocupado = False
        self.campo_matriz.configure(state='normal')
        self.boton_analizar.configure(state='normal')
        for boton in self.botones:
            boton.configure(state='normal' if self.matriz_preparada is not None else 'disabled')
