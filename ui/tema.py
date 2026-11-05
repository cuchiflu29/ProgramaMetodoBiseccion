"""
tema.py
-------
Paleta de colores, tipografías y funciones auxiliares de interfaz,
reutilizadas por todas las vistas para mantener un estilo consistente
(similar a las capturas de referencia del proyecto).
"""

import customtkinter as ctk

# Identidad visual: laboratorio matemático / calculadora científica
COLOR_FONDO = "#0B1120"
COLOR_TARJETA = "#151F31"
COLOR_SIDEBAR = "#0E1728"
COLOR_PRIMARIO = "#6366F1"
COLOR_PRIMARIO_HOVER = "#4F46E5"
COLOR_TEXTO = "#F1F5F9"
COLOR_TEXTO_SUAVE = "#94A3B8"
COLOR_BORDE = "#29364B"
COLOR_RESULTADO_FONDO = "#101A2A"
COLOR_ERROR = "#FB7185"
COLOR_EXITO = "#34D399"
FUENTE_TITULO = ("Arial", 25, "bold")
FUENTE_SUBTITULO = ("Arial", 13)
FUENTE_ETIQUETA = ("Arial", 12, "bold")
FUENTE_TEXTO = ("Arial", 13)
FUENTE_MONO = ("Menlo", 13)
FUENTE_BOTON = ("Arial", 13, "bold")


def crear_tarjeta(parent, **kwargs):
    """Crea un CTkFrame con estilo de 'tarjeta' (fondo blanco, bordes redondeados)."""
    tarjeta = ctk.CTkFrame(
        parent,
        fg_color=COLOR_TARJETA,
        corner_radius=18,
        border_width=1,
        border_color=COLOR_BORDE,
        **kwargs,
    )
    return tarjeta


def crear_encabezado(parent, icono, titulo, subtitulo):
    """Crea el encabezado estándar de cada vista: ícono + título + subtítulo."""
    contenedor = ctk.CTkFrame(parent, fg_color="transparent")
    contenedor.pack(fill="x", padx=28, pady=(27, 16))

    fila_titulo = ctk.CTkFrame(contenedor, fg_color="transparent")
    fila_titulo.pack(fill="x", anchor="w")

    ctk.CTkLabel(fila_titulo, text=icono, font=("Arial", 23, "bold"), text_color=COLOR_PRIMARIO).pack(side="left")
    ctk.CTkLabel(
        fila_titulo, text=titulo, font=FUENTE_TITULO, text_color=COLOR_TEXTO
    ).pack(side="left", padx=(8, 0))

    ctk.CTkLabel(
        contenedor, text=subtitulo, font=FUENTE_SUBTITULO, text_color=COLOR_TEXTO_SUAVE
    ).pack(anchor="w", pady=(4, 0))

    return contenedor


def crear_selector_operaciones(parent, opciones, comando):
    """
    Crea un control segmentado (como las pestañas u+v / u-v / k*u de las
    capturas) usando un CTkSegmentedButton.
    """
    selector = ctk.CTkSegmentedButton(
        parent,
        values=opciones,
        command=comando,
        fg_color=COLOR_FONDO,
        selected_color=COLOR_PRIMARIO,
        selected_hover_color=COLOR_PRIMARIO_HOVER,
        unselected_color=COLOR_TARJETA,
        text_color=COLOR_TEXTO,
        font=FUENTE_BOTON,
        height=36,
    )
    selector.set(opciones[0])
    return selector


def etiqueta_error(parent, texto):
    """Crea (o actualiza) una etiqueta de error en color rojo."""
    return ctk.CTkLabel(parent, text=texto, text_color=COLOR_ERROR, font=FUENTE_TEXTO, justify="left", wraplength=560)


def renderizar_vector_bracket(valores):
    """
    Devuelve un texto multilínea que dibuja un vector columna entre
    corchetes grandes usando caracteres Unicode, imitando la notación
    matemática mostrada en las capturas de referencia.
    """
    textos = [str(v) for v in valores]
    ancho = max(len(t) for t in textos) if textos else 1
    n = len(textos)

    if n == 1:
        return f"[ {textos[0]:^{ancho}} ]"

    lineas = []
    for i, t in enumerate(textos):
        if i == 0:
            izquierda, derecha = "⎡", "⎤"
        elif i == n - 1:
            izquierda, derecha = "⎣", "⎦"
        else:
            izquierda, derecha = "⎢", "⎥"
        lineas.append(f"{izquierda} {t:^{ancho}} {derecha}")
    return "\n".join(lineas)


def renderizar_matriz_bracket(matriz):
    """
    Devuelve un texto multilínea que dibuja una matriz entre corchetes
    grandes, alineando todas las columnas por su ancho máximo.
    """
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0
    anchos = [max(len(str(matriz[f][c])) for f in range(filas)) for c in range(columnas)]

    lineas = []
    for f in range(filas):
        valores = "  ".join(f"{str(matriz[f][c]):^{anchos[c]}}" for c in range(columnas))
        if filas == 1:
            izquierda, derecha = "[", "]"
        elif f == 0:
            izquierda, derecha = "⎡", "⎤"
        elif f == filas - 1:
            izquierda, derecha = "⎣", "⎦"
        else:
            izquierda, derecha = "⎢", "⎥"
        lineas.append(f"{izquierda} {valores} {derecha}")
    return "\n".join(lineas)


def crear_caja_resultado(parent):
    """
    Crea la tarjeta de 'Resultado' estándar: título + área de texto
    monoespaciada donde se muestran los cálculos y el procedimiento.
    """
    tarjeta = crear_tarjeta(parent)
    tarjeta.pack(fill="both", expand=True, padx=28, pady=(14, 24))

    encabezado = ctk.CTkFrame(tarjeta, fg_color="transparent")
    encabezado.pack(fill="x", padx=20, pady=(16, 4))
    ctk.CTkLabel(encabezado, text="Resultado", font=("Arial", 15, "bold"), text_color=COLOR_TEXTO).pack(side="left")

    caja_texto = ctk.CTkTextbox(
        tarjeta,
        font=FUENTE_MONO,
        fg_color=COLOR_RESULTADO_FONDO,
        text_color=COLOR_TEXTO,
        corner_radius=12,
        wrap="word",
        height=260,
    )
    caja_texto.pack(fill="both", expand=True, padx=20, pady=(4, 18))
    caja_texto.configure(state="disabled")
    return tarjeta, caja_texto


def mostrar_texto_resultado(caja_texto, texto, es_error=False):
    """Reemplaza el contenido de una caja de resultado (CTkTextbox)."""
    caja_texto.configure(state="normal")
    caja_texto.delete("1.0", "end")
    caja_texto.insert("1.0", texto)
    caja_texto.configure(state="disabled", text_color=COLOR_ERROR if es_error else COLOR_TEXTO)
