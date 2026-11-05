"""
determinantes.py
----------------
Calcula determinantes por cofactores y descomposición LU.

Incluye:
- Lectura de enteros, decimales y fracciones.
- Validación de matrices cuadradas.
- Recomendación previa del método.
- Procedimientos explicados con pasos numerados.
- Cálculos exactos mediante la clase Fraccion del proyecto.

No utiliza NumPy, SciPy ni funciones avanzadas de math.
"""

from core.fraccion import Fraccion


# ============================================================
# LECTURA Y VALIDACIÓN DE LA MATRIZ
# ============================================================

def leer_matriz(texto):
    """
    Convierte el texto ingresado en una matriz de fracciones.

    Cada línea representa una fila.
    Los valores se separan con espacios o comas.
    Los decimales se escriben con punto.

    Ejemplo:
        1 2 3
        4 5 6
        7 8 9
    """
    matriz = []

    for linea in texto.strip().splitlines():
        if not linea.strip():
            continue

        fila = []

        for valor in linea.replace(",", " ").split():
            try:
                # Convierte un decimal directamente a una razón
                # de enteros para evitar redondeos intermedios.
                if "." in valor and "/" not in valor:
                    signo = -1 if valor.startswith("-") else 1

                    limpio = (
                        valor[1:]
                        if valor.startswith(("+", "-"))
                        else valor
                    )

                    partes = limpio.split(".")

                    if len(partes) != 2:
                        raise ValueError()

                    digitos = "".join(partes)

                    if not digitos.isascii() or not digitos.isdigit():
                        raise ValueError()

                    numerador = signo * int(digitos)
                    denominador = 10 ** len(partes[1])

                    numero = Fraccion(numerador, denominador)

                else:
                    numero = Fraccion.desde_texto(valor)

                fila.append(numero)

            except (ValueError, ZeroDivisionError, OverflowError):
                raise ValueError(
                    f"Valor inválido: {valor}. "
                    "Usa enteros, decimales con punto o fracciones "
                    "con denominador distinto de cero."
                ) from None

        matriz.append(fila)

    validar_matriz(matriz)
    return matriz


def validar_matriz(matriz):
    """
    Comprueba que la matriz sea cuadrada y no esté vacía.

    El determinante solo se define para matrices cuadradas.
    """
    if not matriz:
        raise ValueError("La matriz no puede estar vacía.")

    n = len(matriz)

    for fila in matriz:
        if len(fila) != n:
            raise ValueError(
                "La matriz debe ser cuadrada: todas las filas "
                "deben tener tantos elementos como filas tiene la matriz."
            )


# ============================================================
# PRESENTACIÓN DE LAS MATRICES
# ============================================================

def _texto_matriz(matriz):
    """Representa una matriz alineando sus columnas."""
    columnas = len(matriz[0])

    anchos = [
        max(len(str(fila[j])) for fila in matriz)
        for j in range(columnas)
    ]

    lineas = []

    for fila in matriz:
        valores = "  ".join(
            str(valor).rjust(anchos[j])
            for j, valor in enumerate(fila)
        )
        lineas.append(f"[ {valores} ]")

    return "\n".join(lineas)


# ============================================================
# RECOMENDACIÓN DEL MÉTODO
# ============================================================

def _eje_expansion(matriz):
    """
    Encuentra la fila o columna con menos elementos no nulos.

    Expandir por ese eje permite omitir más términos iguales a cero.
    """
    n = len(matriz)
    mejor = (n + 1, "fila", 0)

    for i in range(n):
        for tipo in ("fila", "columna"):
            cantidad = 0

            for j in range(n):
                valor = (
                    matriz[i][j]
                    if tipo == "fila"
                    else matriz[j][i]
                )

                if not valor.es_cero():
                    cantidad += 1

            if cantidad < mejor[0]:
                mejor = (cantidad, tipo, i)

    return mejor


def recomendar_metodo(matriz):
    """
    Recomienda un método antes de ejecutar el cálculo.

    La recomendación es una estimación basada en el orden y
    la presencia de ceros, no una medición del tiempo real.
    """
    validar_matriz(matriz)

    n = len(matriz)
    cantidad, tipo, indice = _eje_expansion(matriz)

    if n <= 3:
        return (
            "Cofactores",
            "Para matrices de orden 1 a 3, cofactores requiere "
            "pocos cálculos y facilita comprender el procedimiento."
        )

    if cantidad <= 1:
        return (
            "Cofactores",
            f"La {tipo} {indice + 1} tiene {cantidad} elementos "
            "no nulos, por lo que la expansión se simplifica."
        )

    return (
        "LU",
        "Para esta matriz se recomienda LU. Su costo general "
        "es cúbico, mientras que cofactores puede crecer "
        "factorialmente. Esta recomendación es una estimación."
    )


