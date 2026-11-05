"""
vectores.py
-----------
Operaciones algebraicas sobre vectores de R^n, implementadas componente a
componente con la clase Fraccion (sin NumPy). n se deduce automáticamente
de la cantidad de componentes que escribe el usuario.
"""

from core.fraccion import Fraccion
from core.gauss import resolver_sistema


def parsear_vector(texto):
    """
    Convierte un texto como "1, -2, 3" o "1 -2 3" en una lista de Fraccion.
    Separa por comas y/o espacios.
    """
    texto = texto.replace(",", " ")
    partes = [p for p in texto.split(" ") if p.strip() != ""]
    if len(partes) == 0:
        raise ValueError("El vector no puede estar vacío.")
    return [Fraccion.desde_texto(p) for p in partes]


def vector_a_texto(vector):
    """Representa un vector como (v1, v2, ..., vn) para mostrarlo al usuario."""
    return "(" + ", ".join(str(c) for c in vector) + ")"


def sumar_vectores(u, v):
    """
    Suma dos vectores de R^n componente a componente: (u+v)_i = u_i + v_i.
    Requiere que ambos vectores tengan la misma dimensión n.
    """
    if len(u) != len(v):
        raise ValueError(f"Los vectores deben tener la misma dimensión (u tiene {len(u)}, v tiene {len(v)}).")
    return [u[i] + v[i] for i in range(len(u))]


def restar_vectores(u, v):
    """
    Resta dos vectores de R^n componente a componente: (u-v)_i = u_i - v_i.
    """
    if len(u) != len(v):
        raise ValueError(f"Los vectores deben tener la misma dimensión (u tiene {len(u)}, v tiene {len(v)}).")
    return [u[i] - v[i] for i in range(len(u))]


def escalar_por_vector(k, u):
    """
    Multiplica un escalar k por un vector u de R^n: (k*u)_i = k * u_i.
    """
    return [k * componente for componente in u]


def es_combinacion_lineal(objetivo, vectores):
    """
    Determina si el vector 'objetivo' es combinación lineal del conjunto
    'vectores' = [v1, v2, ..., vk]. Es decir, busca escalares c1..ck tales que:

        c1*v1 + c2*v2 + ... + ck*vk = objetivo

    Procedimiento algebraico: esto equivale a resolver el sistema de
    ecuaciones lineales A*c = objetivo, donde cada columna de A es uno de
    los vectores v_i. Se arma la matriz aumentada [A | objetivo] y se resuelve
    mediante eliminación gaussiana (ver core/gauss.py).

    Retorna un diccionario con:
      - 'es_combinacion': True/False
      - 'coeficientes': lista de Fraccion (si existe solución)
      - 'mensaje': explicación del resultado
    """
    n = len(objetivo)
    k = len(vectores)
    for v in vectores:
        if len(v) != n:
            raise ValueError("Todos los vectores deben tener la misma dimensión n.")

    # Construimos la matriz aumentada [A | b] donde las columnas de A son
    # los vectores dados y b es el vector objetivo.
    matriz_aumentada = []
    for fila in range(n):
        fila_actual = [vectores[col][fila] for col in range(k)]
        fila_actual.append(objetivo[fila])
        matriz_aumentada.append(fila_actual)

    resultado = resolver_sistema(matriz_aumentada, k)

    if resultado["tipo"] == "sin_solucion":
        return {
            "es_combinacion": False,
            "coeficientes": None,
            "mensaje": "No es combinación lineal: el sistema c1*v1+...+ck*vk = objetivo no tiene solución.",
            "detalle_gauss": resultado,
        }

    # tipo == "unica" o "infinitas": en ambos casos SÍ existe al menos una combinación
    coeficientes = resultado["solucion_particular"]
    texto_combinacion = " + ".join(f"({coeficientes[i]})*v{i+1}" for i in range(k))
    mensaje = f"Sí es combinación lineal: objetivo = {texto_combinacion}"
    if resultado["tipo"] == "infinitas":
        mensaje += "\n(Existen infinitas combinaciones posibles; se muestra una de ellas.)"

    return {
        "es_combinacion": True,
        "coeficientes": coeficientes,
        "mensaje": mensaje,
        "detalle_gauss": resultado,
    }
