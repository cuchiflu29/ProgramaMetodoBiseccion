# Calculadora de Álgebra Lineal — MTM0120 (UAM)

Proyecto Integrador que cumple con los dos programas de evaluación:
**Programa Vectores** (30 pts) y **Programa Sistemas Numéricos** (20 pts).

## Cómo ejecutarlo en Visual Studio Code

1. Abre esta carpeta en VS Code (`Archivo > Abrir carpeta...`).
2. Abre una terminal (``Ctrl + ` ``) e instala la única dependencia (la
   librería gráfica; **no** se usa NumPy ni SciPy en ningún cálculo):
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## Estructura del proyecto

```
proyecto/
├── main.py                     # Ventana principal + barra lateral de navegación
├── requirements.txt
├── core/                       # TODA la lógica matemática (sin NumPy/SciPy)
│   ├── fraccion.py              # Clase Fraccion (aritmética exacta, con/sin decimales)
│   ├── vectores.py               # Suma, resta, escalar y combinación lineal
│   ├── matrices.py                # Suma, resta, escalar, producto y A·x=b
│   ├── gauss.py                    # Eliminación Gaussiana / Gauss-Jordan (REF y RREF)
│   ├── inversa.py                   # Inversa de una matriz: [A|I], fórmula 2x2, verificación
│   └── sistemas_numericos.py        # Conversión entre bases (2 a 36)
└── ui/                          # Interfaz gráfica (CustomTkinter)
    ├── tema.py                   # Colores, fuentes y widgets reutilizables
    ├── vista_vectores.py
    ├── vista_matrices.py
    ├── vista_gauss.py
    ├── vista_escalonadas.py
    ├── vista_inversa.py
    └── vista_numeros.py
```

## Módulos incluidos (barra lateral)

| Sección | Qué hace |
|---|---|
| **Vectores** | `u+v`, `u-v`, `k·u` y verificación de combinación lineal (resuelve el sistema `c1·v1+...+ck·vk = b`) |
| **Operaciones Matriciales** | `A+B`, `A-B`, `k·A`, `A×B`, validando dimensiones |
| **Eliminación Gaussiana** | Resuelve `A·x = b` con Gauss-Jordan, muestra cada operación de fila y si la solución es única, infinita o inexistente |
| **Formas Escalonadas** | Reduce cualquier matriz a su Forma Escalonada (REF) o Escalonada Reducida (RREF), paso a paso |
| **Inversa de una Matriz** | Calcula A⁻¹ con Gauss-Jordan sobre `[A \| I]` paso a paso (detecta matrices singulares), con la fórmula 2×2 `1/(ad-bc)`, verifica `A·A⁻¹ = I` y resuelve `A·x = b` con `x = A⁻¹·b` |
| **Sistemas Numéricos** | Decimal → binario/octal/hex/base-b (divisiones sucesivas) y base-b → decimal (combinación lineal por posiciones) |

## Cumplimiento del Contrato Didáctico

- **Sin NumPy, SciPy ni funciones avanzadas de `math`**: todos los cálculos
  (suma, resta, producto punto, eliminación gaussiana, MCD, potencias) están
  programados a mano en `core/` usando solo listas, condicionales, bucles y
  funciones.
- **Números exactos**: se implementó una clase `Fraccion` propia (sin usar el
  módulo `fractions`) para no perder precisión con decimales como `1/3` o `5/2`.
- **Comentarios**: cada función en `core/` documenta, en su docstring, el
  procedimiento algebraico que implementa.
- **No se conoce la dimensión n de antemano**: en vectores y matrices, `n`
  (o `m x n`) se calcula a partir de lo que el usuario escribe.

## Pendiente antes de entregar

Agrega tu **portada oficial** (UAM, FIA, asignatura, docente, grupo e
integrantes) como PDF o Word aparte, según lo pida tu profesor — el código
fuente no incluye una portada porque es un documento, no parte del programa.

## Nueva interfaz y método de bisección

La interfaz ahora utiliza una paleta oscura estilo calculadora científica, navegación lateral y pantalla de resultados. Se agregó **Método de Bisección** al menú sin quitar los módulos anteriores.

1. Instala dependencias: `python3 -m pip install -r requirements.txt`
2. Ejecuta desde la carpeta del proyecto: `python3 main.py`
3. En **Método de Bisección** introduce una función como `x^3-x-2`, `cos(x)-x` o `x^2-4`, extremos `a`, `b`, tolerancia y máximo de iteraciones.
4. Presiona **CALCULAR RAÍZ** para ver raíz aproximada, residuo y todas las iteraciones.

Se permiten `x`, `pi`, `e`, `+`, `-`, `*`, `/`, `^`, paréntesis y funciones `sin`, `cos`, `tan`, `sqrt`, `abs`, `exp`, `log`, `ln`. Usa `2*x`, no `2x`. No se utiliza `eval`, NumPy ni SciPy.

**Nota matemática:** el método requiere un cambio de signo entre los extremos (salvo que uno sea raíz exacta); el error mostrado es la cota del semiancho del intervalo. El resultado se detiene al alcanzar la tolerancia o el máximo de iteraciones.


### Bisección: ejemplo del profesor
La vista inicia con f(x)=x^4-5*x^3+0.5*x^2-11*x+10, a=0.6, b=1, tolerancia=0.0001. La columna error sigue el Excel del profesor: abs(f(c)). La salida presenta it, a, b, c, f(a), f(b), f(c), error.
