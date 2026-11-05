"""
sistemas_numericos.py
----------------------
Conversión de números entre distintas bases numéricas (binario, octal,
hexadecimal o cualquier base entre 2 y 36), usando únicamente aritmética
entera de Python estándar (sin funciones de conversión "mágicas" como
bin(), oct(), hex() o int(x, base), ya que el objetivo es que el algoritmo
quede explícito, tal como pide el Contrato Didáctico).
"""

DIGITOS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def decimal_a_base(numero, base):
    """
    Convierte un entero decimal a su representación en 'base' (2 a 36),
    usando el método de divisiones sucesivas:

        Se divide el número entre la base, se guarda el residuo (que es
        un dígito de la respuesta) y se repite el proceso con el cociente
        obtenido, hasta que el cociente sea 0. La respuesta se lee de
        abajo hacia arriba (últ. residuo obtenido -> dígito más
        significativo).

    Retorna (resultado_texto, pasos) donde 'pasos' es una lista de
    tuplas (dividendo, base, cociente, residuo) para poder mostrar la
    tabla de divisiones sucesivas en la interfaz.
    """
    if base < 2 or base > 36:
        raise ValueError("La base debe estar entre 2 y 36.")

    negativo = numero < 0
    numero = abs(numero)

    if numero == 0:
        return "0", [(0, base, 0, 0)]

    pasos = []
    digitos_resultado = []
    actual = numero
    while actual > 0:
        cociente = actual // base
        residuo = actual % base
        pasos.append((actual, base, cociente, residuo))
        digitos_resultado.append(DIGITOS[residuo])
        actual = cociente

    digitos_resultado.reverse()
    resultado = "".join(digitos_resultado)
    if negativo:
        resultado = "-" + resultado
    return resultado, pasos


def base_a_decimal(texto, base):
    """
    Convierte un número escrito en 'base' (2 a 36) a su valor decimal,
    usando el método de la combinación lineal por posiciones:

        Si el número tiene dígitos d_k d_(k-1) ... d_1 d_0 (de izquierda
        a derecha), su valor decimal es:

            d_k*base^k + d_(k-1)*base^(k-1) + ... + d_1*base^1 + d_0*base^0

    Retorna (valor_decimal, pasos_combinacion) donde 'pasos_combinacion'
    es una lista de tuplas (digito, valor_digito, potencia, aporte) para
    poder mostrar la combinación lineal completa en la interfaz, tal como
    exige el enunciado ("debe mostrarse la combinación lineal que genera
    cada número").
    """
    if base < 2 or base > 36:
        raise ValueError("La base debe estar entre 2 y 36.")

    texto = texto.strip().upper()
    negativo = texto.startswith("-")
    if negativo:
        texto = texto[1:]
    if texto == "":
        raise ValueError("El número no puede estar vacío.")

    n = len(texto)
    valor_total = 0
    pasos_combinacion = []

    for indice, caracter in enumerate(texto):
        if caracter not in DIGITOS[:base]:
            raise ValueError(f"El dígito '{caracter}' no es válido en base {base}.")
        valor_digito = DIGITOS.index(caracter)
        potencia = n - indice - 1
        aporte = valor_digito * (base ** potencia)
        valor_total += aporte
        pasos_combinacion.append((caracter, valor_digito, potencia, aporte))

    if negativo:
        valor_total = -valor_total

    return valor_total, pasos_combinacion


def texto_combinacion_lineal(pasos_combinacion, base):
    """
    Arma el texto de la combinación lineal, por ejemplo para "2A" en base 16:
        (2 * 16^1) + (10 * 16^0) = 32 + 10 = 42
    """
    terminos = [f"({p[1]} * {base}^{p[2]})" for p in pasos_combinacion]
    aportes = [str(p[3]) for p in pasos_combinacion]
    total = sum(p[3] for p in pasos_combinacion)
    return f"{' + '.join(terminos)} = {' + '.join(aportes)} = {total}"

