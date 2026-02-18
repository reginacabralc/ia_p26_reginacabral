---
title: "Estrategia 3: Maximizar Entropía (Ingenua)"
---

# Estrategia 3: Maximizar Entropía (Ingenua)

## La idea central

Elige el intento que produce la **distribución más plana** de patrones de feedback. Si cada patrón posible es igualmente probable, cada resultado te dice lo máximo posible.

La entropía formaliza exactamente esto.

## Formulación

Sea $\mathcal{C}$ el conjunto actual de candidatos. Para un guess $g$, define la distribución de patrones:

$$p(f \mid g) = \frac{|\{w \in \mathcal{C} : f(w, g) = f\}|}{|\mathcal{C}|}$$

La entropía del feedback dado $g$:

$$H(F \mid g) = -\sum_{f} p(f \mid g) \log_2 p(f \mid g)$$

**Estrategia**: elegir $g^* = \arg\max_g H(F \mid g)$

## ¿Por qué funciona?

Esto es equivalente a maximizar la **ganancia esperada de información**:

$$\text{IG}(g) = H(X) - \mathbb{E}_f[H(X \mid f, g)]$$

donde $H(X) = \log_2 |\mathcal{C}|$ (entropía uniforme sobre candidatos). Maximizar $H(F \mid g)$ es equivalente a minimizar $\mathbb{E}_f[H(X \mid f, g)]$: queremos que **después** de observar el feedback, la incertidumbre restante sea mínima.

## Pseudocódigo conceptual

```
Para cada candidato g en C:
    Para cada secreto posible w en C:
        Calcular feedback f(w, g)
    Agrupar los secretos por patrón de feedback
    Calcular H(F|g) = entropía de la distribución de patrones
Elegir g con mayor H(F|g)
```

La complejidad es $O(|\mathcal{C}|^2)$ por turno (cada guess se simula contra cada secreto posible).

## Limitaciones

1. **Trata todas las palabras como igualmente probables.** Si "canto" y "zueco" están en el vocabulario, esta estrategia les da el mismo peso. Pero en la realidad, "canto" es mucho más probable como respuesta.

2. **Es greedy de un paso.** Solo optimiza la información del turno actual. No considera cómo el resultado afecta las opciones del siguiente turno.

3. **No distingue entre explorar y ganar.** Puede elegir un guess que da mucha información pero que tiene 0% de probabilidad de ser la respuesta. Cerca del final del juego, esto desperdicia un intento.

## Rendimiento

En Wordle inglés con esta estrategia: promedio de ~4.12 intentos. El opener óptimo (por entropía pura) es TARES.

Es un salto enorme respecto al azar, pero hay espacio para mejorar.

---

**Siguiente:** [Entropía ponderada →](05_entropia_ponderada.md)

**Volver:** [← Índice del proyecto](00_index.md)
