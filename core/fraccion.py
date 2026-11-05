"""
fraccion.py
-----------
Clase Fraccion implementada 100% con Python estándar (sin usar el módulo
'fractions' ni funciones avanzadas de 'math'), tal como exige el Contrato
Didáctico del curso (solo listas, condicionales, bucles y funciones).

Se usa para representar números racionales exactos (ej: -1/2, 5/2) en
vectores, matrices y sistemas, evitando errores de redondeo de los flotantes.
"""


def _maximo_comun_divisor(a, b):
    """
    Calcula el Máximo Común Divisor de dos enteros usando el algoritmo
    de Euclides (restas sucesivas mediante el operador módulo), escrito
    manualmente sin usar math.gcd.
    """
    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a if a != 0 else 1


class Fraccion:
    """
    Representa un número racional numerador/denominador ya simplificado.
    El signo siempre se guarda en el numerador (el denominador es positivo).
    """

    def __init__(self, numerador, denominador=1):
        if denominador == 0:
            raise ZeroDivisionError("El denominador de una fracción no puede ser 0.")

        # Si nos pasan flotantes (ej. 0.5), los convertimos a fracción exacta
        if isinstance(numerador, float) or isinstance(denominador, float):
            numerador, denominador = self._de_decimal(numerador, denominador)

        if denominador < 0:
            numerador = -numerador
            denominador = -denominador

        divisor = _maximo_comun_divisor(numerador, denominador)
        self.numerador = numerador // divisor
        self.denominador = denominador // divisor

    @staticmethod
    def _de_decimal(num, den):
        """Convierte una división con flotantes a una fracción entera exacta."""
        valor = num / den
        # Multiplicamos por potencias de 10 hasta obtener un entero
        texto = repr(valor)
        if "e" in texto or "E" in texto:
            # Notación científica: usamos una aproximación con muchos decimales
            texto = f"{valor:.10f}"
        signo = -1 if texto.startswith("-") else 1
        texto = texto.lstrip("-")
        if "." in texto:
            parte_entera, parte_decimal = texto.split(".")
        else:
            parte_entera, parte_decimal = texto, ""
        parte_decimal = parte_decimal.rstrip("0")
        denom = 10 ** len(parte_decimal)
        numer = int(parte_entera + parte_decimal) if (parte_entera + parte_decimal) != "" else 0
        return signo * numer, denom

    @staticmethod
    def desde_texto(texto):
        """
        Crea una Fraccion a partir de un texto escrito por el usuario.
        Admite enteros ("5"), decimales ("0.5", "-1.25") y fracciones
        escritas como "num/den" (ej. "-1/2", "5/2").
        """
        texto = texto.strip()
        if texto == "":
            raise ValueError("Se encontró un valor vacío.")
        if "/" in texto:
            num_txt, den_txt = texto.split("/")
            return Fraccion(int(num_txt.strip()), int(den_txt.strip()))
        if "." in texto:
            return Fraccion(float(texto))
        return Fraccion(int(texto))

    # ---------- Operaciones aritméticas ----------
    def __add__(self, otra):
        otra = self._a_fraccion(otra)
        return Fraccion(
            self.numerador * otra.denominador + otra.numerador * self.denominador,
            self.denominador * otra.denominador,
        )

    def __sub__(self, otra):
        otra = self._a_fraccion(otra)
        return Fraccion(
            self.numerador * otra.denominador - otra.numerador * self.denominador,
            self.denominador * otra.denominador,
        )

    def __mul__(self, otra):
        otra = self._a_fraccion(otra)
        return Fraccion(self.numerador * otra.numerador, self.denominador * otra.denominador)

    def __rmul__(self, otra):
        return self.__mul__(otra)

    def __truediv__(self, otra):
        otra = self._a_fraccion(otra)
        if otra.numerador == 0:
            raise ZeroDivisionError("División entre cero.")
        return Fraccion(self.numerador * otra.denominador, self.denominador * otra.numerador)

    def __neg__(self):
        return Fraccion(-self.numerador, self.denominador)

    def __eq__(self, otra):
        otra = self._a_fraccion(otra)
        return self.numerador == otra.numerador and self.denominador == otra.denominador

    def __lt__(self, otra):
        otra = self._a_fraccion(otra)
        return self.numerador * otra.denominador < otra.numerador * self.denominador

    def es_cero(self):
        return self.numerador == 0

    @staticmethod
    def _a_fraccion(valor):
        if isinstance(valor, Fraccion):
            return valor
        return Fraccion(valor)

    def a_float(self):
        return self.numerador / self.denominador

    # ---------- Representación ----------
    def __str__(self):
        if self.denominador == 1:
            return str(self.numerador)
        return f"{self.numerador}/{self.denominador}"

    def __repr__(self):
        return self.__str__()
