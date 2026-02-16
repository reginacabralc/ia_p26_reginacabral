---
title: "Proyecto Wordle: Teoría de la Información en Acción"
---

# Proyecto Wordle: Teoría de la Información en Acción

:::project{id="PROJ-WORDLE" title="Proyecto Wordle" due="2026-03-02" points="10"}
Diseña, implementa y compara estrategias de Wordle usando herramientas de teoría de la información (entropía, ganancia de información, score esperado). Trabaja en el [repositorio del torneo](https://github.com/sonder-art/rtorneo_wordle_p26) y participa en el torneo del curso.

**Entrega:** Pull request en el [repositorio del torneo](https://github.com/sonder-art/rtorneo_wordle_p26) con tu archivo `estudiantes/<tu-equipo>/strategy.py`.
:::

## Notas de teoría

Estas notas cubren la teoría detrás de las estrategias de Wordle, progresando desde lo trivial hasta lo sofisticado. Léelas antes de implementar tu estrategia.

| Sección | Tema | Idea clave |
|:------:|------|-----------|
| W.1 | [El juego de Wordle](01_el_juego.md) | Reglas, feedback y estructura de información |
| W.2 | [Estrategia aleatoria](02_estrategia_aleatoria.md) | Baseline: adivinar al azar |
| W.3 | [Máxima probabilidad](03_maxima_probabilidad.md) | Greedy: siempre la más probable |
| W.4 | [Entropía ingenua](04_entropia_ingenua.md) | Maximizar bits esperados (3B1B S1) |
| W.5 | [Entropía ponderada](05_entropia_ponderada.md) | Incorporar frecuencia con sigmoide (3B1B S2) |
| W.6 | [Score esperado](06_score_esperado.md) | Minimizar intentos totales (3B1B S3) |
| W.7 | [Look-ahead](07_look_ahead.md) | Mirar dos pasos al futuro (3B1B S4) |
| W.8 | [Preguntas abiertas](08_preguntas_abiertas.md) | Direcciones creativas y extensiones |

---

## Repositorio del torneo

Todo el código vive en un repositorio separado: **[github.com/sonder-art/rtorneo_wordle_p26](https://github.com/sonder-art/rtorneo_wordle_p26)**

El repositorio es un framework completo de torneo que:

1. **Descubre** automáticamente todas las estrategias de estudiantes (de `estudiantes/<equipo>/strategy.py`)
2. **Ejecuta** juegos en paralelo (un proceso por estrategia, con timeout estricto)
3. **Rankea** con Borda Count sobre 6 rondas canónicas
4. **Genera** leaderboard, CSVs, histogramas y un dashboard web

### Setup

```bash
git clone git@github.com:sonder-art/rtorneo_wordle_p26.git
cd rtorneo_wordle_p26
pip install -r requirements.txt   # solo numpy + matplotlib
python3 run_all.py                # descarga corpus + corre torneo de prueba
```

`run_all.py` descarga las listas de palabras en español (4, 5 y 6 letras desde OpenSLR), corre las 6 rondas oficiales con 10 juegos por ronda, e imprime el leaderboard.

---

## Cómo funciona el torneo

### Las 6 rondas

Tu estrategia debe funcionar para **todas** las combinaciones:

| Ronda | Longitud | Modo |
|:-----:|:--------:|------|
| 1 | 4 letras | uniform (todas las palabras igualmente probables) |
| 2 | 4 letras | frequency (probabilidad ponderada por frecuencia de uso) |
| 3 | 5 letras | uniform |
| 4 | 5 letras | frequency |
| 5 | 6 letras | uniform |
| 6 | 6 letras | frequency |

### Scoring: Borda Count

En **cada ronda** se rankean las estrategias por promedio de intentos (menor = mejor):

1. 1er lugar recibe $N$ puntos ($N$ = total de estrategias), 2do recibe $N-1$, etc.
2. Empates reciben el promedio de los puntos de sus posiciones
3. Los puntos se **suman a través de las 6 rondas** (y de las repeticiones si hay varias)
4. **Gana quien tenga más puntos totales**

Juegos no resueltos y timeouts cuentan como `max_guesses + 1` intentos.

### Restricciones

| Recurso | Límite |
|---------|--------|
| Tiempo por juego | **5 segundos** (estricto, incluye `begin_game()` + todos los `guess()`) |
| CPU | 1 core por estrategia |
| Memoria | 2 GB por estrategia |
| Intentos máximos | 6 por juego |
| Dependencias | `numpy` + librería estándar de Python |

### Distribution shock

En modo **frequency** durante torneos oficiales, se aplica una perturbación aleatoria (~5%) a las probabilidades. Las probabilidades perturbadas se pasan en `config.probabilities` — son visibles pero no predecibles de antemano. Esto prueba la robustez de tu estrategia.

---

## Qué debes implementar

Tu entrega es **un solo archivo** `strategy.py` con una clase que hereda de `Strategy`. El framework importa únicamente ese archivo durante el torneo.

### Interfaz de la estrategia

```python
from strategy import Strategy, GameConfig
from wordle_env import feedback, filter_candidates

class MiEstrategia(Strategy):
    @property
    def name(self) -> str:
        return "MiEstrategia_mi_equipo"   # nombre único

    def begin_game(self, config: GameConfig) -> None:
        """Se llama al inicio de cada juego. Usa para precomputar."""
        self._vocab = list(config.vocabulary)
        self._config = config

    def guess(self, history: list[tuple[str, tuple[int, ...]]]) -> str:
        """Devuelve el siguiente intento dado el historial de feedback.

        history: lista de (intento, feedback) acumulados
          feedback: tupla de enteros — 2=verde, 1=amarillo, 0=gris

        Puede devolver cualquier combinación de letras (no solo palabras del vocabulario).
        """
        candidates = self._vocab
        for g, pat in history:
            candidates = filter_candidates(candidates, g, pat)
        # --- TU LÓGICA AQUÍ ---
        return candidates[0]
```

### GameConfig — lo que recibes al inicio de cada juego

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `config.word_length` | `int` | 4, 5, o 6 |
| `config.vocabulary` | `tuple[str,...]` | Todas las palabras válidas (la secreta sale de aquí) |
| `config.mode` | `str` | `"uniform"` o `"frequency"` |
| `config.probabilities` | `dict[str,float]` | palabra $\to$ probabilidad (suman 1) |
| `config.max_guesses` | `int` | Intentos máximos (6) |
| `config.allow_non_words` | `bool` | Si `True`, puedes adivinar cualquier combinación de letras |

### Utilidades disponibles

```python
from wordle_env import feedback, filter_candidates

# Simular feedback entre dos palabras
pat = feedback("canto", "arcos")   # → (1, 0, 1, 1, 0)

# Filtrar candidatos consistentes con el feedback
remaining = filter_candidates(word_list, "arcos", (1, 0, 1, 1, 0))
```

Usa `feedback()` para **simular** qué pasaría si adivinas una palabra contra cada candidato posible — así puedes evaluar qué tan bueno es un guess antes de hacerlo.

---

## Benchmarks

Tu estrategia compite contra estos 3 benchmarks incluidos:

| Estrategia | Qué hace | Nivel |
|-----------|----------|-------|
| **Random** | Elige al azar entre candidatos restantes | Baseline — si no le ganas, algo está mal |
| **MaxProb** | Elige el candidato más probable | Medio — pura explotación, sin exploración |
| **Entropy** | Maximiza entropía de Shannon del feedback | Fuerte — si le ganas consistentemente, excelente |

---

## Cómo probar tu estrategia

```bash
# Prueba rápida (verbose = ves cada intento y feedback)
python3 experiment.py --strategy "MiEstrategia_mi_equipo" --num-games 10 --verbose

# Probar configuración específica
python3 experiment.py --strategy "MiEstrategia_mi_equipo" --length 6 --mode frequency --num-games 20 --verbose

# Torneo local: tu equipo vs los 3 benchmarks (6 rondas oficiales)
python3 tournament.py --team mi_equipo --official --num-games 10

# Torneo completo con todos
python3 run_all.py --num-games 100

# Dashboard web (visualización de resultados)
python3 run_all.py --num-games 50 --dashboard
```

---

## Entrega

1. **Copia el template:**
   ```bash
   cp -r estudiantes/_template estudiantes/mi_equipo
   ```

2. **Edita** `estudiantes/mi_equipo/strategy.py` — **único archivo evaluado**

3. **Prueba** todas las configuraciones (4/5/6 letras, uniform/frequency)

4. **Abre un PR** en el [repositorio del torneo](https://github.com/sonder-art/rtorneo_wordle_p26):
   ```bash
   git add estudiantes/mi_equipo/strategy.py
   git commit -m "add strategy mi_equipo"
   git push
   ```

---

## Reglas

1. **Un archivo:** todo tu código en `estudiantes/<equipo>/strategy.py`
2. **Nombre único:** la propiedad `name` debe incluir el nombre del equipo
3. **Sin dependencias extra:** solo `numpy` + librería estándar de Python
4. **No ML/RL:** no redes neuronales, no Q-learning, no policy gradient
5. **Sí permitido:** agentes basados en metas/utilidad, búsqueda, simulaciones, teoría de la información, tablas precomputadas, heurísticas
6. **5 segundos** máximo por juego (estricto)
7. **No trampa:** solo recibes `history` de `(intento, feedback)` — no puedes acceder al secreto
8. **Puedes adivinar no-palabras:** cualquier combinación de letras es válida como intento exploratorio

---

## Consejos

- **Empieza simple.** El template ya filtra candidatos por feedback. Construye sobre eso.
- **Piensa en entropía.** Cada intento particiona el espacio de candidatos. Maximizar la "planitud" de esa partición es maximizar información por intento.
- **Simula antes de adivinar.** Usa `feedback()` para evaluar qué tan bueno es un guess contra todos los candidatos restantes *antes* de jugarlo.
- **Prueba todas las configuraciones.** Tu estrategia debe funcionar para 4, 5 y 6 letras en ambos modos.
- **Monitorea tiempos.** Usa `--verbose` para ver el tiempo por intento. El budget de 5s incluye `begin_game()` + todos los `guess()`.
- **Intentos no-palabra.** Puedes adivinar "aeiou" o cualquier combinación puramente para maximizar información (ver [sección W.8](08_preguntas_abiertas.md)).
- **Modo frequency.** Cuando quedan pocos candidatos en modo frequency, considera apostar por el más probable en vez de maximizar entropía (ver [sección W.6](06_score_esperado.md)).

## Referencia

- [3Blue1Brown: Solving Wordle using information theory](https://www.3blue1brown.com/lessons/wordle) — el video que inspira la progresión de estrategias de este proyecto
- [Reglas completas del torneo](https://github.com/sonder-art/rtorneo_wordle_p26/blob/main/docs/rules.md)
- [Guía de equipo paso a paso](https://github.com/sonder-art/rtorneo_wordle_p26/blob/main/docs/team_guide.md)

---

**Volver:** [← Índice del módulo](../00_index.md)
