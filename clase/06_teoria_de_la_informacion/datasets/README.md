---
title: "Datasets (descarga y licencias)"
---

# Datasets (descarga y licencias)

Este módulo usa **priors realistas** para:

- palabras en español (para Wordle/hacking),
- contraseñas comunes (para password guessing),

pero **no** comiteamos datasets grandes en el repo. En su lugar:

- incluimos un fallback pequeño (offline) para demos rápidas,
- y scripts para descargar y procesar datasets completos.

## 1) Palabras en español con frecuencias (OpenSLR SLR21)

Usamos el recurso **OpenSLR SLR21** (`es_wordlist.json`) con licencia **CC BY-SA 3.0**.

- Fuente: OpenSLR SLR21
- Licencia: CC BY-SA 3.0
- Uso: obtener conteos/frecuencias aproximadas de palabras.

**Qué descargamos:** un tarball `es_wordlist.json.tgz` y lo procesamos.

## 2) Listas de contraseñas comunes (SecLists)

Usamos **SecLists** (MIT) para listas “common credentials”.

⚠️ Nota ética/legal:

- Evitamos datasets de leaks personales “raw” cuando sea posible.
- Aun así, listas de contraseñas comunes existen y se usan para auditorías defensivas.
- Este material es **educativo** y debe usarse solo con fines defensivos o en entornos autorizados.

## Descarga y preparación

Desde `clase/06_teoria_de_la_informacion/`:

```bash
python -m datasets.download_datasets
python -m datasets.prepare_lexicons
```

Esto generará archivos en `datasets/cache/` (no deberían comitearse si son grandes).

## Fallback offline (comiteado)

Si no hay internet, el capstone usa:

- `datasets/mini_spanish_5letter.txt`
- `datasets/mini_passwords.txt`

Son listas pequeñas, suficientes para explicar el método (no para “realismo” total).

