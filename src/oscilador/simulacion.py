"""Oscilador con Euler explícito, Euler implícito y Newton–Raphson.

El estado se representa como ``[x, v]``. El tiempo se mide en unidades de
``1/ω``, con ``ω = sqrt(k/m)``: así la masa con resorte cumple ``x'' = -x`` y
un período dura ``2π``.

Los integradores reciben la aceleración como una función de la posición,
``a(x)``. Euler implícito recibe además su derivada ``da/dx``, que usa
Newton–Raphson.
"""

import numpy as np


def aceleracion_resorte(x: float) -> float:
    """Aceleración de la masa con resorte ideal, ``a(x) = -x``."""

    return -x


def derivada_aceleracion_resorte(x: float) -> float:
    """Derivada ``da/dx`` del resorte ideal."""

    return -1.0


def newton_raphson(
    G,
    derivada_G,
    z0: float,
    tolerancia: float = 1e-12,
    max_iter: int = 50
) -> float:

    z = z0

    for _ in range(max_iter):

        if abs(G(z)) < tolerancia:
            return z

        dG = derivada_G(z)

        if dG == 0:
            raise ArithmeticError("La derivada se anuló")

        z = z - G(z) / dG

    raise ArithmeticError("Newton-Raphson no convergió")


def integrar_euler_explicito(
    estado_inicial: np.ndarray,
    dt: float,
    pasos: int,
    aceleracion=aceleracion_resorte,
) -> tuple[np.ndarray, np.ndarray]:
    """Integra ``x' = v``, ``v' = a(x)`` con Euler explícito.

    Cada paso usa la pendiente al **comienzo** del intervalo:

        x[n+1] = x[n] + dt v[n]
        v[n+1] = v[n] + dt a(x[n])

    Devuelve un arreglo de tiempos y otro de estados. Ambos incluyen la
    condición inicial, por lo que tienen ``pasos + 1`` elementos.
    """

    tiempos = np.arange(pasos + 1) * dt
    estados = np.zeros((pasos + 1, 2))

    estados[0] = estado_inicial

    for n in range(pasos):
        x = estados[n, 0]
        v = estados[n, 1]

        estados[n + 1, 0] = x + dt * v
        estados[n + 1, 1] = v + dt * aceleracion(x)

    return tiempos, estados


def integrar_euler_implicito(
    estado_inicial: np.ndarray,
    dt: float,
    pasos: int,
    aceleracion=aceleracion_resorte,
    derivada_aceleracion=derivada_aceleracion_resorte,
) -> tuple[np.ndarray, np.ndarray]:
    """Integra ``x' = v``, ``v' = a(x)`` con Euler implícito."""

    tiempos = np.arange(pasos + 1) * dt
    estados = np.zeros((pasos + 1, 2))

    estados[0] = estado_inicial

    for n in range(pasos):
        x = estados[n, 0]
        v = estados[n, 1]

        G = lambda z: z - x - dt * v - dt**2 * aceleracion(z)
        derivada_G = lambda z: 1 - dt**2 * derivada_aceleracion(z)

        x_nuevo = newton_raphson(G, derivada_G, x)
        v_nuevo = v + dt * aceleracion(x_nuevo)

        estados[n + 1, 0] = x_nuevo
        estados[n + 1, 1] = v_nuevo

    return tiempos, estados


def solucion_exacta(tiempos: np.ndarray, estado_inicial: np.ndarray) -> np.ndarray:
    """Solución del resorte ideal, ``x(t) = x0 cos t + v0 sin t``."""

    x0, v0 = np.asarray(estado_inicial, dtype=float)
    t = np.asarray(tiempos, dtype=float)
    return np.column_stack(
        (
            x0 * np.cos(t) + v0 * np.sin(t),
            -x0 * np.sin(t) + v0 * np.cos(t),
        )
    )


def energia(estados: np.ndarray) -> np.ndarray:
    """Energía del resorte por unidad de masa, ``(v² + x²) / 2``.

    Acepta un estado ``[x, v]`` o una tabla de estados de forma ``(n, 2)``.
    """

    estados = np.asarray(estados, dtype=float)
    return 0.5 * (estados[..., 0] ** 2 + estados[..., 1] ** 2)
