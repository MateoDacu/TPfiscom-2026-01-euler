# Pregunta y predicciones

Completen este archivo **antes** de ejecutar los experimentos.

## Pregunta

¿Qué evidencia necesitamos para confiar en una trayectoria del oscilador
calculada durante muchos ciclos?

## Modelo y supuestos

- Una masa unida a un resorte ideal, sin rozamiento: $m x''=-kx$.
- Medimos el tiempo en unidades de $1/\omega$, con $\omega=\sqrt{k/m}$. Así la
  ecuación queda $x''=-x$ y un período dura $2\pi$.
- La energía por unidad de masa es $E=(x^2+v^2)/2$.

## Predicciones

1. ¿Qué forma tiene la órbita exacta en el plano $(x,v)$? ¿Qué pasa con la
   energía exacta a lo largo del tiempo?
   La orvita excata seria la de una circunsferencia, mientras la energia deberia ser constante.
2. Escriban a mano un paso de Euler explícito para $x''=-x$. ¿En qué factor
   cambia $x^2+v^2$ en ese paso? ¿Y en un paso de Euler implícito?


Para Euler explícito:

x_(n+1) = x_n + dt·v_n

v_(n+1) = v_n - dt·x_n

Entonces:

x_(n+1)² + v_(n+1)²
= (x_n + dt·v_n)² + (v_n - dt·x_n)²
= x_n² + 2dt·x_nv_n + dt²v_n² + v_n² - 2dt·x_nv_n + dt²x_n²

Los términos cruzados se cancelan y queda:

x_(n+1)² + v_(n+1)² = (1 + dt²)(x_n² + v_n²)

Por lo tanto, en Euler explícito x² + v² aumenta en cada paso por un factor (1 + dt²).

Para Euler implícito:

x_(n+1) = x_n + dt·v_(n+1)

v_(n+1) = v_n - dt·x_(n+1)

Al resolver estas ecuaciones se obtiene:

x_(n+1)² + v_(n+1)² = [1/(1 + dt²)](x_n² + v_n²)

Por lo tanto, en Euler implícito x² + v² disminuye en cada paso por un factor 1/(1 + dt²).




3. Con esa cuenta, ¿qué esperan que pase con la amplitud y con el período de
   la oscilación después de diez períodos con cada método? ¿Qué verían en el
   plano $(x,v)$?

Con Euler explícito, la amplitud aumenta con el tiempo porque el método agrega energía. En el plano (x,v), la trayectoria se va abriendo hacia afuera en forma de espiral.

Con Euler implícito, la amplitud disminuye porque el método pierde energía. En el plano (x,v), la trayectoria se va cerrando hacia el centro.


4. Si `dt` se reduce a la mitad, ¿qué esperan que ocurra con el error a tiempo
   final fijo?

   Si dt se reduce a la mitad, esperamos que el error a tiempo final fijo se reduzca aproximadamente a la mitad, ya que el método de Euler es de primer orden.
error por paso ~ dt²
número de pasos ~ 1/dt
error acumulado ~ dt² · 1/dt = dt

5. Para el resorte, ¿cuántas iteraciones de Newton esperan que haga falta en
   cada paso implícito?
Como el problema del resorte es lineal, esperamos que el método de Newton converja en una sola iteración en cada paso implícito.


## Criterio de aceptación

Propongan un criterio para decidir si un valor de `dt` es aceptable para
simular cien períodos. ¿Qué cantidad medirían y qué tolerancia le pedirían?

Consideraría aceptable un valor de dt si, después de simular 100 períodos, el error relativo de la energía permanece por debajo del 1 %:
|E_final - E_inicial| / E_inicial < 0.01
De esta forma verificamos que la simulación no gane ni pierda demasiada energía con el tiempo.