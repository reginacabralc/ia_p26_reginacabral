---
title: "Teoría de la Información: Bits, Entropía y Aprendizaje"
---



:::exam{id="EX-03" title="Segundo parcial: Probabilidad" date="2026-02-11" points="10" duration="20 minutos"}
Examen de probabilidad, estadistica y fat-tails. Se preguntara acerta de probabilidad, estadistica y fat-tails.
:::

:::exam{id="EX-04" title="Parcial de Teoria de la Informacion" date="2026-03-02" points="10" duration="20 minutos"}

Examen sobre teoria de la inforamcion, incluyendo bits, entropia (interpretacion y propiedades), algoritmo de Huffman, y filosofia. Todo lo que hemos visto en el modulo en clase (no lo que no vimos)
:::
# Teoría de la Información: Bits, Entropía y Aprendizaje

¿Qué significa **“información”** cuando queremos razonar, comunicar, aprender y (sí) *adivinar una palabra* o *crackear una contraseña*?

Este módulo va **despacio** y construye todo paso a paso: empezamos con intuiciones honestas (con sus límites), subimos a definiciones formales, y cerramos con un ejercicio acumulativo estilo **Wordle/Fallout hacking** usando **priors** y **entropía**.

## Contenido

| Sección | Tema | Idea clave |
|:------:|------|-----------|
| 6.1 | [Introducción](01_intro.md) | Información = reducción de incertidumbre (con cuidado) |
| 6.2 | [Bits y preguntas](02_bits_y_preguntas.md) | “¿Cuántas preguntas sí/no necesito?” |
| 6.3 | [Sorpresa y auto-información](03_sorpresa_y_auto_informacion.md) | $I(x)=-\log_2 p(x)$ como “sorpresa” cuantificada |
| 6.4 | [Entropía (Shannon y Jaynes)](04_entropia.md) | Entropía = sorpresa promedio; Jaynes: “información faltante” |
| 6.5 | [Códigos y compresión](05_codigos_y_compresion.md) | Códigos cortos para cosas frecuentes; límite ligado a $H$ |
| 6.6 | [Cross-entropy y KL (puente a ML)](06_cross_entropy_y_kl.md) | Log-loss, “apostar mal” y el costo de un modelo |
| 6.7 | [Información mutua y ML](07_informacion_mutua_y_ml.md) | “Cuánto me dice $Y$ sobre $X$” y por qué importa |
| Lab | [Laboratorio en Python](lab_informacion.py) | Generar imágenes/experimentos para clase |
| Ejercicios | [Capstone Wordle/Password](ejercicios/00_index.md) | Culminación acumulativa con priors + entropía |
| Proyecto | [Proyecto Wordle](08_wordle/00_index.md) | Aplica todo: diseña y compara estrategias ([repo del torneo](https://github.com/sonder-art/rtorneo_wordle_p26)) |

## Cómo correr el lab (para imágenes)

```bash
cd clase/06_teoria_de_la_informacion
python lab_informacion.py
```

Esto genera imágenes en `images/` que se usan en las notas.

## Objetivos de aprendizaje

Al terminar este módulo podrás:

1. Explicar qué es un **bit** como unidad de distinción y por qué aparece el $\log_2$.
2. Definir **auto-información** $I(x)$ y conectarla con probabilidad.
3. Definir y calcular **entropía** $H(X)$ y entender qué significa (y qué no significa).
4. Describir la perspectiva de **Jaynes**: entropía como medida de información faltante dado un contexto $I$.
5. Relacionar entropía con **compresión** y con el diseño de códigos.
6. Conectar **cross-entropy** y **KL** con pérdidas típicas de ML (log-loss).
7. Usar **ganancia esperada de información** para elegir buenas “preguntas” (y buenos guesses) en un juego tipo Wordle/hacking.

## Hilo conductor del módulo (un ejemplo que se acumula)

Durante el módulo volveremos varias veces a la misma historia, cada vez con más precisión:

> Una “caja negra” elige una palabra secreta en español (de 5 letras, sin acentos) según una distribución $p(\text{palabra}\mid I)$.  
> Tú haces intentos. A veces recibes feedback (tipo Wordle). A veces no (tipo password guessing).  
> ¿Cómo cuantificas progreso? ¿Cómo eliges el siguiente intento?

## Nota sobre analogías (importante)

Usaremos analogías (pistas, preguntas, compresión, “sorpresa”). Funcionan **bien** para construir intuición, pero **no son definiciones**. En cada analogía vamos a decir explícitamente:

- qué parte captura bien, y
- qué parte es incompleta o puede confundir.

---

**Siguiente:** [Introducción →](01_intro.md)