# ============================================================
# DETERMINANTE POR COFACTORES
# ============================================================

def determinante_cofactores(matriz, registrar_pasos=True):
    """
    Calcula el determinante mediante expansión de Laplace.

    Para cada elemento seleccionado:
    1. Construye su menor.
    2. Calcula el determinante del menor.
    3. Aplica el signo del cofactor.
    4. Multiplica el elemento por su cofactor.
    5. Acumula las contribuciones.

    Devuelve el determinante y los pasos explicados.
    """
    validar_matriz(matriz)

    pasos = []
    llamadas = 0

    def anotar(explicacion):
        """Registra una explicación con numeración consecutiva."""
        if registrar_pasos:
            pasos.append(
                f"Paso {len(pasos) + 1}:\n{explicacion}\n"
            )

    def expandir(a, nombre):
        """Desarrolla el determinante de una matriz y sus menores."""
        nonlocal llamadas
        llamadas += 1

        # La expansión puede requerir una cantidad excesiva de
        # operaciones. Se interrumpe sin presentar un resultado parcial.
        if llamadas > 10000:
            raise ValueError(
                "Esta expansión requiere demasiados cálculos. "
                "Selecciona LU para esta matriz."
            )

        n = len(a)

        anotar(
            f"Calculamos el determinante de {nombre}, "
            f"una matriz de orden {n}:\n"
            f"{_texto_matriz(a)}"
        )

        # Caso base: matriz de un solo elemento.
        if n == 1:
            resultado = a[0][0]

            anotar(
                "En una matriz de orden 1, el determinante "
                "es su único elemento.\n"
                f"det({nombre}) = {resultado}"
            )

            return resultado

        # Caso base: diferencia de productos en una matriz 2 por 2.
        if n == 2:
            principal = a[0][0] * a[1][1]
            secundaria = a[0][1] * a[1][0]

            anotar(
                "Para una matriz de orden 2 aplicamos:\n"
                "det = a11 × a22 - a12 × a21.\n"
                "Primero multiplicamos la diagonal principal:\n"
                f"({a[0][0]}) × ({a[1][1]}) = {principal}"
            )

            anotar(
                "Multiplicamos la diagonal secundaria:\n"
                f"({a[0][1]}) × ({a[1][0]}) = {secundaria}"
            )

            resultado = principal - secundaria

            anotar(
                "Restamos el producto de la diagonal secundaria "
                "al de la principal:\n"
                f"det({nombre}) = ({principal}) "
                f"- ({secundaria}) = {resultado}"
            )

            return resultado

        # Se elige el eje que permite omitir más términos nulos.
        _, tipo, indice = _eje_expansion(a)

        anotar(
            f"Elegimos la {tipo} {indice + 1} de {nombre}, "
            "porque tiene la menor cantidad de elementos no nulos.\n"
            "Aplicamos la expansión de Laplace:\n"
            "det = suma de elemento × cofactor.\n"
            "El cofactor se calcula con:\n"
            "C(i,j) = (-1)^(i+j) × det(M(i,j)).\n"
            "Las posiciones se numeran desde 1."
        )

        total = Fraccion(0)
        terminos = []

        for k in range(n):
            if tipo == "fila":
                i, j = indice, k
            else:
                i, j = k, indice

            elemento = a[i][j]

            # Un coeficiente cero produce una contribución nula.
            if elemento.es_cero():
                anotar(
                    f"En {nombre}, el elemento de la posición "
                    f"({i + 1}, {j + 1}) es cero.\n"
                    "Su contribución es 0 × cofactor = 0.\n"
                    "Por eso no necesitamos desarrollar su menor."
                )
                continue

            # El menor se forma eliminando la fila y la columna
            # correspondientes al elemento seleccionado.
            menor = [
                [
                    a[f][c]
                    for c in range(n)
                    if c != j
                ]
                for f in range(n)
                if f != i
            ]

            nombre_menor = f"{nombre}/M({i + 1},{j + 1})"
            signo = 1 if (i + j) % 2 == 0 else -1

            anotar(
                f"Tomamos el elemento {elemento} de {nombre}, "
                f"ubicado en ({i + 1}, {j + 1}).\n"
                f"Eliminamos la fila {i + 1} "
                f"y la columna {j + 1}.\n"
                f"El menor {nombre_menor} es:\n"
                f"{_texto_matriz(menor)}\n\n"
                "Calculamos el signo correspondiente:\n"
                f"(-1)^({i + 1} + {j + 1}) = {signo}"
            )

            # Se desarrolla el menor con el mismo procedimiento.
            det_menor = expandir(menor, nombre_menor)
            cofactor = signo * det_menor

            anotar(
                f"El determinante de {nombre_menor} "
                f"es {det_menor}.\n"
                "Multiplicamos ese determinante por el signo:\n"
                f"C({i + 1},{j + 1}) = "
                f"({signo}) × ({det_menor}) = {cofactor}"
            )

            termino = elemento * cofactor
            anterior = total
            total = total + termino
            terminos.append(str(termino))

            anotar(
                f"Volvemos a la expansión de {nombre}.\n"
                "Multiplicamos el elemento por su cofactor:\n"
                f"({elemento}) × ({cofactor}) = {termino}\n\n"
                "Sumamos esta contribución al acumulado:\n"
                f"({anterior}) + ({termino}) = {total}"
            )

        suma = " + ".join(
            f"({termino})" for termino in terminos
        ) or "0"

        anotar(
            f"Terminamos la expansión de {nombre}.\n"
            "Sumamos todas las contribuciones no nulas:\n"
            f"det({nombre}) = {suma} = {total}"
        )

        return total

    try:
        resultado = expandir(matriz, "A")

    except RecursionError:
        raise ValueError(
            "La expansión requiere demasiados niveles. Selecciona LU."
        ) from None

    anotar(
        "El procedimiento por cofactores ha terminado.\n"
        f"DETERMINANTE DE A = {resultado}"
    )

    return resultado, pasos


