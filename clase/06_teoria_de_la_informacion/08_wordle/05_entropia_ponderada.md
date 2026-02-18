---
title: "Estrategia 4: Entropía con Frecuencia de Palabras"
---

# Estrategia 4: Entropía con Frecuencia de Palabras

## El problema de la entropía ingenua

La estrategia anterior trata "aalii" y "canto" como igualmente probables. Pero si Wordle elige de un vocabulario de palabras comunes, las frecuencias importan — y mucho.

El problema no es solo de accuracy: la frecuencia cruda tampoco sirve directamente. "que" puede tener frecuencia 1000x mayor que "brazo", pero ambas son palabras "comunes" que Wordle podría usar. Lo que necesitamos es una forma de distinguir entre **plausible** e **implausible**, no entre **frecuente** y **muy frecuente**.

## La solución sigmoide

Una función **sigmoide** aplicada al logaritmo de la frecuencia crea un corte suave:

$$\sigma(w) = \frac{1}{1 + e^{-k(\log f(w) - \mu)}}$$

donde $f(w)$ es la frecuencia de la palabra $w$, y $k, \mu$ son parámetros que controlan la pendiente y el punto de corte.

El efecto:
- Palabras muy comunes → $\sigma \approx 1$ (plausibles)
- Palabras moderadamente comunes → $\sigma \approx 1$ (también plausibles)
- Palabras verdaderamente oscuras → $\sigma \approx 0$ (implausibles)

Esto crea una **meseta** en lugar de un pico: todas las palabras "razonables" tienen peso similar, y solo las realmente raras son penalizadas.

## ¿Por qué sigmoide y no otra cosa?

La sigmoide comprime el rango dinámico. Alternativas:
- **Frecuencia cruda**: sesga masivamente hacia "el", "de", "que" — inútil para Wordle
- **Corte duro** (top-K): pierde gradualidad; ¿dónde pones el corte?
- **Raíz o log**: reduce la dispersión pero no la elimina

La sigmoide preserva el **orden** pero convierte una distribución de cola pesada en una casi-uniforme sobre palabras plausibles. Exactamente lo que queremos.

## Entropía ponderada

Con los pesos $\sigma(w)$, definimos probabilidades normalizadas:

$$p(w) = \frac{\sigma(w)}{\sum_{w' \in \mathcal{C}} \sigma(w')}$$

Ahora los patrones de feedback se ponderan por **masa de probabilidad**, no por conteo:

$$p(f \mid g) = \sum_{w : f(w,g) = f} p(w)$$

Y la entropía ponderada:

$$H_\sigma(F \mid g) = -\sum_f p(f \mid g) \log_2 p(f \mid g)$$

## Pseudocódigo conceptual

```
Precalcular σ(w) para cada palabra en el vocabulario

Para cada candidato g en C:
    Para cada secreto posible w en C:
        Calcular feedback f(w, g)
    Agrupar los secretos por patrón, sumando p(w) por grupo
    Calcular H_σ(F|g) = entropía de la distribución ponderada
Elegir g con mayor H_σ(F|g)
```

## ¿Cuándo importa más?

Cuando la lista de candidatos es grande y tiene **cola pesada** de palabras raras. En listas curadas (solo palabras comunes), la diferencia con la entropía ingenua es pequeña. Pero en vocabularios grandes extraídos de corpus, la mejora es significativa.

---

**Siguiente:** [Score esperado →](06_score_esperado.md)

**Volver:** [← Índice del proyecto](00_index.md)
