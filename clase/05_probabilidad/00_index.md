---
title: "Probabilidad: Razonamiento bajo Incertidumbre"
---

# Probabilidad: Razonamiento bajo Incertidumbre

¿Cómo razonamos cuando no tenemos certeza absoluta?

## Contenido

| Sección | Tema | Descripción |
|---------|------|-------------|
| [01](01_intro.md) | Introducción | ¿Por qué necesitamos probabilidad? El problema del razonamiento plausible |
| [02](02_robot_desiderata.md) | El Robot Pensante | Los desiderata de Jaynes: qué queremos de un sistema de razonamiento |
| [03](03_probabilidad_como_logica.md) | Probabilidad como Lógica Extendida | La conexión profunda entre lógica y probabilidad |
| [04](04_interpretaciones.md) | Interpretaciones de Probabilidad | Frecuentista vs Bayesiano vs Jaynes |
| [05](05_conceptos_basicos.md) | Conceptos Básicos | Espacio muestral, eventos, medidas de probabilidad |
| [06](06_condicional_marginal.md) | Probabilidad Condicional y Marginal | P(A\|B), marginalización, independencia |
| [07](07_reglas_probabilidad.md) | Las Reglas de Probabilidad | Regla del producto y suma; Jaynes vs Kolmogorov |
| [08](08_bayes.md) | Teorema de Bayes | La joya de la corona: actualización de creencias |
| [09](09_esperanza_momentos.md) | Esperanza y Momentos | Valores esperados, varianza, covarianza |
| [11](11_distribuciones.md) | Distribuciones | Normal, Exponencial, Pareto, Cauchy y más |
| [12](12_estadistica_estimadores.md) | Estadística y Estimadores | MLE, método de momentos, estimación puntual |
| [13](13_tlc_lgn.md) | TLC y LGN | Teorema del Límite Central y Ley de los Grandes Números |
| [14](14_colas_largas.md) | Colas Largas (Fat Tails) | Cuando el TLC falla — Taleb y fenómenos extremos |

## Laboratorio

| Archivo | Descripción |
|---------|-------------|
| [lab_probabilidad.py](lab_probabilidad.py) | Simulaciones en Python: TLC, LGN, fat tails. Genera imágenes para las notas. |

Para ejecutar el laboratorio:
```bash
cd clase/05_probabilidad
python lab_probabilidad.py
```

## Ejercicios Prácticos: Fat Tails

Ejercicios interactivos para entender las colas largas usando datos reales y simulaciones.

| Ejercicio | Descripción | Datos |
|-----------|-------------|-------|
| [S&P 500](ejercicios/ejercicio_sp500.md) | Los eventos "imposibles" del mercado | Reales |
| [VaR](ejercicios/ejercicio_var.md) | Por qué el Value at Risk falla | Reales |
| [Sintético](ejercicios/ejercicio_sintetico.md) | Anatomía de las colas largas | Simulados |

**Setup con uv:**
```bash
cd clase/05_probabilidad/ejercicios

# Crear entorno
uv venv && source .venv/bin/activate

# Instalar dependencias
uv pip install -r requirements.txt

# Ejecutar
python ejercicio_sp500.py
python ejercicio_var.py
python ejercicio_sintetico.py
```

Ver [ejercicios/README.md](ejercicios/README.md) para instrucciones completas.

## Tareas

| # | Descripción | Puntos | Entrega |
|---|-------------|--------|---------|
| [10a](10_tarea_probabilidad.md#tarea-curso-datacamp--foundations-of-probability-in-python) | Curso DataCamp: Foundations of Probability in Python | 20 | 4 feb |
| [10b](10_tarea_probabilidad.md#tarea-ejercicios-de-probabilidad) | Ejercicios de Probabilidad, Conceptos y Álgebra Booleana | 20 | 4 feb |

## Lecturas

- [Lecturas de Probabilidad (PDF)](lecturas_probabilidad.pdf) — E.T. Jaynes, Capítulos 1-2

## Idea Central

> "La teoría de probabilidad no es más que sentido común reducido a cálculo."
> — Pierre-Simon Laplace

En esta sección exploraremos la probabilidad desde la perspectiva de **E.T. Jaynes**, quien argumenta que:

1. La probabilidad es una **extensión de la lógica** para manejar incertidumbre
2. Las reglas de probabilidad no son arbitrarias — son las **únicas** reglas consistentes
3. Toda probabilidad es **condicional** en información de fondo

Este enfoque unifica las visiones "frecuentista" y "bayesiana" bajo un marco más fundamental.

---

## Mapa Conceptual

```
LÓGICA DEDUCTIVA          RAZONAMIENTO PLAUSIBLE
     │                            │
  Certeza                    Incertidumbre
  (T/F)                      (grados 0-1)
     │                            │
     └──────────┬─────────────────┘
                │
        ┌───────▼───────┐
        │  DESIDERATA   │
        │  (requisitos) │
        └───────┬───────┘
                │
        ┌───────▼───────┐
        │   REGLAS DE   │
        │ PROBABILIDAD  │
        └───────┬───────┘
                │
        ┌───────▼───────┐
        │    BAYES      │
        │   THEOREM     │
        └───────┬───────┘
                │
    ┌───────────┴───────────┐
    │                       │
┌───▼───────┐       ┌───────▼───────┐
│DISTRIBU-  │       │ ESTADÍSTICA   │
│CIONES     │       │ (MLE, etc.)   │
└───┬───────┘       └───────┬───────┘
    │                       │
    └───────────┬───────────┘
                │
        ┌───────▼───────┐
        │  TLC & LGN    │
        │ (convergencia)│
        └───────┬───────┘
                │
        ┌───────▼───────┐
        │  FAT TAILS    │
        │ (¡cuidado!)   │
        └───────────────┘
```

---

**Siguiente:** [Introducción →](01_intro.md)