# ============================================================
# DETERMINANTE POR DESCOMPOSICIÓN LU
# ============================================================

def determinante_lu(matriz, registrar_pasos=True):
    """
    Construye una descomposición P*A=L*U con pivoteo parcial.

    L es triangular inferior con diagonal igual a uno.
    U es triangular superior.
    P registra los intercambios de filas.

    El determinante se calcula mediante:
        det(A) = (-1)^intercambios × producto de la diagonal de U.

    Devuelve:
        determinante, pasos, L, U, P.
    """
    validar_matriz(matriz)

    n = len(matriz)

    # Se copia la matriz para conservar intactos los datos originales.
    u = [fila[:] for fila in matriz]

    l = [
        [
            Fraccion(1 if i == j else 0)
            for j in range(n)
        ]
        for i in range(n)
    ]

    p = [
        [
            Fraccion(1 if i == j else 0)
            for j in range(n)
        ]
        for i in range(n)
    ]

    pasos = []
    cambios = 0

    def anotar(explicacion):
        """Registra una explicación con numeración consecutiva."""
        if registrar_pasos:
            pasos.append(
                f"Paso {len(pasos) + 1}:\n{explicacion}\n"
            )

    anotar(
        "Buscamos la descomposición P × A = L × U.\n"
        "P registra los intercambios de filas.\n"
        "L guarda los multiplicadores de la eliminación.\n"
        "U se transforma en una matriz triangular superior.\n\n"
        "Inicialmente U = A, mientras L y P son "
        "matrices identidad.\n\n"
        f"U inicial:\n{_texto_matriz(u)}\n\n"
        f"L inicial:\n{_texto_matriz(l)}\n\n"
        f"P inicial:\n{_texto_matriz(p)}"
    )

    # Se selecciona un pivote y se eliminan los elementos
    # inferiores en cada columna.
    for k in range(n):
        pivote = k

        # El pivoteo parcial escoge el candidato de mayor
        # valor absoluto usando comparaciones exactas.
        for i in range(k + 1, n):
            actual = Fraccion(
                abs(u[pivote][k].numerador),
                u[pivote][k].denominador
            )

            candidato = Fraccion(
                abs(u[i][k].numerador),
                u[i][k].denominador
            )

            if actual < candidato:
                pivote = i

        candidatos = ", ".join(
            f"F{i + 1}: {u[i][k]}"
            for i in range(k, n)
        )

        anotar(
            f"Procesamos la columna {k + 1}.\n"
            f"Candidatos para el pivote: {candidatos}.\n"
            "Buscamos el candidato de mayor valor absoluto "
            "entre la fila actual y las inferiores."
        )

        # Si no existe un pivote no nulo, la matriz es singular.
        # Se continúa para completar la descomposición.
        if u[pivote][k].es_cero():
            anotar(
                "Todos los candidatos de esta columna son cero.\n"
                "No hay un pivote no nulo y no dividimos entre cero.\n"
                "La matriz es singular: su determinante será cero.\n"
                "Continuamos con las columnas restantes "
                "para completar L y U."
            )
            continue

        # Los intercambios deben actualizar U y P.
        # También se permutan los multiplicadores anteriores de L.
        if pivote != k:
            u[k], u[pivote] = u[pivote], u[k]
            p[k], p[pivote] = p[pivote], p[k]

            for j in range(k):
                l[k][j], l[pivote][j] = (
                    l[pivote][j],
                    l[k][j]
                )

            cambios += 1

            anotar(
                f"El candidato elegido está en la fila "
                f"{pivote + 1}.\n"
                f"Intercambiamos F{k + 1} con F{pivote + 1}.\n"
                "Actualizamos P y los multiplicadores anteriores "
                "de L para conservar P × A = L × U.\n"
                "Cada intercambio cambia el signo del determinante.\n"
                f"Intercambios acumulados: {cambios}.\n\n"
                f"U actual:\n{_texto_matriz(u)}\n\n"
                f"L actual:\n{_texto_matriz(l)}\n\n"
                f"P actual:\n{_texto_matriz(p)}"
            )

        else:
            anotar(
                f"El pivote elegido es {u[k][k]} y ya está "
                f"en la posición ({k + 1}, {k + 1}).\n"
                "No necesitamos intercambiar filas."
            )

        # Se calculan y aplican los multiplicadores de eliminación.
        for i in range(k + 1, n):
            entrada = u[i][k]
            valor_pivote = u[k][k]
            factor = entrada / valor_pivote

            l[i][k] = factor

            anotar(
                f"Queremos anular U({i + 1},{k + 1}) = {entrada}.\n"
                "Calculamos el multiplicador:\n"
                f"m = U({i + 1},{k + 1}) / "
                f"U({k + 1},{k + 1})\n"
                f"m = ({entrada}) / ({valor_pivote}) = {factor}\n"
                f"Guardamos este valor en L({i + 1},{k + 1})."
            )

            if factor.es_cero():
                anotar(
                    "La entrada que queremos anular ya es cero.\n"
                    "El multiplicador es cero y la fila no cambia."
                )
                continue

            anotar(
                f"Aplicamos la operación:\n"
                f"F{i + 1} ← F{i + 1} "
                f"- ({factor}) × F{k + 1}\n\n"
                "Restar un múltiplo de otra fila conserva "
                "el determinante.\n"
                "A continuación actualizamos las entradas "
                "desde la columna del pivote."
            )

            for j in range(k, n):
                anterior = u[i][j]
                referencia = u[k][j]
                producto = factor * referencia
                nuevo = anterior - producto

                u[i][j] = nuevo

                anotar(
                    f"Actualizamos U({i + 1},{j + 1}):\n"
                    "nuevo valor = valor anterior "
                    "- multiplicador × valor de la fila pivote\n"
                    f"= ({anterior}) - ({factor}) × ({referencia})\n"
                    f"= ({anterior}) - ({producto})\n"
                    f"= {nuevo}"
                )

            anotar(
                f"Terminamos de modificar la fila {i + 1}.\n"
                f"La posición ({i + 1},{k + 1}) ahora es cero.\n\n"
                f"U actual:\n{_texto_matriz(u)}\n\n"
                f"L actual:\n{_texto_matriz(l)}"
            )

    anotar(
        "La eliminación ha terminado.\n"
        "U es triangular superior.\n"
        "L es triangular inferior con unos en su diagonal.\n\n"
        f"P final:\n{_texto_matriz(p)}\n\n"
        f"L final:\n{_texto_matriz(l)}\n\n"
        f"U final:\n{_texto_matriz(u)}\n\n"
        "Las matrices obtenidas cumplen P × A = L × U."
    )

    # El determinante de una matriz triangular se obtiene
    # multiplicando los elementos de su diagonal principal.
    producto = Fraccion(1)

    anotar(
        "Calculamos det(U).\n"
        "Como U es triangular, su determinante es "
        "el producto de los elementos de la diagonal principal.\n"
        "Iniciamos el producto acumulado en 1."
    )

    for i in range(n):
        anterior = producto
        producto = producto * u[i][i]

        anotar(
            f"Tomamos U({i + 1},{i + 1}) = {u[i][i]}.\n"
            "Lo multiplicamos por el acumulado:\n"
            f"({anterior}) × ({u[i][i]}) = {producto}"
        )

    # Se corrige el signo según la cantidad de intercambios.
    signo = -1 if cambios % 2 else 1
    resultado = signo * producto

    anotar(
        "La diagonal de L contiene únicamente unos, "
        "por lo tanto det(L) = 1.\n"
        f"El producto diagonal de U es {producto}.\n"
        f"Se realizaron {cambios} intercambios de filas.\n"
        f"El factor de signo es (-1)^{cambios} = {signo}.\n\n"
        "Aplicamos la fórmula:\n"
        "det(A) = (-1)^intercambios × det(U)\n"
        f"det(A) = ({signo}) × ({producto}) = {resultado}\n\n"
        f"DETERMINANTE DE A = {resultado}"
    )

    return resultado, pasos, l, u, p