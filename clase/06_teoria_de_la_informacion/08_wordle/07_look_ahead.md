---
title: "Estrategia 6: Mirar al Futuro (Look-Ahead)"
---

# Estrategia 6: Mirar al Futuro (Look-Ahead)

## El problema de la miopía

Todas las estrategias anteriores son **greedy**: evalúan cada guess solo por su efecto inmediato. Pero un guess puede verse bien ahora y dejarte con un conjunto de candidatos difícil de distinguir en el siguiente turno.

## La idea de look-ahead

En lugar de evaluar un guess solo por el turno actual, simula también el **siguiente turno**:

1. Para cada guess $g_1$ (primer paso):
   - Simula todos los posibles feedbacks $f_1$
   - Para cada feedback, calcula los candidatos restantes $\mathcal{C}_1$
2. Para cada estado $\mathcal{C}_1$ resultante (segundo paso):
   - Encuentra el mejor guess $g_2^*$ según la métrica de score esperado
   - Calcula el score esperado de $g_2^*$
3. Combina: el score de $g_1$ es el costo del primer paso más el score esperado del segundo paso

$$\text{Score}_2(g_1) = \sum_{f_1} p(f_1 \mid g_1) \left[ \mathbb{1}[f_1 = \text{win}] + \mathbb{1}[f_1 \neq \text{win}] \cdot (1 + \text{Score}_1^*(g_1, f_1)) \right]$$

donde $\text{Score}_1^*$ es el mejor score del siguiente paso dado el estado resultante.

## Pseudocódigo conceptual

```
Para cada candidato g₁ en C:
    score_total = 0
    Para cada patrón f₁ posible:
        p₁ = proporción de candidatos que producen f₁
        Si f₁ = todo verde:
            score_total += p₁ × 1  # ganamos en este turno
        Sino:
            C₁ = filtrar candidatos por (g₁, f₁)
            mejor_score_paso2 = infinito
            Para cada candidato g₂ en C₁:
                score₂ = evaluar g₂ con estrategia de score esperado en C₁
                mejor_score_paso2 = min(mejor_score_paso2, score₂)
            score_total += p₁ × (1 + mejor_score_paso2)
    Score₂(g₁) = score_total
Elegir g₁ con menor Score₂(g₁)
```

## Costo computacional

La complejidad crece exponencialmente con la profundidad:
- 1 paso: $O(|\mathcal{C}|^2)$
- 2 pasos: $O(|\mathcal{C}|^3)$ en el peor caso (cada estado del paso 1 requiere evaluar todos los guesses del paso 2)

Con ~13,000 palabras (Wordle inglés), el paso 2 es costoso pero tratable con optimizaciones (filtrar guesses candidatos, paralelizar). Un paso 3 sería prohibitivo sin poda agresiva.

## ¿Por qué 2 pasos?

Hay un rendimiento marginal decreciente:
- Paso 0 (sin look-ahead) → paso 1: mejora grande
- Paso 1 → paso 2: mejora moderada
- Paso 2 → paso 3: mejora mínima, costo enorme

Dos pasos es el **sweet spot** entre mejora y costo.

## Rendimiento

En Wordle inglés con look-ahead de 2 pasos: promedio de ~3.43 intentos. El opener matemáticamente óptimo resulta ser CRANE.

## Conexión con teoría de juegos

Esto es exactamente **búsqueda expectimax** con profundidad 2:
- El jugador elige un guess (nodo **max**: minimizar score)
- La "naturaleza" revela un feedback (nodo **chance**: ponderado por probabilidad)
- El jugador elige otro guess (nodo **max**)

Es la misma estructura que aparece en juegos como ajedrez y backgammon, limitada a profundidad 2 por tratabilidad.

---

**Siguiente:** [Preguntas abiertas →](08_preguntas_abiertas.md)

**Volver:** [← Índice del proyecto](00_index.md)
