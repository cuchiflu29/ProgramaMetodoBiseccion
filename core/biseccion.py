"""Bisección con evaluación segura de expresiones matemáticas mediante AST."""
import ast
import math
import operator

_BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod}
_UN = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_FUN = {"sin": math.sin, "cos": math.cos, "tan": math.tan,
        "sqrt": math.sqrt, "abs": abs, "exp": math.exp,
        "log": math.log, "ln": math.log}
_CONST = {"pi": math.pi, "e": math.e}


def compilar_funcion(expresion):
    """Admite x, + - * / ^, paréntesis y funciones matemáticas conocidas; nunca eval()."""
    expresion = expresion.strip().replace('^', '**').replace('π', 'pi')
    if not expresion or len(expresion) > 200:
        raise ValueError('Introduce una función válida de hasta 200 caracteres.')
    try:
        raiz = ast.parse(expresion, mode='eval').body
    except SyntaxError as exc:
        raise ValueError('Sintaxis incorrecta en f(x). Usa * para multiplicar: 2*x.') from exc

    def evaluar(nodo, x, profundidad=0):
        if profundidad > 35:
            raise ValueError('Expresión demasiado compleja.')
        p = profundidad + 1
        if isinstance(nodo, ast.Constant) and type(nodo.value) in (int, float):
            return float(nodo.value)
        if isinstance(nodo, ast.Name):
            if nodo.id == 'x':
                return x
            if nodo.id in _CONST:
                return _CONST[nodo.id]
            raise ValueError(f'Variable desconocida: {nodo.id}')
        if isinstance(nodo, ast.BinOp) and type(nodo.op) in _BIN:
            izq, der = evaluar(nodo.left, x, p), evaluar(nodo.right, x, p)
            if isinstance(nodo.op, ast.Pow) and abs(der) > 100:
                raise ValueError('Exponente demasiado grande.')
            return _BIN[type(nodo.op)](izq, der)
        if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _UN:
            return _UN[type(nodo.op)](evaluar(nodo.operand, x, p))
        if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name) and not nodo.keywords:
            nombre = nodo.func.id
            if nombre in _FUN and len(nodo.args) == 1:
                return _FUN[nombre](evaluar(nodo.args[0], x, p))
        raise ValueError('Operación no permitida en f(x).')

    def funcion(x):
        try:
            y = float(evaluar(raiz, x))
            if not math.isfinite(y):
                raise ValueError('La función no es finita en el intervalo.')
            return y
        except (OverflowError, ZeroDivisionError, TypeError) as exc:
            raise ValueError(f'No se puede evaluar f({x:g}): {exc}') from exc
    return funcion


def resolver_biseccion(expresion, a, b, tolerancia=1e-6, max_iter=100):
    if not all(math.isfinite(v) for v in (a, b, tolerancia)):
        raise ValueError('Los valores deben ser números finitos.')
    if a >= b:
        raise ValueError('El extremo a debe ser menor que b.')
    if tolerancia <= 0:
        raise ValueError('La tolerancia debe ser mayor que cero.')
    if not 1 <= max_iter <= 1000:
        raise ValueError('Las iteraciones deben estar entre 1 y 1000.')
    f = compilar_funcion(expresion)
    fa, fb = f(a), f(b)
    if fa == 0:
        return {'raiz': a, 'valor': 0.0, 'pasos': [], 'convergio': True, 'mensaje': 'a es raíz exacta.'}
    if fb == 0:
        return {'raiz': b, 'valor': 0.0, 'pasos': [], 'convergio': True, 'mensaje': 'b es raíz exacta.'}
    if (fa > 0) == (fb > 0):
        raise ValueError('No hay cambio de signo: f(a) y f(b) deben tener signos opuestos.')
    pasos = []
    for i in range(1, max_iter + 1):
        medio = a + (b-a)/2
        fm = f(medio)
        error_intervalo = abs(b-a)/2
        error = abs(fm)  # Criterio del Excel del profesor: |f(c)|
        pasos.append({'n': i, 'a': a, 'b': b, 'fa': fa, 'fb': fb,
                      'medio': medio, 'fm': fm, 'error': error, 'error_intervalo': error_intervalo})
        if fm == 0 or error <= tolerancia:
            return {'raiz': medio, 'valor': fm, 'pasos': pasos, 'convergio': True,
                    'mensaje': 'Tolerancia |f(c)| alcanzada o raíz exacta.'}
        if (fa > 0) != (fm > 0):
            b, fb = medio, fm
        else:
            a, fa = medio, fm
    return {'raiz': medio, 'valor': fm, 'pasos': pasos, 'convergio': False,
            'mensaje': 'Se alcanzó el máximo de iteraciones sin cumplir la tolerancia.'}
