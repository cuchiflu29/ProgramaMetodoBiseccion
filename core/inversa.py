"""
inversa.py
----------
Inversa de una matriz (Unidad 2.2) implementada con Python estándar y la
clase Fraccion (sin NumPy, SciPy ni el módulo 'fractions').

Definición: una matriz A de n x n es invertible si existe C de n x n tal que
    C·A = I   y   A·C = I,      donde I = I_n es la identidad.
En ese caso C = A^-1. Una matriz que no es invertible se llama singular.

Métodos incluidos:
  - Gauss-Jordan sobre [A | I]  ->  [I | A^-1]   (cualquier tamaño n x n)
  - Fórmula 2x2: si ad - bc != 0, A^-1 = 1/(ad-bc) * [[d, -b], [-c, a]]
  - Verificación A·A^-1 = I
  - Resolución de A·x = b mediante x = A^-1·b
"""

from core.fraccion import Fraccion
from core.matrices import dimensiones, multiplicar_matrices


def matriz_identidad(n):
    """Construye la matriz identidad I_n (unos en la diagonal, ceros fuera)."""
    identidad = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(Fraccion(1) if i == j else Fraccion(0))
        identidad.append(fila)
    return identidad


def es_identidad(matriz):
    """Retorna True si 'matriz' es cuadrada y es exactamente la identidad."""
    filas, columnas = dimensiones(matriz)
    if filas != columnas:
        return False
    for i in range(filas):
        for j in range(columnas):
            esperado = Fraccion(1) if i == j else Fraccion(0)
            if not (matriz[i][j] == esperado):
                return False
    return True


def validar_cuadrada(A):
    """Lanza ValueError si A no es cuadrada (solo las cuadradas pueden ser invertibles)."""
    filas, columnas = dimensiones(A)
    if filas != columnas:
        raise ValueError(
            f"La matriz debe ser cuadrada para tener inversa (A es {filas}x{columnas})."
        )
    return filas


def matriz_aumentada_con_identidad(A):
    """Arma la matriz aumentada [A | I] pegando la identidad a la derecha de A."""
    n = validar_cuadrada(A)
    identidad = matriz_identidad(n)
    return [A[i][:] + identidad[i][:] for i in range(n)]


def inversa_gauss_jordan(A):
    """
    Calcula A^-1 con Gauss-Jordan sobre la matriz aumentada [A | I].

    Procedimiento: para cada columna j se busca un pivote no nulo (de la fila
    j hacia abajo), se intercambian filas si hace falta, se divide la fila
    pivote entre el pivote para obtener un 1 y se hacen ceros en el resto de
    la columna (arriba y abajo). Si alguna columna no tiene pivote, A es
    singular. Si todas lo tienen, el bloque izquierdo queda como I y el
    derecho es A^-1.

    Retorna un diccionario con:
      - 'invertible': True/False
      - 'inversa': matriz A^-1 (lista de listas de Fraccion) o None
      - 'pasos': lista de (texto_de_la_operacion, matriz_aumentada_resultante)
      - 'inicial': la matriz [A | I] de partida
      - 'final': la matriz aumentada al terminar (o al detectar singularidad)
      - 'columna_sin_pivote': índice (base 1) de la columna que falló, o None
    """
    n = validar_cuadrada(A)
    m = matriz_aumentada_con_identidad(A)
    inicial = [fila[:] for fila in m]
    pasos = []

    for col in range(n):
        # 1) Buscar un pivote no nulo en la columna 'col' desde la fila 'col' hacia abajo
        fila_no_nula = None
        for f in range(col, n):
            if not m[f][col].es_cero():
                fila_no_nula = f
                break

        if fila_no_nula is None:
            return {
                "invertible": False,
                "inversa": None,
                "pasos": pasos,
                "inicial": inicial,
                "final": m,
                "columna_sin_pivote": col + 1,
            }

        # 2) Intercambiar filas si el pivote no está en la posición diagonal
        if fila_no_nula != col:
            m[col], m[fila_no_nula] = m[fila_no_nula], m[col]
            pasos.append((f"F{col+1} <-> F{fila_no_nula+1}", [fila[:] for fila in m]))

        # 3) Convertir el pivote en 1 dividiendo toda la fila entre él
        pivote = m[col][col]
        if not (pivote == Fraccion(1)):
            m[col] = [valor / pivote for valor in m[col]]
            pasos.append((f"F{col+1} -> F{col+1} / ({pivote})", [fila[:] for fila in m]))

        # 4) Hacer ceros en el resto de la columna (arriba y abajo del pivote)
        for f in range(n):
            if f != col and not m[f][col].es_cero():
                factor = m[f][col]
                m[f] = [m[f][c] - factor * m[col][c] for c in range(2 * n)]
                pasos.append(
                    (f"F{f+1} -> F{f+1} - ({factor})*F{col+1}", [fila[:] for fila in m])
                )

    inversa = [fila[n:] for fila in m]
    return {
        "invertible": True,
        "inversa": inversa,
        "pasos": pasos,
        "inicial": inicial,
        "final": m,
        "columna_sin_pivote": None,
    }


def determinante_2x2(A):
    """Retorna ad - bc para una matriz A = [[a, b], [c, d]]."""
    filas, columnas = dimensiones(A)
    if filas != 2 or columnas != 2:
        raise ValueError(f"La fórmula directa solo aplica a matrices 2x2 (A es {filas}x{columnas}).")
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def inversa_formula_2x2(A):
    """
    Fórmula de la inversa para A = [[a, b], [c, d]]:
        si ad - bc != 0  ->  A^-1 = 1/(ad - bc) * [[ d, -b], [-c,  a]]
        si ad - bc == 0  ->  A no es invertible.

    Retorna (determinante, inversa_o_None).
    """
    det = determinante_2x2(A)
    if det.es_cero():
        return det, None
    a, b = A[0][0], A[0][1]
    c, d = A[1][0], A[1][1]
    adjunta = [[d, -b], [-c, a]]
    inversa = [[valor / det for valor in fila] for fila in adjunta]
    return det, inversa


def verificar_inversa(A, inversa):
    """
    Verifica que A·A^-1 = I y A^-1·A = I.
    Retorna (A·A^-1, A^-1·A, ambos_son_identidad).
    """
    producto_derecho = multiplicar_matrices(A, inversa)
    producto_izquierdo = multiplicar_matrices(inversa, A)
    ok = es_identidad(producto_derecho) and es_identidad(producto_izquierdo)
    return producto_derecho, producto_izquierdo, ok


def resolver_con_inversa(A, b):
    """
    Resuelve A·x = b usando x = A^-1·b (válido solo si A es invertible).

    Retorna (inversa, x) donde x es una lista de Fraccion; si A es singular
    retorna (None, None).
    """
    n = validar_cuadrada(A)
    if len(b) != n:
        raise ValueError(f"El vector b debe tener {n} componentes (una por cada fila de A).")
    resultado = inversa_gauss_jordan(A)
    if not resultado["invertible"]:
        return None, None
    inversa = resultado["inversa"]
    columna_b = [[valor] for valor in b]
    producto = multiplicar_matrices(inversa, columna_b)
    x = [fila[0] for fila in producto]
    return inversa, x
