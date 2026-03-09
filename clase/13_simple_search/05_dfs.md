---
title: "Búsqueda en profundidad (DFS)"
---

# Búsqueda en profundidad (DFS)

> *"In order to understand recursion, one must first understand recursion."*

---

DFS es `busqueda_generica` con `frontera = PilaDeFrontera`. La diferencia respecto a BFS es exactamente una línea: en lugar de `popleft()` (FIFO), usamos `pop()` (LIFO). Esta pequeña diferencia produce un comportamiento radicalmente distinto.

---

## 1. Intuición: explorar hasta el fondo antes de volver

Imagina que estás explorando un laberinto. La estrategia DFS es: siempre avanza por el pasillo más reciente que descubriste. Si llegas a un callejón sin salida, *retroce* (*backtrack*) al punto donde tomaste el último desvío y prueba el siguiente.

DFS **va tan profundo como puede** en una rama antes de considerar ramas alternativas. El resultado: puede encontrar la solución rápido si está en la rama que elige primero, o puede explorar un laberinto enorme antes de encontrarla si eligió mal.

---

## 2. En lenguaje natural

1. Crea una **pila** (LIFO) con el nodo inicial.
2. Mientras la pila no esté vacía:
   a. Toma el nodo *más reciente* de la pila (el último en entrar).
   b. Si es la meta, reconstruye y devuelve el camino.
   c. Márcalo como explorado.
   d. Añade a la pila todos sus vecinos que no hayan sido explorados ni estén ya en la pila.
3. Si la pila se vacía sin encontrar la meta, devuelve fallo.

La diferencia con BFS está en el paso 2a: **el más reciente**, no el más antiguo. Esto hace que DFS "se entierre" en la rama más nueva antes de retroceder.

---

## 3. Pseudocódigo (antes del ejemplo)

```
DFS(problema):
    frontera ← Pila con [inicio]
    explorado ← {}
    padre ← {inicio: null}

    mientras frontera no vacía:
        nodo ← frontera.POP()               [L1: tomar el más reciente]

        si ES-META(nodo):                   [L2: test de objetivo]
            devolver RECONSTRUIR(padre, nodo)

        explorado.añadir(nodo)              [L3: marcar como explorado]

        para vecino en VECINOS(nodo):       [L4: expandir vecinos]
            si vecino ∉ explorado
            y vecino ∉ frontera:
                padre[vecino] ← nodo
                frontera.AÑADIR(vecino)     [L5: apilar vecino]

    devolver FALLO
```

Compara con el pseudocódigo de BFS: **la única diferencia es `POP()` vs `POPLEFT()`**.

---

## 4. Ejemplo paso a paso

Usamos el mismo grafo de 6 nodos. Recordemos: $\{A,B\}, \{A,C\}, \{B,D\}, \{B,E\}, \{C,E\}, \{D,F\}, \{E,F\}$. Buscamos F desde A. Los vecinos se ordenan alfabéticamente, pero al apilarlos en orden alfabético, el primero en entrar es el último en salir — así que B estará encima de C.

![DFS paso a paso]({{ '/13_simple_search/images/10_dfs_step_by_step.png' | url }})

| Paso | Nodo actual | Pila (tope a la derecha) | Explorado | Qué pasó |
|------|-------------|--------------------------|-----------|----------|
| 0 | — | `[A]` | `{}` | Inicialización. |
| 1 | A | `[C, B]` | `{A}` | **L1**: pop A. **L4-L5**: push C, luego B. B queda en tope. |
| 2 | B | `[C, E, D]` | `{A, B}` | **L1**: pop B (tope). **L4-L5**: push E, luego D. D queda en tope. |
| 3 | D | `[C, E, F]` | `{A, B, D}` | **L1**: pop D. **L5**: push F. |
| 4 | F | — | — | **L1**: pop F. **L2**: F es la meta. ¡Encontrado! |

**Camino encontrado:** `A → B → D → F` (longitud 3).

En este caso particular, DFS encontró el mismo camino óptimo que BFS. Eso es coincidencia — DFS no garantiza optimalidad.

:::example{title="Un caso donde DFS no es óptimo"}
Modifica el grafo: añade la arista $\{A, F\}$ directamente. Ahora el camino óptimo es `A → F` (longitud 1). BFS lo encontraría de inmediato (F está en el nivel 1). DFS, si explora B antes que F, se iría por la rama `A → B → D → F` y devolvería un camino de longitud 3 — no el óptimo.
:::

---

## 5. DFS y la recursión

DFS tiene una implementación recursiva elegante que muestra por qué la pila es natural:

```python
def dfs_recursivo(problema, nodo, explorado, padre):
    if problema.es_meta(nodo):
        return reconstruir_camino(padre, nodo)
    explorado.add(nodo)
    for vecino in problema.vecinos(nodo):
        if vecino not in explorado:
            padre[vecino] = nodo
            resultado = dfs_recursivo(problema, vecino, explorado, padre)
            if resultado is not None:
                return resultado
    return None
```

La **pila del sistema** (call stack de la recursión) *es* la frontera de DFS. Cada llamada recursiva corresponde a apilar un nodo; el retorno corresponde a hacer pop. Son exactamente la misma idea.

La versión iterativa que usamos (con `PilaDeFrontera`) es equivalente pero más explícita — y evita el riesgo de desbordamiento de pila (*stack overflow*) en grafos muy profundos.

---

## 6. Comparación directa: BFS vs DFS en el mismo grafo

La diferencia de comportamiento queda clara viendo los árboles de búsqueda que genera cada algoritmo:

