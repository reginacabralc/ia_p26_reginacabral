---
title: "Sorpresa y auto-información: medir lo inesperado"
---

# Sorpresa y auto-información: medir lo inesperado

En la sección anterior llegamos a una idea:

$$
I(p) = -\log_2 p
$$

Ahora vamos a decir con precisión **qué significa** y **qué objeto matemático es**.

---

## Un modelo mínimo (con contexto explícito)

Tenemos una variable aleatoria $X$ que puede tomar valores $x$ (por ejemplo, palabras de una lista).

- $X$: “la palabra secreta”
- $x$: una palabra concreta, por ejemplo `"canto"`
- $I$: información de fondo (“estamos en español”, “5 letras”, “sin acentos”, “lista válida”, etc.)

Entonces describimos nuestras creencias con:

$$
p(x\mid I)
$$

Esta $p(\cdot)$ no tiene que ser “la verdad metafísica”: es el **modelo** que vamos a usar para razonar y tomar decisiones.

---

## Definición: auto-información

La **auto-información** (también llamada “sorpresa”) de observar $X=x$ es:

$$
I(x) \;=\; -\log_2 p(x\mid I)
$$

- Se mide en **bits** (por usar $\log_2$).
- Depende del **contexto** $I$ porque la probabilidad depende de $I$.

![Sorpresa: $I(p)=-\log_2(p)$]({{ '/06_teoria_de_la_informacion/images/surprisal_vs_p_bits.png' | url }})

*La curva deja claro el comportamiento clave: cuando $p$ es grande, $I(p)$ es pequeño; cuando $p$ es muy pequeño, $I(p)$ crece rápido. No es “utilidad para una tarea”: es sorpresa relativa al prior.*

### Lectura en palabras

> Si algo era muy probable bajo tu modelo $p(\cdot\mid I)$, observarlo tiene **poca sorpresa**: ya lo esperabas.  
> Si algo era muy improbable, observarlo tiene **mucha sorpresa**: tu modelo casi lo descartaba.

Otra forma (menos ambigua con el español coloquial) de decir lo mismo es:

> Un resultado probable requiere **pocos bits para especificarse** bajo el prior.  
> Un resultado raro requiere **muchos bits**.

### No confundir (esto es la fuente de casi toda la confusión)

Hay dos ideas distintas que suenan parecidas:

1) **Después de observar $X=x$, ya no hay incertidumbre sobre $X$**  
   Si tu pregunta era “¿qué valor tomó $X$?”, al observarlo ya lo sabes con certeza. En ese sentido, la incertidumbre sobre $X$ colapsa a 0.

2) **La auto-información $I(x)$ mide otra cosa**  
   Mide *cuánto “costaba” (en bits) señalar ese resultado* **antes** de verlo, dada tu distribución $p(\cdot\mid I)$.  
   Por eso depende del prior: si ya estabas casi seguro de $x$, especificarlo es “barato”; si era muy raro, es “caro”.

La conexión con el resto del módulo es operacional:

- en [Códigos y compresión](05_codigos_y_compresion.md), $-\log p(x)$ aparece como longitud ideal de un código para describir $x$;
- en [Entropía](04_entropia.md), el “promedio” de ese costo es $H(X\mid I)$.
- si quieres una motivación más completa de *por qué* usamos esta definición y por qué no coincide con el uso coloquial, vuelve a la sección “Por qué hablamos así (y por qué aparece $-\log p$)” en [Introducción](01_intro.md).

---

## Ejemplo acumulativo (con números, no con “moneda/dado”)

Supón que (dado tu contexto $I$) solo consideras estas 3 palabras como candidatas:

| palabra $x$ | $p(x\mid I)$ |
|---|---:|
| `"canto"` | 0.50 |
| `"costa"` | 0.25 |
| `"zueco"` | 0.25 |

Entonces:

- $I(\text{"canto"}) = -\log_2(0.50)=1$ bit  
- $I(\text{"costa"}) = -\log_2(0.25)=2$ bits  
- $I(\text{"zueco"}) = -\log_2(0.25)=2$ bits

Interpretación:

> Si la palabra es `"canto"`, no aprendiste tanto: ya era la más plausible.  
> Si sale `"costa"` o `"zueco"`, eso te “sorprende” más: necesitabas el doble de bits para “señalarla”.

### Nota de honestidad (limitación)

Este ejemplo “se siente” simple porque el conjunto es pequeño. La idea no depende del tamaño: en el capstone usaremos miles de palabras.

---

## Por qué $-\log$ es la forma correcta (y no otra)

Aquí hay una versión corta, pero formal-en-espíritu, del argumento.

Queremos medir información de un evento con probabilidad $p$.

1) **Monotonía**: si algo es menos probable, debería dar más información.  
2) **Aditividad para independencia**: si dos cosas independientes pasan, la información total debería sumar.

Si $A$ y $B$ son independientes, entonces $p(AB)=p(A)p(B)$.  
La aditividad pide:

$$
I(p(A)p(B)) = I(p(A)) + I(p(B))
$$

La solución estándar (bajo supuestos suaves) es:

$$
I(p) = k\cdot(-\log p)
$$

Y elegir base 2 fija unidades: **bits**.

---

## Cómo se conecta con “hacer un guess”

Si tú propones un guess $g$ en Wordle, no estás observando directamente $X$. Estás observando un **feedback** $F$ (patrón verde/amarillo/gris).

En general:

- antes del guess tienes $p(x\mid I)$,
- después de ver feedback $f$, actualizas a $p(x\mid f,I)$.

La teoría de la información nos va a dar una forma de medir:

> “En promedio, ¿cuántos bits reduce mi **incertidumbre ex ante** (mi entropía) si juego $g$?”

Ese “en promedio” es exactamente el paso hacia entropía.

---

:::exercise{title="Sorpresa y escala (bits) con un prior sesgado" difficulty="2"}

Una lista de 5 palabras tiene este prior:

- $p(w_1)=0.60$
- $p(w_2)=0.20$
- $p(w_3)=0.10$
- $p(w_4)=0.05$
- $p(w_5)=0.05$

1. Calcula $I(w_i)=-\log_2 p(w_i)$ (aproxima a 2 decimales).
2. Ordena las palabras de “menos sorpresa” a “más sorpresa”.
3. Interpreta: ¿cuál palabra se parece más a “password humano típico” y cuál a uno raro, bajo este prior?

:::

---

**Siguiente:** [Entropía (Shannon y Jaynes) →](04_entropia.md)  
**Volver:** [← Índice](00_index.md)

