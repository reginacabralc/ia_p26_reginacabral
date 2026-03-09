---
title: "Espacio de estados"
---

# Espacio de estados

> *"Well-defined problems are the beginning of solutions."*

---

En el módulo 2 definimos un **agente racional** como aquel que toma acciones para maximizar su medida de desempeño. Ahora necesitamos ser más precisos: ¿cómo *representa* un agente el problema que está resolviendo? ¿Cómo sabe qué acciones tiene disponibles y qué consecuencias tienen?

La respuesta es el **espacio de estados**: una formulación formal del problema que lo convierte en un grafo que podemos explorar.

---

## 1. Conexión con el módulo de agentes

Recordemos la clasificación de Russell & Norvig que vimos en el módulo 2. Un **agente basado en objetivos** (*goal-based agent*) necesita saber cuál es su meta y buscar secuencias de acciones para alcanzarla.

Los entornos más simples para estudiar búsqueda son:

| Propiedad | Valor |
|---|---|
| Observable | Totalmente (el agente conoce el estado completo) |
| Determinista | Sí (las acciones tienen efecto predecible) |
| Estático | Sí (el entorno no cambia mientras el agente piensa) |
| Discreto | Sí (número finito de estados y acciones) |
| Un agente | Sí |

En este entorno, el problema del agente se reduce completamente a **encontrar un camino en un grafo**. Eso es búsqueda.

---

## 2. Formulación del problema

Un problema de búsqueda se especifica con cinco componentes:

$$\text{Problema} = (S,\; s_0,\; A,\; T,\; \text{Goal})$$

| Símbolo | Nombre | Significado |
|---|---|---|
| $S$ | **Estados** | Conjunto de todas las configuraciones posibles del mundo |
| $s_0 \in S$ | **Estado inicial** | Dónde empieza el agente |
| $A(s)$ | **Acciones** | Conjunto de acciones disponibles en el estado $s$ |
| $T(s, a)$ | **Función de transición** | Estado resultante de aplicar $a$ en $s$ |
| $\text{Goal}(s)$ | **Test de objetivo** | Predicado: ¿es $s$ una solución? |

Una **solución** es una secuencia de acciones $a_1, a_2, \ldots, a_k$ tal que:

$$T(T(\ldots T(s_0, a_1)\ldots, a_{k-1}), a_k) = s^*$$

donde $\text{Goal}(s^*) = \text{True}$.

---

## 3. El espacio de estados como grafo

Una vez tenemos la formulación $(S, s_0, A, T, \text{Goal})$, el **espacio de estados** es el grafo dirigido donde:

- **Nodos** = estados en $S$
- **Aristas** = pares $(s, T(s,a))$ para todo $s \in S$ y $a \in A(s)$

Buscar una solución equivale a **encontrar un camino** desde $s_0$ hasta cualquier estado $s^*$ con $\text{Goal}(s^*) = \text{True}$.

Este es el puente entre la formulación abstracta del problema y los algoritmos de grafos que vamos a desarrollar.

---

## 4. Ejemplo 1: robot en una cuadrícula

**Problema:** un robot en una cuadrícula de $3 \times 3$ con un obstáculo quiere ir de la esquina superior-izquierda a la esquina inferior-derecha.

| Componente | Definición |
|---|---|
| $S$ | $\{(r,c) \mid 0 \leq r,c \leq 2,\; (r,c) \neq (1,1)\}$ — celdas libres |
| $s_0$ | $(0, 0)$ |
| $A(s)$ | $\{\text{arriba, abajo, izquierda, derecha}\}$ restringidas a celdas libres |
| $T((r,c), \text{abajo})$ | $(r+1, c)$ si es celda libre |
| $\text{Goal}(s)$ | $s = (2, 2)$ |

El espacio de estados tiene **8 nodos** (9 celdas menos el obstáculo) y un número de aristas proporcional al número de movimientos válidos.

![Robot en cuadrícula y su espacio de estados]({{ '/13_simple_search/images/06_grid_state_space.png' | url }})

La imagen muestra: a la izquierda, la cuadrícula física con el obstáculo; a la derecha, el grafo del espacio de estados donde cada celda libre es un nodo y cada movimiento válido es una arista.

---

## 5. Ejemplo 2: problema del mapa de rutas

**Problema:** encontrar un camino de carretera entre dos ciudades.

| Componente | Definición |
|---|---|
| $S$ | Conjunto de ciudades |
| $s_0$ | Ciudad de origen (ej. Ciudad de México) |
| $A(s)$ | Ciudades conectadas directamente por carretera |
| $T(s, a)$ | La ciudad $a$ (la acción *es* el destino) |
| $\text{Goal}(s)$ | $s = $ ciudad de destino (ej. Guadalajara) |

Aquí el espacio de estados **es** el mapa de carreteras — el grafo ya existe explícitamente.

---

## 6. Tamaño del espacio de estados: por qué importa

El tamaño del espacio de estados determina la dificultad del problema. Considera el **8-puzzle** (tablero de $3 \times 3$ con 8 fichas numeradas y un hueco):

| Aspecto | Valor |
|---|---|
| Estados posibles | $9! = 362{,}880$ |
| Estados alcanzables | $\approx 181{,}440$ (la mitad, por razones de paridad) |
| Factor de ramificación promedio | $\approx 2.67$ |

El 8-puzzle es *trivial* para BFS moderno. Ahora considera el **15-puzzle** ($4 \times 4$):

| Aspect | Valor |
|---|---|
| Estados posibles | $16! \approx 2 \times 10^{13}$ |
| Factor de ramificación | $\approx 3$ |

A $10^7$ expansiones por segundo, explorar todo el espacio tardaría **millones de años**. Aquí ya necesitamos algoritmos inteligentes.

El 8-puzzle sirve para ilustrar algoritmos y entender su comportamiento. Pero la motivación real para los algoritmos que estudiaremos (BFS, DFS, IDDFS y más adelante A*) es que el espacio de estados crece exponencialmente con la profundidad.

---

## 7. Por qué necesitamos frontera y conjunto explorado

Tenemos el espacio de estados. Queremos encontrar un camino de $s_0$ a algún $s^*$. La idea más naive: **explorar nodo por nodo**.

Pero hay dos problemas:

**Problema 1: Ciclos.** Un grafo con un ciclo $A \to B \to C \to A$ haría que un algoritmo ingenuo explore $A, B, C, A, B, C, \ldots$ infinitamente.

**Solución:** Mantener un **conjunto explorado** (*explored set*) con los nodos ya procesados completamente. Nunca volver a explorar un nodo que ya está ahí.

**Problema 2: Eficiencia.** No queremos re-visitar nodos que ya están pendientes de explorar.

**Solución:** Mantener una **frontera** (*frontier*) con los nodos descubiertos pero aún no procesados. Solo añadir a la frontera nodos que no estén ya explorados ni en la frontera.

Juntos, frontera y conjunto explorado forman la estructura del **algoritmo genérico de búsqueda** que veremos en el siguiente capítulo.

---

**Siguiente:** [Algoritmo genérico de búsqueda →](03_busqueda_generica.md)
