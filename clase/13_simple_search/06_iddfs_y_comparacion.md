---
title: "IDDFS y comparación"
---

# IDDFS y comparación de algoritmos

> *"The best of both worlds."*

---

Hemos visto dos algoritmos con propiedades complementarias:

| | BFS | DFS |
|---|---|---|
| Memoria | Cara — $O(b^d)$ | Barata — $O(bm)$ |
| Optimalidad | Sí (sin pesos) | No |
| Completitud | Sí | Sí (finito) |

¿Podemos tener la memoria barata de DFS con las garantías de BFS? Sí: se llama **búsqueda iterativa por profundización** (IDDFS, *Iterative Deepening Depth-First Search*).

---

## 1. La idea central: DFS con límite de profundidad creciente

La observación clave es que BFS encuentra el objetivo a la profundidad mínima $d$ porque explora todos los nodos a profundidad $< d$ antes de llegar a profundidad $d$. DFS no garantiza esto — puede ir a profundidades mayores antes de encontrar la solución.

¿Qué tal si forzamos a DFS a no ir más allá de cierta profundidad?

**DFS con límite de profundidad $d$**: ejecuta DFS pero *nunca expande nodos a profundidad mayor que $d$*. Si el objetivo está a profundidad $\leq d$, lo encuentra. Si no, devuelve fallo.

**IDDFS**: ejecuta DFS con límite $0$, luego con límite $1$, luego $2$, así sucesivamente hasta encontrar la solución.

```
IDDFS(problema):
    para d = 0, 1, 2, 3, ...:
        resultado ← DFS-CON-LÍMITE(problema, d)
        si resultado ≠ FALLO:
            devolver resultado
```

---

## 2. DFS con límite de profundidad: implementación

La única diferencia con `PilaDeFrontera`: rechazamos nodos que excedan el límite. Para saber la profundidad de un nodo, usamos el parámetro opcional `padre` que pasamos al hacer `push`.

```python
class PilaConLimite(Frontera):
    """
    Frontera tipo pila con límite de profundidad.
    Produce DFS-con-límite cuando se usa con busqueda_generica.
    """

    def __init__(self, limite):
        self.pila = []
        self.miembros = {}     # nodo → profundidad
        self.limite = limite
        self.poda = False      # ¿se podó algún nodo por el límite?

    def push(self, nodo, padre=None):
        # Calculamos la profundidad del nodo a partir del padre
        prof_padre = self.miembros.get(padre, -1) if padre is not None else -1
        prof_nodo = prof_padre + 1

        if prof_nodo <= self.limite:
            self.pila.append(nodo)
            self.miembros[nodo] = prof_nodo
        else:
            self.poda = True  # registramos que hubo poda

    def pop(self):
        nodo = self.pila.pop()
        # No eliminamos de miembros: necesitamos la profundidad para calcular hijos
        return nodo

    def contains(self, nodo):
        return nodo in self.miembros and nodo in self.pila  # solo si sigue en pila

    def is_empty(self):
        return len(self.pila) == 0


def dfs_con_limite(problema, limite):
    return busqueda_generica(problema, PilaConLimite(limite))


def iddfs(problema, max_depth=1000):
    for d in range(max_depth + 1):
        resultado = dfs_con_limite(problema, d)
        if resultado is not None:
            return resultado
    return None
```

---

## 3. Ejemplo: IDDFS en acción

Usamos un árbol con factor de ramificación $b = 2$ y objetivo en profundidad 3. El objetivo es el nodo `K`.

![IDDFS iteraciones]({{ '/13_simple_search/images/12_iddfs_levels.png' | url }})

| Iteración | Límite | Nodos explorados | ¿Encontró K? |
|-----------|--------|-----------------|--------------|
| 0 | 0 | `{A}` | No |
| 1 | 1 | `{A, B, C}` | No |
| 2 | 2 | `{A, B, C, D, E, F, G}` | No |
| 3 | 3 | todos | **Sí** |

Nótese que K está en el nivel 3 de la rama izquierda del árbol. IDDFS lo encuentra exactamente en la iteración 3.

---

## 4. La objeción del trabajo redundante — y por qué no importa

La crítica obvia: IDDFS re-explora los mismos nodos en cada iteración. ¿No es eso ineficiente?

