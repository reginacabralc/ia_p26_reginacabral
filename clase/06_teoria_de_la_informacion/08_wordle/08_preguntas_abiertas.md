---
title: "Preguntas Abiertas y Direcciones Creativas"
---

# Preguntas Abiertas y Direcciones Creativas

Las estrategias anteriores cubren un espectro desde lo trivial (azar) hasta lo sofisticado (look-ahead). Pero hay muchas direcciones que no exploramos — y que podrían superar lo que vimos. Aquí hay ideas para investigar.

## 1. Funciones de agregación diferentes

Todas nuestras estrategias usan el **valor esperado** para agregar sobre los posibles feedbacks. Pero el valor esperado no es la única opción:

- **Min-max (peor caso)**: ¿Cuál es el guess que minimiza el *peor* resultado posible? Esto da robustez contra el peor escenario.
- **Mediana**: menos sensible a outliers que la media.
- **Media penalizada por varianza**: $\mathbb{E}[\text{score}] + \lambda \cdot \text{Var}[\text{score}]$. Prefiere resultados consistentes sobre resultados con alta varianza.

¿Cuándo convendría cada una? ¿Cambia la respuesta según el número de intentos restantes?

## 2. Intentos no-palabra

¿Qué pasa si permitimos adivinar secuencias de letras que **no son palabras reales**, puramente para recopilar información?

Esto desacopla completamente exploración de explotación: un intento no-palabra nunca puede ganar, pero podría dar más información que cualquier palabra real.

Preguntas de diseño:
- ¿Cómo elegir la secuencia óptima de letras para maximizar información?
- ¿Cuándo es mejor una "sonda" no-palabra que el mejor guess real?
- ¿Cuántas sondas vale la pena hacer antes de empezar a adivinar?

El framework del torneo soporta esto con `config.allow_non_words=True` (ver [repositorio del torneo](https://github.com/sonder-art/rtorneo_wordle_p26)).

## 3. Look-ahead más profundo

Si 2 pasos mejoran sobre 1, ¿3 pasos mejoran sobre 2? ¿4 sobre 3?

- ¿Cuál es la mejora marginal por cada paso adicional?
- ¿Se puede hacer poda (alpha-beta) para reducir el costo?
- ¿Existe un límite teórico a cuánto puede mejorar el look-ahead?

## 4. Estrategias híbridas

Una idea natural: usar entropía al inicio del juego (mucha incertidumbre, exploración es valiosa) y score esperado al final (poca incertidumbre, explotación domina).

- ¿Cuál es la regla de switching óptima?
- ¿Depende del número de intentos restantes, de los bits restantes, o de ambos?
- ¿Se puede aprender la regla automáticamente?

## 5. Medidas de información alternativas

Shannon no es la única entropía:

- **Entropía de Rényi**: $H_\alpha(X) = \frac{1}{1-\alpha} \log_2 \sum_x p(x)^\alpha$. El parámetro $\alpha$ controla la sensibilidad a eventos raros ($\alpha < 1$) o frecuentes ($\alpha > 1$). ¿Existe un $\alpha$ óptimo para Wordle?
- **Entropía de Tsallis**: no aditiva, usada en sistemas con correlaciones de largo alcance.
- **Medidas ad-hoc**: por ejemplo, "número de particiones con más de $k$ elementos" o "tamaño del grupo más grande".

## 6. Wordle adversarial

¿Qué pasa si la palabra secreta no se elige al inicio, sino que un **adversario** la elige *después* de ver tu guess, eligiendo siempre el feedback que te deja en la peor situación (mientras sea consistente con feedbacks anteriores)?

- Esto convierte el juego en un **juego de suma cero de dos jugadores**.
- La estrategia óptima es **minimax**.
- ¿Cuántos intentos necesitas en el peor caso bajo juego adversarial?

## 7. Longitud de palabra variable

Las estrategias que funcionan bien con $L = 5$, ¿se transfieren a $L = 4$? ¿A $L = 7$?

- ¿Qué estrategias son más **robustas** al cambio de longitud?
- ¿Cómo cambia el espacio de feedback? (Con $L = 5$ hay $3^5 = 243$ patrones posibles; con $L = 7$ hay $3^7 = 2187$)
- ¿La importancia relativa de las estrategias cambia con $L$?

## 8. Tu propia idea

Las estrategias presentadas son un punto de partida. Cualquier idea original que puedas formular, implementar y evaluar contra las existentes es bienvenida.

Preguntas guía para una buena propuesta:
- ¿Qué suposición de las estrategias existentes estás relajando o cambiando?
- ¿Cómo medirás si tu idea funciona mejor?
- ¿En qué situaciones esperas que sea mejor (y en cuáles peor)?

---

**Volver:** [← Índice del proyecto](00_index.md)
