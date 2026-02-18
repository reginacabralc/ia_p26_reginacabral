---
title: "Estrategia 2: Siempre la Más Probable"
---

# Estrategia 2: Siempre la Más Probable

## Intuición

Si tuvieras un prior sobre qué palabras son más probables como respuesta (por ejemplo, frecuencia de uso en español), una estrategia natural es: **siempre adivina la palabra más probable** entre los candidatos restantes.

```
Para cada turno:
  1. Filtra los candidatos consistentes con el historial
  2. Ordena por probabilidad (frecuencia de uso)
  3. Adivina la de mayor probabilidad
```

## ¿Por qué parece inteligente?

Maximiza $P(\text{ganar este turno})$. Si la palabra más probable tiene un 15% de probabilidad, estás tomando la apuesta con mayor probabilidad de éxito inmediato.

## ¿Por qué es subóptima?

El problema es que optimiza para **ganar ahora**, no para **aprender**. Considera esta situación:

Supón que quedan 10 candidatos. La más probable tiene $p = 0.15$. Hay otra palabra que, aunque menos probable como respuesta, produce un feedback que **distingue entre 8 de los 10 candidatos**. Si la primera falla (85% de las veces), aprendes poco. Si la segunda falla, aprendes mucho.

La estrategia de máxima probabilidad es **greedy en explotación**: apuesta todo a ganar ahora y sacrifica aprendizaje.

## Exploración vs. explotación

Esta tensión es fundamental en inteligencia artificial:

- **Explotación** (exploit): usa lo que sabes para maximizar la recompensa inmediata
- **Exploración** (explore): sacrifica recompensa inmediata para obtener información que mejore decisiones futuras

La estrategia de máxima probabilidad es pura explotación. Las estrategias basadas en entropía (siguientes secciones) incorporan exploración.

## ¿Cuándo SÍ es óptima?

Cuando la incertidumbre es muy baja:

- Si quedan 1-2 candidatos, simplemente adivina el más probable
- Si un candidato tiene probabilidad > 50%, la apuesta directa tiene valor esperado alto

En general, **al final del juego** la explotación domina. **Al inicio** la exploración es más valiosa. Las mejores estrategias navegan esta transición.

---

**Siguiente:** [Entropía ingenua →](04_entropia_ingenua.md)

**Volver:** [← Índice del proyecto](00_index.md)
