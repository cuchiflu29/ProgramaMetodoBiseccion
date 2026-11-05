"""
matrices.py
-----------
Operaciones básicas con matrices (listas de listas de Fraccion), sin usar
NumPy. Incluye suma, resta, multiplicación por escalar, multiplicación de
matrices y resolución de la ecuación matricial A*X = B.
"""

from core.fraccion import Fraccion
from core.gauss import resolver_sistema


def parsear_matriz(texto):
    """
    Convierte un texto de varias líneas en una matriz (lista de listas de
    Fraccion). Cada línea es una fila; los valores se separan por comas o
    espacios. Ejemplo de entrada:
        "1, 2, 3
         4, 5, 6"
    """
    lineas = [linea for linea in texto.strip().split("\n") if linea.strip() != ""]
    if len(lineas) == 0:
        raise ValueError("La matriz no puede estar vacía.")

    matriz = []
    columnas_esperadas = None
    for linea in lineas:
        limpia = linea.replace(",", " ")
        valores = [v for v in limpia.split(" ") if v.strip() != ""]
        fila = [Fraccion.desde_texto(v) for v in valores]
        if columnas_esperadas is None:
            columnas_esperadas = len(fila)
        elif len(fila) != columnas_esperadas:
            raise ValueError("Todas las filas deben tener la misma cantidad de columnas.")
        matriz.append(fila)
    return matriz


def dimensiones(matriz):
    """Retorna (filas, columnas) de la matriz."""
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0
    return filas, columnas


def matriz_a_texto(matriz):
    """Representa la matriz como filas separadas por saltos de línea, tipo [a, b, c]."""
    return "\n".join("[" + ", ".join(str(v) for v in fila) + "]" for fila in matriz)


def sumar_matrices(A, B):
    """
    Suma dos matrices A + B componente a componente. Requiere que A y B
    tengan exactamente las mismas dimensiones (m x n).
    """
    fa, ca = dimensiones(A)
    fb, cb = dimensiones(B)
    if (fa, ca) != (fb, cb):
        raise ValueError(f"Dimensiones incompatibles para sumar: A es {fa}x{ca} y B es {fb}x{cb}.")
    return [[A[i][j] + B[i][j] for j in range(ca)] for i in range(fa)]


def restar_matrices(A, B):
    """
    Resta dos matrices A - B componente a componente. Requiere las mismas
    dimensiones (m x n).
    """
    fa, ca = dimensiones(A)
    fb, cb = dimensiones(B)
    if (fa, ca) != (fb, cb):
        raise ValueError(f"Dimensiones incompatibles para restar: A es {fa}x{ca} y B es {fb}x{cb}.")
    return [[A[i][j] - B[i][j] for j in range(ca)] for i in range(fa)]


def escalar_por_matriz(k, A):
    """Multiplica cada entrada de la matriz A por el escalar k."""
    return [[k * valor for valor in fila] for fila in A]


def multiplicar_matrices(A, B):
    """
    Multiplica A (m x n) por B (n x p), usando la definición de producto
    matricial: (AB)_ij = suma_k A_ik * B_kj.
    Requiere que el número de columnas de A sea igual al número de filas de B.
    """
    fa, ca = dimensiones(A)
    fb, cb = dimensiones(B)
    if ca != fb:
        raise ValueError(f"Dimensiones incompatibles para multiplicar: columnas de A ({ca}) debe ser igual a filas de B ({fb}).")

    resultado = []
    for i in range(fa):
        fila_resultado = []
        for j in range(cb):
            suma = Fraccion(0)
            for k in range(ca):
                suma = suma + A[i][k] * B[k][j]
            fila_resultado.append(suma)
        resultado.append(fila_resultado)
    return resultado


def resolver_ecuacion_matricial(A, b):
    """
    Resuelve la ecuación matricial A*x = b (A es m x n, b es un vector
    columna de tamaño m), usando eliminación de Gauss-Jordan sobre la
    matriz aumentada [A | b] (ver core/gauss.py).

    Retorna el mismo diccionario que 'resolver_sistema'.
    """
    fa, ca = dimensiones(A)
    if len(b) != fa:
        raise ValueError(f"El vector b debe tener {fa} componentes (una por cada fila de A).")

    matriz_aumentada = [A[i][:] + [b[i]] for i in range(fa)]
    return resolver_sistema(matriz_aumentada, ca)
