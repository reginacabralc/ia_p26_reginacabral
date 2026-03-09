---
title: "Algoritmo genérico de búsqueda"
---

# Algoritmo genérico de búsqueda

> *"A good notation has a subtlety and suggestiveness which at times make it seem almost like a live teacher."*
> — Bertrand Russell

---

Este capítulo presenta la idea central del módulo: existe **un solo algoritmo de búsqueda**. BFS, DFS e IDDFS no son tres algoritmos distintos — son tres instancias del mismo algoritmo, cada una con una estructura de datos diferente para gestionar la frontera.

Entender esto no solo simplifica el aprendizaje; permite *diseñar* nuevos algoritmos cambiando únicamente la frontera.

---

## 1. La observación clave

Sabemos que buscar una solución = encontrar un camino en el grafo del espacio de estados. Para explorar el grafo necesitamos dos estructuras:

| Estructura | Rol |
|---|---|
| **Frontera** (*frontier*) | Nodos descubiertos pero aún no procesados. La "lista de pendientes". |
| **Conjunto explorado** (*explored*) | Nodos completamente procesados. Nunca volvemos aquí. |
| **Mapa de padres** (*parent*) | Registra de dónde vino cada nodo. Permite reconstruir el camino. |

La pregunta es: ¿en qué orden procesamos los nodos de la frontera?

La respuesta determina *completamente* el algoritmo.

---

## 2. El pseudocódigo genérico

```
función BUSQUEDA-GENERICA(problema):
    frontera ← NUEVA-FRONTERA(problema.inicio)
    explorado ← {}
    padre ← {problema.inicio: null}

    mientras frontera no esté vacía:
        nodo ← frontera.SELECCIONAR()            ← ¡Aquí está toda la magia!

        si problema.ES-META(nodo):
            devolver RECONSTRUIR-CAMINO(padre, nodo)

        explorado.añadir(nodo)

        para cada vecino de problema.VECINOS(nodo):
            si vecino no está en explorado
            y vecino no está en frontera:
                padre[vecino] ← nodo
                frontera.AÑADIR(vecino)

    devolver FALLO
```

Solo hay **una línea que cambia** entre todos los algoritmos de búsqueda no informada: cómo `frontera.SELECCIONAR()` elige el siguiente nodo.

---

## 3. La interfaz Frontera

Definimos una interfaz abstracta con tres operaciones:

| Operación | Descripción |
|---|---|
| `push(nodo, padre=None)` | Añade un nodo a la frontera. El parámetro `padre` es opcional — lo usan las fronteras que necesitan rastrear profundidad. |
| `pop()` | Elimina y devuelve el nodo a explorar a continuación. **Aquí vive la diferencia entre algoritmos.** |
| `contains(nodo)` | Verifica si un nodo está en la frontera. Necesario para evitar duplicados. |

Con esta interfaz, la tabla de algoritmos es:

| Frontera | Estrategia de `pop()` | Algoritmo resultante |
|---|---|---|
| Cola (FIFO) | El más *antiguo* primero | **BFS** |
| Pila (LIFO) | El más *reciente* primero | **DFS** |
| Pila con límite | El más reciente, hasta prof. $d$ | **DFS con límite** |
| Cola de prioridad (por costo) | El *más barato* primero | Costo uniforme / Dijkstra |
| Cola de prioridad ($g + h$) | El *más prometedor* primero | **A*** |

Los tres últimos los veremos en módulos posteriores. Por ahora nos concentramos en los dos primeros.

---

## 4. Por qué necesitamos el conjunto explorado: el problema de los ciclos

Considera este grafo de tres nodos con un ciclo:

```
A → B → C → A  (ciclo)
```

Sin conjunto explorado, `BUSQUEDA-GENERICA` desde A produciría:

```
paso 1: procesar A → añadir B a frontera
paso 2: procesar B → añadir C a frontera
paso 3: procesar C → añadir A a frontera  ← !
paso 4: procesar A → añadir B a frontera  ← otra vez
paso 5: procesar B → añadir C a frontera  ← otra vez
... bucle infinito
```

