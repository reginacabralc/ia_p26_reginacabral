---
title: "Teoría de la Decisión"
---

# Teoría de la Decisión

> *"The oracle sees, but cannot choose."*
> — Dune Messiah

:::homework{id="hw-grafos" title="Grafos" due="2026-02-25" points="20"}
Ver el curso de grafos de datacamp y subir en pull reques similar a los anteriores y en canvas la evidencia. El curso es: https://app.datacamp.com/learn/courses/intermediate-network-analysis-in-python 

Solo tienen que realizar las primeras dos secciones, 10 puntos extra en tareas si terminan el curso.
:::

El módulo anterior mostró cómo predecir — estimar $P(Y \mid X)$, cuantificar incertidumbre, elegir el modelo correcto. Pero predecir no es decidir. Un modelo perfecto de pronóstico del clima no te dice si llevar paraguas. Una predicción de ventas no te dice cuánto producir. El oráculo ve, pero no elige.

Este módulo introduce **teoría de la decisión**: el marco formal para agentes que deben **actuar** bajo incertidumbre. Combina probabilidad (mod 05), optimización (mod 07) y predicción (mod 08) en una sola fórmula:

$$a^{∗} = \arg\max_{a \in A} \sum_{s \in S} P(s) \cdot U(o(a, s))$$

## Contenido

| Sección | Tema | Idea clave |
|:------:|------|-----------|
| 9.1 | [Anatomía de un problema de decisión](01_anatomia_decision.md) | Estados, acciones, utilidades, tres regímenes |
| 9.2 | [Utilidad y preferencias racionales](02_utilidad_preferencias.md) | Axiomas vNM, funciones de utilidad, riesgo |
| 9.3 | [Decidir bajo incertidumbre](03_decidir_bajo_incertidumbre.md) | MEU, árboles de decisión, valor de la información |
| 9.4 | [Optimización estocástica](04_optimizacion_estocastica.md) | Newsvendor, políticas, media-varianza |
| 9.5 | [El agente que decide](05_el_agente_que_decide.md) | Pipeline completo, taxonomía de problemas, mirada adelante |

## Cómo correr el lab (para imágenes)

```bash
cd clase/09_teoria_decision
python lab_decision.py
```

## Flujo de trabajo: lee y haz

| Paso | Actividad | Material |
|:----:|-----------|----------|
| 1 | **Lee** 9.1: Anatomía de decisión | [Notas](01_anatomia_decision.md) |
| 2 | **Lee** 9.2: Utilidad y preferencias | [Notas](02_utilidad_preferencias.md) |
| 3 | **Haz** Secciones 1-2 del notebook | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/09_teoria_decision/notebooks/01_decisiones_y_utilidad.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> |
| 4 | **Lee** 9.3: Decidir bajo incertidumbre | [Notas](03_decidir_bajo_incertidumbre.md) |
| 5 | **Haz** Secciones 3-4 del notebook | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/09_teoria_decision/notebooks/01_decisiones_y_utilidad.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> |
| 6 | **Lee** 9.4: Optimización estocástica | [Notas](04_optimizacion_estocastica.md) |
| 7 | **Haz** Sección 5 del notebook | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/09_teoria_decision/notebooks/01_decisiones_y_utilidad.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> |
| 8 | **Lee** 9.5: El agente que decide | [Notas](05_el_agente_que_decide.md) |

## Materiales

| Tipo | Archivo | Descripción |
|:----:|---------|-------------|
| Notas | [9.1 Anatomía](01_anatomia_decision.md) | Estados, acciones, utilidades, tres regímenes |
| Notas | [9.2 Utilidad](02_utilidad_preferencias.md) | Axiomas vNM, funciones de utilidad, riesgo |
| Notas | [9.3 Incertidumbre](03_decidir_bajo_incertidumbre.md) | MEU, árboles, VoI |
| Notas | [9.4 Estocástica](04_optimizacion_estocastica.md) | Newsvendor, políticas, media-varianza |
| Notas | [9.5 Agente](05_el_agente_que_decide.md) | Pipeline completo, reflexión |
| Notebook | [NB1: Decisiones y utilidad](notebooks/01_decisiones_y_utilidad.ipynb) | Interactivo: matrices, utilidad, MEU, VoI, newsvendor |
| Lab | [lab_decision.py](lab_decision.py) | Genera todas las visualizaciones |
| Lectura | [DMUU Ch. 3](lecturas_decision.pdf) | Kochenderfer: Decision Problems (pp 57-74) |

## Objetivos de aprendizaje

Al terminar este módulo podrás:

1. **Definir** formalmente un problema de decisión: estados $S$, acciones $A$, resultados $O$, creencias $P(S)$, preferencias $U$.
2. **Explicar** los axiomas de von Neumann-Morgenstern y por qué garantizan la existencia de una función de utilidad.
3. **Calcular** la utilidad esperada de una acción y encontrar la acción óptima bajo el principio MEU.
4. **Construir** árboles de decisión y resolverlos por inducción hacia atrás.
5. **Calcular** el Valor de la Información (VoI) y determinar cuándo vale la pena obtener más datos.
6. **Formular** el problema del vendedor de periódicos y derivar la cantidad óptima.
7. **Distinguir** entre los criterios MEU, maximin y minimax regret, y cuándo usar cada uno.
8. **Analizar** cómo la predicción (mod 08) alimenta las decisiones y cuándo una predicción tiene valor real.

---

**Siguiente:** [Anatomía de un problema de decisión →](01_anatomia_decision.md)