![BFS vs DFS: árbol de búsqueda]({{ '/13_simple_search/images/11_dfs_vs_bfs_tree.png' | url }})

Los números junto a cada nodo indican el orden de descubrimiento.

- **BFS** descubre A(1), B(2), C(3), D(4), E(5), F(6) — nivel a nivel.
- **DFS** descubre A(1), B(2), D(3), F(4), E(5), C(6) — se hunde primero por B→D→F.

---

## 7. Implementación Python

```python
class PilaDeFrontera(Frontera):
    """Frontera tipo pila (LIFO). Produce DFS cuando se usa con busqueda_generica."""

    def __init__(self):
        self.pila = []          # lista Python — O(1) para append/pop
        self.miembros = set()   # para contains en O(1)

    def push(self, nodo, padre=None):
        # padre se ignora — DFS básico no rastrea profundidad
        self.pila.append(nodo)
        self.miembros.add(nodo)

    def pop(self):
        nodo = self.pila.pop()   # ← LIFO: el más reciente primero
        self.miembros.discard(nodo)
        return nodo

    def contains(self, nodo):
        return nodo in self.miembros

    def is_empty(self):
        return len(self.pila) == 0


def dfs(problema):
    return busqueda_generica(problema, PilaDeFrontera())
```

Comparación directa con `ColaDeFrontera`:

| `ColaDeFrontera` (BFS) | `PilaDeFrontera` (DFS) |
|---|---|
| `self.cola = deque()` | `self.pila = []` |
| `self.cola.append(nodo)` | `self.pila.append(nodo)` |
| `self.cola.popleft()` ← **FIFO** | `self.pila.pop()` ← **LIFO** |

**Eso es todo.** Una línea diferente produce un algoritmo completamente distinto.

---

## 8. Complejidad de tiempo y espacio

### Tiempo: $O(V + E)$ o $O(b^m)$

Al igual que BFS, cada nodo entra y sale de la frontera a lo sumo una vez: $O(V + E)$.

En términos de $b$ y $m$ (profundidad máxima del grafo):

$$T_{\text{DFS}} = O(b^m)$$

Nota importante: si $m \gg d$ (la profundidad máxima es mucho mayor que la profundidad de la solución), DFS puede ser mucho más lento que BFS en el peor caso.

### Espacio: $O(bm)$ — la gran ventaja de DFS

La pila de DFS nunca necesita contener más de **un camino desde el inicio hasta el nodo actual** más los hermanos de cada nodo en el camino. Esto es proporcional a la profundidad máxima:

$$S_{\text{DFS}} = O(bm)$$

Compara con $O(b^d)$ de BFS. Para $b = 10$, $d = m = 10$:

- BFS: $10^{10} = 10{,}000{,}000{,}000$ nodos en memoria.
- DFS: $10 \times 10 = 100$ nodos en memoria.

DFS usa **órdenes de magnitud menos memoria** que BFS. Esta es su ventaja principal.

---

## 9. Completitud y optimalidad

### Completitud: depende del grafo

**En grafos finitos con conjunto explorado:** DFS es completo. El conjunto explorado previene que el algoritmo entre en bucles infinitos.

**Sin conjunto explorado en grafos con ciclos:** DFS puede entrar en un bucle infinito y nunca encontrar la solución, aunque exista.

**En grafos infinitos:** DFS puede seguir bajando por una rama infinita y nunca volver. No es completo en este caso.

### Optimalidad: **no**

DFS **no es óptimo**. Puede encontrar un camino largo antes de descubrir uno corto, simplemente porque exploró esa rama primero. En el ejemplo de la sección 4, si se añade una arista directa $\{A,F\}$, DFS podría devolverla camino de longitud 3 en vez de 1.

---

## 10. Aplicaciones de DFS

### Encontrar componentes conexas

Para verificar si un grafo es conexo, o para encontrar todas sus componentes conexas, DFS es la herramienta natural:

```python
def componentes_conexas(grafo):
    visitado = set()
    componentes = []
    for nodo in grafo:
        if nodo not in visitado:
            # Nueva componente: DFS desde este nodo
            componente = []
            pila = [nodo]
            while pila:
                v = pila.pop()
                if v not in visitado:
                    visitado.add(v)
                    componente.append(v)
                    for vecino in grafo[v]:
                        if vecino not in visitado:
                            pila.append(vecino)
            componentes.append(componente)
    return componentes
```

### Detección de ciclos

DFS puede detectar ciclos: si durante la exploración encontramos un nodo que ya está en el camino actual (en la pila), hay un ciclo.

### Exploración de laberintos

La estrategia de explorar hasta el fondo y retroceder es exactamente cómo un humano exploraría un laberinto físico con la regla "sigue la pared derecha". DFS captura esta intuición de forma natural.

### Ordenamiento topológico (preview)

DFS tiene una propiedad útil: el orden en que los nodos *terminan de procesarse* (al hacer pop) es el inverso del **orden topológico** de un grafo dirigido acíclico (DAG). Esto tiene muchas aplicaciones en compiladores, schedulers de tareas, y análisis de dependencias.

---

## Resumen de DFS

| Propiedad | Valor | Justificación |
|---|---|---|
| Frontera | Pila (LIFO) | Nodo más reciente primero |
| Tiempo | $O(b^m)$ | Puede explorar toda la profundidad $m$ |
| Espacio | $O(bm)$ | Solo un camino + hermanos en memoria |
| Completo | Sí (finito + explorado) | No en grafos infinitos |
| Óptimo | **No** | Puede encontrar camino largo antes del corto |

---

**Siguiente:** [IDDFS y comparación →](06_iddfs_y_comparacion.md)
