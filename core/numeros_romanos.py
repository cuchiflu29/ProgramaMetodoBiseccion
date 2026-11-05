"""
numeros_romanos.py
--------------------
Conversión de números decimales a números romanos, usando el algoritmo
"goloso" (greedy) clásico: se resta el valor romano más grande posible,
una y otra vez, hasta llegar a cero. Implementado con Python estándar,
sin librerías externas.

El sistema de numeración romano clásico solo representa enteros positivos
entre 1 y 3999 (no existe un símbolo romano estándar para el 0, ni una
notación aceptada universalmente para números mayores o decimales).
"""

# Lista ordenada de mayor a menor: (valor decimal, símbolo romano).
# Incluye los casos "restados" (4, 9, 40, 90, 400, 900) para poder resolver
# el algoritmo con una sola pasada, sin casos especiales adicionales.
TABLA_ROMANA = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
    (1, "I"),
]


def decimal_a_romano(numero):
    """
    Convierte un entero 'numero' (1 a 3999) a su representación en números
    romanos, usando el algoritmo goloso:

        Mientras el número sea mayor que 0, se busca el valor más grande
        de la tabla que quepa dentro del número, se agrega su símbolo al
        resultado, y se resta ese valor del número. Se repite hasta llegar
        a 0.

    Retorna (resultado_texto, pasos) donde 'pasos' es una lista de tuplas
    (valor_usado, simbolo, numero_antes, numero_despues) para mostrar el
    procedimiento en la interfaz.
    """
    if not isinstance(numero, int):
        raise ValueError("El número debe ser un entero (los romanos no representan decimales).")
    if numero < 1 or numero > 3999:
        raise ValueError("El sistema romano clásico solo representa enteros entre 1 y 3999.")

    restante = numero
    resultado = []
    pasos = []

    for valor, simbolo in TABLA_ROMANA:
        while restante >= valor:
            antes = restante
            restante -= valor
            resultado.append(simbolo)
            pasos.append((valor, simbolo, antes, restante))

    return "".join(resultado), pasos


def romano_a_decimal(texto):
    """
    Convierte un número romano (texto) a su valor decimal, recorriendo los
    símbolos de izquierda a derecha: si el valor de un símbolo es menor que
    el del símbolo siguiente, se resta (caso IV, IX, XL, etc.); si no, se
    suma. Esta es la regla clásica de lectura de números romanos.
    """
    valores = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    texto = texto.strip().upper()
    if texto == "":
        raise ValueError("Debes escribir un número romano.")
    for caracter in texto:
        if caracter not in valores:
            raise ValueError(f"'{caracter}' no es un símbolo romano válido (usa I, V, X, L, C, D, M).")

    total = 0
    pasos = []
    n = len(texto)
    for i in range(n):
        valor_actual = valores[texto[i]]
        valor_siguiente = valores[texto[i + 1]] if i + 1 < n else 0
        if valor_actual < valor_siguiente:
            total -= valor_actual
            pasos.append((texto[i], valor_actual, "resta"))
        else:
            total += valor_actual
            pasos.append((texto[i], valor_actual, "suma"))

    return total, pasos