Hagamos las cuentas. Con $b = 3$ y objetivo a profundidad $d = 4$:

| Iteración | Nodos en esa iteración | Nodos acumulados |
|-----------|----------------------|-----------------|
| 0 | $1$ | $1$ |
| 1 | $1 + 3 = 4$ | $5$ |
| 2 | $1 + 3 + 9 = 13$ | $18$ |
| 3 | $1 + 3 + 9 + 27 = 40$ | $58$ |
| 4 | $1 + 3 + 9 + 27 + 81 = 121$ | $179$ |

BFS exploraría $1 + 3 + 9 + 27 + 81 = 121$ nodos. IDDFS exploró $179$ — solo $48\%$ más.

En general, el total de expansiones de IDDFS es:

$$N_{\text{IDDFS}} = \sum_{i=0}^{d} \sum_{j=0}^{i} b^j \approx \frac{b}{b-1} \cdot b^d = O(b^d)$$

El trabajo redundante es absorbido por el término dominante $b^d$. **La complejidad asintótica de IDDFS es idéntica a la de BFS.**

---

## 5. Tabla de comparación completa

| Propiedad | BFS | DFS | IDDFS |
|---|---|---|---|
| **Frontera** | Cola (FIFO) | Pila (LIFO) | Pila con límite $d$, en loop |
| **Tiempo** | $O(b^d)$ | $O(b^m)$ | $O(b^d)$ |
| **Espacio** | $O(b^d)$ | $O(bm)$ | $O(bd)$ |
| **Completo** | Sí | Sí (finito + explorado) | Sí |
| **Óptimo** | Sí (sin pesos) | No | Sí (sin pesos) |
| **Implementación** | `popleft()` | `pop()` | loop + pila con límite |

Donde: $b$ = factor de ramificación, $d$ = profundidad de la solución, $m$ = profundidad máxima del grafo.

![Comparación de complejidad de tiempo y espacio]({{ '/13_simple_search/images/13_complexity_comparison.png' | url }})

---

## 6. ¿Cuándo usar cada algoritmo?

### Usa BFS cuando:
- Necesitas el **camino más corto** (en número de pasos) de forma garantizada.
- El grafo es **poco profundo y ancho** — los niveles no tienen demasiados nodos.
- La memoria no es una limitación crítica.
- **Ejemplos:** encontrar el camino mínimo en un laberinto pequeño, grados de separación en una red social local, flood fill en imágenes pequeñas.

### Usa DFS cuando:
- Necesitas **cualquier** solución rápido (no importa si es óptima).
- El grafo es **profundo** y la solución probablemente está lejos del inicio.
- La **memoria es limitada** — DFS usa $O(bm)$ vs $O(b^d)$ de BFS.
- Quieres explorar **todas** las soluciones posibles (DFS con backtracking).
- **Ejemplos:** explorar laberintos, resolver puzzles con backtracking, encontrar componentes conexas.

### Usa IDDFS cuando:
- Necesitas las **garantías de BFS** (completitud + optimalidad) pero tienes **memoria limitada**.
- No sabes de antemano la profundidad de la solución.
- El factor de ramificación es grande — la penalización del trabajo redundante de IDDFS es pequeña comparada con el ahorro en memoria.
- **Ejemplos:** búsqueda en espacios de estados grandes con soluciones a profundidad desconocida.

---

## 7. Preview: búsqueda informada

Los tres algoritmos que hemos visto son **no informados** (*uninformed* o *blind*): no usan ninguna información sobre cuán cerca está la meta. Exploran el espacio de estados de forma sistemática pero sin guía.

El siguiente paso natural es añadir **información heurística**: una estimación de cuán lejos estamos de la meta. Esto da lugar a:

- **Búsqueda voraz por mejor primero** (*greedy best-first*): frontera = cola de prioridad ordenada por $h(n)$ (heurística).
- **A***: frontera = cola de prioridad ordenada por $f(n) = g(n) + h(n)$ (costo real + heurística).

A* con una heurística admisible (que nunca sobrestima) es completo, óptimo, y en la práctica mucho más eficiente que BFS e IDDFS porque guía la búsqueda hacia la meta.

---

**Inicio:** [Volver al índice →](00_index.md)
