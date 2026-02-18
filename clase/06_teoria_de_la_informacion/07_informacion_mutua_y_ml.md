---
title: "Información mutua: qué tanto me dice Y sobre X"
---

# Información mutua: qué tanto me dice Y sobre X

Hasta ahora medimos incertidumbre sobre una variable $X$.

Ahora queremos medir algo relacional:

> ¿Cuánto me dice $Y$ sobre $X$?

Ese “cuánto” es **información mutua**.

---

## Entropía condicional (la pieza que faltaba)

La entropía condicional es:

$$
H(X\mid Y, I) = \mathbb{E}_{y\sim p}\left[H(X\mid Y=y, I)\right]
$$

Lectura:

> Es la incertidumbre promedio que queda sobre $X$ después de observar $Y$.

---

## Definición: información mutua

La información mutua se define como:

$$
I(X;Y\mid I) = H(X\mid I) - H(X\mid Y, I)
$$

Lectura UX:

> Es cuántos bits (en promedio) reduce $Y$ tu incertidumbre sobre $X$.

### Propiedades importantes (sin prueba)

- $I(X;Y)\ge 0$.
- $I(X;Y)=0$ si $X$ y $Y$ son independientes (saber $Y$ no cambia nada).
- Es simétrica: $I(X;Y)=I(Y;X)$.

---

## Ejemplo acumulativo: “feedback” como variable aleatoria

En Wordle:

- $X$ = palabra secreta,
- $G$ = tu guess (lo eliges),
- $F$ = feedback que te regresa el juego.

Si fijas un guess $G=g$, entonces $F$ se vuelve una función de $X$ (con reglas del juego).

La cantidad relevante para “elegir un buen guess” es:

$$
I(X;F\mid G=g, I)
=
H(X\mid I) - H(X\mid F, G=g, I)
$$

Esto es la misma idea que escribimos como ganancia esperada de información:

$$
\text{IG}(g) = H(X\mid I) - \mathbb{E}_{F}[H(X\mid F,I)]
$$

Solo que ahora lo vemos como un caso particular de información mutua.

---

## ¿Dónde aparece en ML?

### 1) Selección de features (intuición)

Si una feature $Y$ tiene alta $I(X;Y)$, entonces:

- observar $Y$ reduce mucho la incertidumbre sobre $X$,
- por lo tanto $Y$ “contiene información” relevante sobre la etiqueta $X$.

Esto inspira criterios como:

- **ganancia de información** en árboles de decisión (ID3/C4.5),
- variantes basadas en entropía/MI para ranking de variables.

### 2) LLMs: entropía promedio y perplejidad

Si un modelo de lenguaje asigna $q(\text{token}_t\mid \text{contexto})$,
la pérdida típica es:

$$
-\log q(\text{token}_t\mid \text{contexto})
$$

Promediada en el tiempo y en datos reales (aprox $p$), esto es cross-entropy.

La **perplejidad** es (en base $e$) algo como:

$$
\text{ppl} = \exp\left(\mathbb{E}[-\log q]\right)
$$

Lectura:

> perplejidad = “número efectivo de opciones” que el modelo siente que tiene en promedio.

---

## Analogía honesta: “preguntas que valen la pena”

Analogía:

> Si tu objetivo es identificar $X$, quieres observar variables $Y$ que en promedio eliminen muchas posibilidades.

- **Qué captura bien**: MI como reducción esperada de incertidumbre.
- **Qué es incompleto**: no incluye costo de medir $Y$, ni restricciones computacionales, ni sesgo del modelo.

---

:::exercise{title="MI como reducción de incertidumbre (idea cualitativa)" difficulty="2"}

Considera $X$ = “palabra secreta” y dos posibles pistas:

- $Y_1$: “la primera letra de la palabra”
- $Y_2$: “si la palabra contiene la letra e”

1. Sin calcular números: ¿cuál crees que suele dar más información mutua con $X$? ¿depende del idioma/dataset?
2. ¿Cómo cambiaría tu respuesta si el prior $p(X)$ está muy concentrado (pocas palabras muy probables)?

:::

---

## Cierre del módulo (conceptual)

Ya tenemos un toolkit completo para el capstone:

- $I(x)=-\log p(x)$: sorpresa de una hipótesis específica.
- $H(X)$: incertidumbre promedio / bits inevitables.
- $H(p,q)$ y $D_{KL}$: costo por modelar mal.
- $I(X;Y)$: utilidad esperada de observar una pista.

Lo siguiente es convertir esto en un sistema tangible:

1) elegir datasets (priors realistas),  
2) generar imágenes que expliquen,  
3) implementar un solver Wordle/password.

---

**Siguiente:** [Laboratorio en Python →](lab_informacion.py)  
**Volver:** [← Índice](00_index.md)

