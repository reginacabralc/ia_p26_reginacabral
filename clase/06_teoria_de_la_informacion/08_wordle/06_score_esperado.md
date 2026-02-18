---
title: "Estrategia 5: Minimizar el Puntaje Esperado"
---

# Estrategia 5: Minimizar el Puntaje Esperado

## Cambio de objetivo

Las estrategias anteriores maximizan **información por turno**. Pero el objetivo real del juego es **minimizar el número total de intentos**. Estos dos objetivos no siempre coinciden.

## El problema del final del juego

Imagina que quedan 3 candidatos y te queda 1 intento. La entropía dice: "elige el guess que mejor distinga entre los 3". Pero si uno de los 3 tiene probabilidad 60%, lo correcto es **apostar por ese** — maximizar tu probabilidad de ganar, no tu información.

La entropía es una herramienta de **exploración**. Cerca del final, la **explotación** es más valiosa. Necesitamos una función objetivo que balancee ambas.

## La función de score

Para cada guess $g$, definimos:

$$\text{Score}(g) = p(\text{win} \mid g) \times 1 + (1 - p(\text{win} \mid g)) \times (1 + \hat{f}(\text{bits restantes}))$$

donde:
- $p(\text{win} \mid g) = p(g = s)$: probabilidad de que $g$ sea la respuesta
- $\hat{f}(b)$: estimación de cuántos intentos más necesitarás si te quedan $b$ bits de incertidumbre

El primer término es el "costo de ganar ahora" (1 intento). El segundo es el "costo de no ganar" (1 intento gastado + los que faltan).

## ¿De dónde sale $\hat{f}$?

De una **regresión empírica**. El proceso:

1. Corre la estrategia de entropía ponderada en muchas partidas
2. En cada turno, registra: (bits de incertidumbre restante, intentos que faltaron para ganar)
3. Ajusta una curva $\hat{f}(b)$ a estos datos (regresión lineal o polinomial)

$\hat{f}$ es un **traductor empírico**: "cuando me quedan $b$ bits de incertidumbre, históricamente necesito $\hat{f}(b)$ intentos más".

## Pseudocódigo conceptual

```
Precalcular f̂(b) mediante regresión en datos históricos

Para cada candidato g en C:
    p_win = p(g)  # probabilidad de que g sea la respuesta
    Si g es la respuesta: costo = 1

    Para cada patrón f posible (si g no es la respuesta):
        Calcular candidatos restantes C' y sus bits H(C')
        Costo esperado del subproblema ≈ 1 + f̂(H(C'))

    Score(g) = p_win × 1 + (1 - p_win) × costo esperado
Elegir g con menor Score(g)
```

## ¿Por qué funciona?

Porque combina los dos regímenes:

- **Cuando hay mucha incertidumbre** (bits altos): $p(\text{win})$ es baja para todos los guesses, así que el término dominante es $\hat{f}(\text{bits})$. Esto se reduce a minimizar bits restantes ≈ maximizar entropía.
- **Cuando hay poca incertidumbre** (pocos candidatos): $p(\text{win})$ puede ser significativa, y el score favorece apostar directamente por la respuesta.

La transición es suave y automática — no hay un "switch" manual entre explorar y explotar.

## Rendimiento

En Wordle inglés: promedio de ~3.6 intentos. Una mejora significativa sobre la entropía pura (~4.12).

## Conexión con programación dinámica

Este score es una aproximación de la **ecuación de Bellman**: el costo óptimo desde un estado es el mínimo sobre acciones del costo inmediato más el costo futuro esperado. Aquí $\hat{f}$ aproxima el valor futuro sin resolver el problema exacto (que sería intratable).

---

**Siguiente:** [Look-ahead →](07_look_ahead.md)

**Volver:** [← Índice del proyecto](00_index.md)
