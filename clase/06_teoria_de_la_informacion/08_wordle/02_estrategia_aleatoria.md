---
title: "Estrategia 1: Adivinar al Azar"
---

# Estrategia 1: Adivinar al Azar

## La estrategia más simple

La estrategia aleatoria es el baseline absoluto: en cada turno, elige **uniformemente al azar** entre los candidatos restantes. No hay inteligencia, no hay análisis — pura suerte.

```
Para cada turno:
  1. Filtra los candidatos consistentes con el historial de feedback
  2. Elige uno al azar (uniforme)
```

## ¿Por qué es útil como baseline?

Toda estrategia debería superar al azar. Si tu estrategia sofisticada no le gana consistentemente a esta, algo está mal.

Además, la estrategia aleatoria nos permite aislar el efecto del **mecanismo de feedback** del efecto de la **inteligencia del jugador**: incluso sin elegir bien, el hecho de que el feedback filtra candidatos te acerca a la respuesta.

## Análisis de rendimiento esperado

Con $N$ candidatos iniciales y feedback perfecto (que siempre reduce el espacio), el número esperado de intentos depende de qué tan rápido se contrae $\mathcal{C}_t$.

En el peor caso (sin feedback), necesitarías $\sim N/2$ intentos en promedio. Pero con feedback de Wordle, incluso un jugador aleatorio se beneficia: cada intento revela información sobre letras correctas e incorrectas, reduciendo el pool de candidatos.

Sin embargo, la reducción es **inconsistente**: a veces tienes suerte y el feedback elimina muchos candidatos, a veces casi ninguno. La varianza es alta.

## La pregunta clave

El feedback proporciona información en cada turno. La estrategia aleatoria no intenta **maximizar** esa información — simplemente la recibe pasivamente. La pregunta que motiva las siguientes estrategias es:

> ¿Podemos elegir nuestros intentos de forma que **maximicen** la información que el feedback nos da?

---

**Siguiente:** [Máxima probabilidad →](03_maxima_probabilidad.md)

**Volver:** [← Índice del proyecto](00_index.md)
