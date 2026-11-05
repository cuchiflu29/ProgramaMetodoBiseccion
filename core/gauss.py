"""
gauss.py
--------
Eliminación Gaussiana y Gauss-Jordan implementadas manualmente sobre listas
de listas de Fraccion (sin NumPy). Se usa para:
  - Llevar una matriz a su Forma Escalonada (REF) y Forma Escalonada
    Reducida (RREF).
  - Resolver sistemas de ecuaciones lineales A*x = b (matriz aumentada).
  - Determinar combinaciones lineales (módulo vectores).

Procedimiento algebraico: se aplican las tres operaciones elementales de
fila (intercambiar filas, multiplicar una fila por un escalar distinto de
cero, sumar a una fila un múltiplo de otra) hasta obtener ceros debajo (y,
en Gauss-Jordan, también arriba) de cada pivote.
"""

from core.fraccion import Fraccion


def _copiar_matriz(matriz):
    return [fila[:] for fila in matriz]


def forma_escalonada(matriz, registrar_pasos=False):
    """
    Lleva 'matriz' (lista de listas de Fraccion) a su Forma Escalonada (REF):
    ceros debajo de cada pivote, pivotes de izquierda a derecha y de arriba
    hacia abajo.

    Retorna (matriz_resultado, pasos) donde 'pasos' es una lista de textos
    describiendo cada operación elemental de fila aplicada (útil para
    mostrar el procedimiento en la interfaz).
    """
    m = _copiar_matriz(matriz)
    filas = len(m)
    columnas = len(m[0]) if filas > 0 else 0
    pasos = []

    fila_pivote = 0
    for col in range(columnas):
        if fila_pivote >= filas:
            break

        # 1) Buscar una fila, desde 'fila_pivote' hacia abajo, con valor no nulo en 'col'
        fila_no_nula = None
        for f in range(fila_pivote, filas):
            if not m[f][col].es_cero():
                fila_no_nula = f
                break
        if fila_no_nula is None:
            continue  # toda la columna es cero desde aquí, pasamos a la siguiente columna

        # 2) Intercambiar filas si el pivote no está en 'fila_pivote'
        if fila_no_nula != fila_pivote:
            m[fila_pivote], m[fila_no_nula] = m[fila_no_nula], m[fila_pivote]
            if registrar_pasos:
                pasos.append(f"F{fila_pivote+1} <-> F{fila_no_nula+1}")

        # 3) Hacer ceros debajo del pivote
        pivote = m[fila_pivote][col]
        for f in range(fila_pivote + 1, filas):
            if not m[f][col].es_cero():
                factor = m[f][col] / pivote
                m[f] = [m[f][c] - factor * m[fila_pivote][c] for c in range(columnas)]
                if registrar_pasos:
                    pasos.append(f"F{f+1} -> F{f+1} - ({factor})*F{fila_pivote+1}")

        fila_pivote += 1

    return m, pasos


def forma_escalonada_reducida(matriz, registrar_pasos=False):
    """
    Lleva 'matriz' a su Forma Escalonada Reducida (RREF): además de la REF,
    cada pivote vale 1 y hay ceros arriba y debajo de él.
    """
    m, pasos = forma_escalonada(matriz, registrar_pasos)
    filas = len(m)
    columnas = len(m[0]) if filas > 0 else 0

    for f in range(filas - 1, -1, -1):
        # Buscar el pivote de la fila f (primer valor no nulo)
        col_pivote = None
        for c in range(columnas):
            if not m[f][c].es_cero():
                col_pivote = c
                break
        if col_pivote is None:
            continue

        pivote = m[f][col_pivote]
        if pivote != Fraccion(1):
            m[f] = [valor / pivote for valor in m[f]]
            if registrar_pasos:
                pasos.append(f"F{f+1} -> F{f+1} / ({pivote})")

        # Hacer ceros arriba del pivote
        for arriba in range(0, f):
            if not m[arriba][col_pivote].es_cero():
                factor = m[arriba][col_pivote]
                m[arriba] = [m[arriba][c] - factor * m[f][c] for c in range(columnas)]
                if registrar_pasos:
                    pasos.append(f"F{arriba+1} -> F{arriba+1} - ({factor})*F{f+1}")

    return m, pasos


def resolver_sistema(matriz_aumentada, num_incognitas):
    """
    Resuelve el sistema representado por la matriz aumentada [A | b]
    (num_incognitas es el número de columnas de A, sin contar b) usando
    Gauss-Jordan.

    Retorna un diccionario con:
      - 'tipo': 'unica' | 'infinitas' | 'sin_solucion'
      - 'solucion_particular': lista de Fraccion (una solución válida), o None
      - 'rref': la matriz en forma escalonada reducida
      - 'pasos': lista de operaciones de fila aplicadas
    """
    rref, pasos = forma_escalonada_reducida(matriz_aumentada, registrar_pasos=True)
    filas = len(rref)
    columnas = len(rref[0]) if filas > 0 else 0

    # Detectar inconsistencia: fila de la forma [0 0 ... 0 | c] con c != 0
    for fila in rref:
        if all(fila[c].es_cero() for c in range(num_incognitas)) and not fila[-1].es_cero():
            return {"tipo": "sin_solucion", "solucion_particular": None, "rref": rref, "pasos": pasos}

    # Identificar columnas pivote
    columnas_pivote = []
    for f in range(filas):
        for c in range(num_incognitas):
            if not rref[f][c].es_cero():
                columnas_pivote.append(c)
                break

    rango = len(columnas_pivote)
    solucion = [Fraccion(0) for _ in range(num_incognitas)]

    for idx, col in enumerate(columnas_pivote):
        solucion[col] = rref[idx][-1]

    tipo = "unica" if rango == num_incognitas else "infinitas"
    return {"tipo": tipo, "solucion_particular": solucion, "rref": rref, "pasos": pasos, "columnas_pivote": columnas_pivote}