Con el conjunto explorado, en el paso 3 al intentar añadir A, el algoritmo ve que A ya está en `explorado` y simplemente no lo añade. El ciclo queda cortado.

---

## 5. El truco del conjunto sombra para `contains` eficiente

Implementar `contains` sobre una lista o deque es $O(n)$ — hay que revisar cada elemento. Para grafos grandes, esto destruye el rendimiento.

La solución es mantener un **conjunto sombra** (*shadow set*) paralelo a la estructura principal:

```python
class ColaDeFrontera:
    def __init__(self):
        self.cola = deque()     # para el orden FIFO
        self.miembros = set()   # para contains en O(1)

    def push(self, nodo, padre=None):
        self.cola.append(nodo)
        self.miembros.add(nodo)

    def pop(self):
        nodo = self.cola.popleft()
        self.miembros.discard(nodo)
        return nodo

    def contains(self, nodo):
        return nodo in self.miembros  # O(1)
```

El coste es duplicar el espacio de la frontera — siempre aceptable porque la frontera ya vive en memoria.

---

## 6. Reconstrucción del camino

El mapa `padre` registra, para cada nodo descubierto, desde qué nodo fue alcanzado. Una vez encontrada la meta, seguimos los padres hacia atrás:

```python
def reconstruir_camino(padre, meta):
    camino = []
    nodo = meta
    while nodo is not None:
        camino.append(nodo)
        nodo = padre[nodo]
    camino.reverse()
    return camino
```

Ejemplo con `padre = {A: None, B: A, D: B, F: D}` y meta `F`:

```
F → D → B → A → None
```

Reversed: `[A, B, D, F]` — el camino de inicio a meta.

---

## 7. Implementación Python completa

Esta es la única implementación del algoritmo genérico que usaremos en todo el módulo. BFS, DFS e IDDFS no tendrán su propio loop — solo su propia clase `Frontera`.

```python
from collections import deque

# ── Interfaz abstracta ────────────────────────────────────────────────────

class Frontera:
    """Interfaz abstracta. Cada subclase implementa una estrategia distinta."""

    def push(self, nodo, padre=None):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def contains(self, nodo):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError


# ── Funciones de búsqueda ─────────────────────────────────────────────────

def busqueda_generica(problema, frontera):
    """
    Algoritmo genérico de búsqueda.
    El algoritmo específico (BFS, DFS, etc.) está determinado únicamente
    por la clase `frontera` que se pasa como argumento.
    """
    inicio = problema.inicio
    frontera.push(inicio)
    explorado = set()
    padre = {inicio: None}

    while not frontera.is_empty():
        nodo = frontera.pop()

        if problema.es_meta(nodo):
            return reconstruir_camino(padre, nodo)

        explorado.add(nodo)

        for vecino in problema.vecinos(nodo):
            if vecino not in explorado and not frontera.contains(vecino):
                padre[vecino] = nodo
                frontera.push(vecino, padre=nodo)

    return None  # FALLO: no se encontró solución


def reconstruir_camino(padre, meta):
    """Reconstruye el camino desde el inicio hasta la meta usando el mapa de padres."""
    camino = []
    nodo = meta
    while nodo is not None:
        camino.append(nodo)
        nodo = padre[nodo]
    camino.reverse()
    return camino
```

---

## Resumen visual

```
                        busqueda_generica(problema, frontera)
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                  │
           ColaDeFrontera     PilaDeFrontera    PilaConLimite
               (FIFO)             (LIFO)          (LIFO + d)
                    │                 │                  │
                  BFS               DFS             DFS limitado
                                                         │
                                                      IDDFS
                                               (loop sobre DFS limitado)
```

En los próximos capítulos veremos exactamente cómo se implementa cada frontera y qué consecuencias tiene cada elección en términos de completitud, optimalidad y complejidad.

---

**Siguiente:** [Búsqueda en amplitud (BFS) →](04_bfs.md)
