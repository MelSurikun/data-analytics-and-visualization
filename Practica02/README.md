# Práctica 2: Reducción de dimensiones: PCA, Sammon y Autocodificadores

**Materia:** Analítica y Visualización de Datos (ESCOM-IPN)
**Profesor:** Ituriel Enrique Flores Estrada
**Conjunto de datos:** Breast Cancer Wisconsin (Diagnostic) — 569 muestras, 30 variables, 2 clases
**Objetivo:** proyectar los datos a 3 dimensiones con PCA, Sammon, Sammon sobre PCA y un autocodificador no lineal, comparar los métodos y presentar los resultados en un tablero.

> **📌 Esta entrega es un solo notebook: `Practica02.ipynb`.** Todos ponemos nuestra sección ahí, en el orden del desarrollo. Se edita **por turnos** (ver [reglas de trabajo](#5-dependencias-y-orden-de-trabajo)) y no hay notebooks individuales ni carpeta `src/`.

---

## Índice

1. [Equipo y repartición](#1-equipo-y-repartición)
2. [Reglas de entrega y evaluación](#2-reglas-de-entrega-y-evaluación)
3. [Acuerdos comunes (obligatorios para todos)](#3-acuerdos-comunes-obligatorios-para-todos)
4. [Tareas detalladas por persona](#4-tareas-detalladas-por-persona)
5. [Dependencias y orden de trabajo](#5-dependencias-y-orden-de-trabajo)
6. [Advertencias técnicas](#6-advertencias-técnicas)
7. [Preguntas pendientes para el profesor](#7-preguntas-pendientes-para-el-profesor)
8. [Reporte](#8-reporte)
9. [Estructura del repositorio](#9-estructura-del-repositorio)
10. [Checklist final antes de entregar](#10-checklist-final-antes-de-entregar)

---

## 1. Equipo y repartición

| Persona | Nombre | Responsable de | Puntos de rúbrica que cubre |
|---|---|---|---|
| **P1** | _Melanie_ | Sección 0 del notebook (funciones compartidas) + Sección 1 + Sección 3, incisos 3g–3i (barrido de k, stress contra k, k-NN y tabla del 3i) | 10 + ~10 de 30 |
| **P2** | _Magaly_ | Sección 2 (PCA) + Sección 6 (tablero y justificación del diseño) | 30 + 35 |
| **P3** | _Ricardo_ | Sección 3, incisos 3a–3f (Sammon directo, Sammon sobre PCA, Procrustes) + función `pca_mas_sammon(k)` | ~20 de 30 |
| **P4** | _Santiago_ | Sección 4 (autocodificador) + Sección 5 (tabla 5a y análisis 5b) | 30 + 35 |


> **El reporte lo hace cada quien** (no entra en la repartición). Cada integrante redacta la sección de lo que programó: propósito, procedimiento, evidencia e interpretación. Así todos entendemos todos los métodos, lo cual es necesario porque **el profe elige quién contesta la pregunta de teoría**. Ver sección 8 para las tareas compartidas del reporte.

---

## 2. Reglas de entrega y evaluación

**Calificación: 0 automático (y se pierde el derecho a examen del parcial) si:**
- No se entrega o se entrega después de la fecha y hora límite.
- La entrega **no incluye reporte**.
- No es un archivo comprimido **ZIP o RAR**.
- El nombre del comprimido no sigue el formato de **"ReglasEvaluación"** → revisar ese documento antes de entregar.
- **Quien no asista** a la evaluación presencial.

**Evaluación presencial:**
- Calificación final = teoría (34%) + reporte (33%) + código (33%).
- **Cada pregunta la contesta un integrante distinto.** El profe elige quién responde teoría; nosotros elegimos quién responde reporte y código.
- **Las capturas de código NO son evidencia de funcionamiento.** La evidencia son salidas ejecutadas: gráficas, tablas, tiempos y métricas.

**Rúbrica (200 pts):**

| Sección | Pts | Responsable |
|---|---|---|
| 1. Visualización y estandarización | 10 | P1 |
| 2. PCA | 30 | P2 |
| 3. Sammon | 30 | P3 (3a–3f) y P1 (3g–3i) |
| 4. Autocodificadores | 30 | P4 |
| 5. Análisis y conclusiones | 35 | P4 (con un párrafo de cada quien sobre su método) |
| 6. Tablero | 35 | P2 |
| 7. Reporte, cabecera y comentarios | 30 | Todos (cada quien su sección y sus celdas) |

> Ojo: la tabla de la rúbrica numera Análisis, Tablero y Reporte como 6, 7 y 8, pero en el desarrollo son 5, 6 y 7. **En el reporte usamos la numeración del desarrollo (5, 6, 7).**

---

## 3. Acuerdos comunes (obligatorios para todos)

Todo esto vive en la **Sección 0 del notebook** (P1). Nadie lo redefine por su cuenta; si algo se tiene que cambiar, se avisa al equipo y se cambia en la Sección 0.

### 3.1 Datos
```python
# pip install ucimlrepo
from ucimlrepo import fetch_ucirepo
wdbc = fetch_ucirepo(id=17)
X = wdbc.data.features                 # DataFrame: (569, 30)
y = wdbc.data.targets["Diagnosis"]     # "M" = maligno, "B" = benigno
```
- **El dataset no se sube al repositorio:** se descarga por código, así que la ejecución necesita internet.
- **Etiquetas:** vienen como texto, `M` y `B`. Usar siempre el diccionario `CLASES = {"M": "Maligno", "B": "Benigno"}` de la Sección 0.
- **Nombres de variables:** el sufijo indica el estadístico: `1` = media, `2` = error estándar y `3` = peor valor (por ejemplo, `area1`, `area2`, `area3`).
- **Estandarización:** `StandardScaler` sobre las **30 variables**. Variable común: `X_std`.
- Verificar al cargar que no hay valores faltantes y que no hay filas duplicadas (las filas duplicadas rompen Sammon, ver advertencias).

### 3.2 Semilla
```python
SEED = 42
import random, numpy as np
random.seed(SEED); np.random.seed(SEED)
# En la sección del autocodificador además:
# import tensorflow as tf; tf.keras.utils.set_random_seed(SEED)
```
Usar `random_state=SEED` en todo lo que lo acepte (PCA, StratifiedKFold, train_test_split, etc.).

Como todo corre en un solo notebook, las secciones anteriores mueven el generador de NumPy: **Sammon fija `np.random.seed(SEED)` justo antes de cada corrida**.

### 3.3 Colores (significado constante en todas las gráficas y en el tablero)
```python
COLORES_CLASE = {"Maligno": "#D1495B", "Benigno": "#2E86AB"}

COLORES_METODO = {
    "PCA": "#4C4C4C",
    "Sammon": "#EE8A1F",
    "Sammon sobre PCA": "#A61C8F",
    "Autocodificador": "#157F3B",
}
```
- Rojo = maligno y azul = benigno **siempre**. No cambiarlos en ninguna figura.
- Cada método tiene su color fijo para las gráficas de comparación y el tablero.
- Los colores de los métodos se eligieron para no confundirse entre sí ni con los de las clases, también con daltonismo. **No se cambian ni se agregan otros sin revisarlo con el equipo.**
- El naranja tiene poco contraste sobre fondo claro: en las gráficas y el tablero, cada método lleva siempre su **nombre visible**, no solo su color.

### 3.4 Medición de tiempos
- Usar **`time.perf_counter()`** siempre.
- Medir **solo la transformación** (fit/transform, entrenamiento o proyección), **no** graficación ni impresión.
- Reportar en **segundos con 4 decimales**.
- Anotar en el reporte el equipo usado (CPU, RAM, GPU sí/no), porque la práctica pide el tiempo "requerido por el equipo de cómputo utilizado".

```python
from time import perf_counter
t0 = perf_counter()
Z = pca.fit_transform(X_std)
t_pca = perf_counter() - t0
```

### 3.5 Exactitud de k-NN (un solo método para todo)
- **k-NN con 5 vecinos** (`n_neighbors=5`). En esta práctica, la letra `k` se reserva para el **número de dimensiones** de PCA (3g–3i).
- **Validación cruzada estratificada de 5 particiones** (`StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)`).
- Reportar **media ± desviación estándar** de la exactitud.
- Usar siempre la función compartida `evaluar_knn(Z, y)`. **Nadie programa su propio k-NN.**

### 3.6 Stress de Sammon (un solo cálculo para todo)
La tabla 5a pide stress de Sammon **para todos los métodos** (PCA, Sammon, Sammon sobre PCA y autocodificador), así que se calcula con una función común:

$$E = \frac{1}{\sum_{i<j} d^*_{ij}} \sum_{i<j} \frac{(d^*_{ij} - d_{ij})^2}{d^*_{ij}}$$

- `d*_ij` = distancia euclidiana en el **espacio estandarizado original de 30 dimensiones** (`X_std`).
- `d_ij` = distancia euclidiana en la proyección 3D.
- Función compartida: `stress_sammon(X_std, Z)`.
- **Importante:** para "Sammon sobre PCA" el stress que va en la tabla comparativa se calcula contra `X_std` (30D), **no** contra los datos de PCA a k dimensiones. Si no, los números no son comparables. El stress que devuelve la librería de Sammon es relativo a su entrada, así que en ese caso **se reportan los dos** y se aclara cuál es cuál.

### 3.7 Error de reconstrucción
- Métrica: **MSE** entre `X_std` y su reconstrucción.
- PCA: `pca.inverse_transform(Z)`.
- Autocodificador: salida del decodificador.
- Ambos se calculan **en el mismo espacio** (estandarizado) para que se puedan comparar.
- Sammon no reconstruye → en la tabla va **"no aplica"**.

### 3.8 Exportación de resultados (CSV)
- Carpeta `resultados/`, codificación UTF-8, separador coma.
- Donde algo no corresponda se escribe **`no aplica`**, **nunca `0`** ni vacío.
- Formato de la tabla comparativa (`resultados/comparativa.csv`):

| metodo | tiempo_s | tiempo_entrenamiento_s | tiempo_proyeccion_s | stress_sammon | knn_exactitud_media | knn_exactitud_std | error_reconstruccion_mse | notas |
|---|---|---|---|---|---|---|---|---|

`tiempo_s` es el tiempo total del método (en Sammon sobre PCA, PCA + Sammon; en el autocodificador, entrenamiento + proyección). Las columnas de entrenamiento y proyección solo aplican al autocodificador; en los demás métodos llevan `no aplica`.

- Archivos que debe generar cada quien:

| Archivo | Responsable | Contenido |
|---|---|---|
| `pca_varianza.csv` | P2 | PC, varianza explicada, varianza acumulada (10 PC) |
| `pca_error_reconstruccion.csv` | P2 | k, MSE |
| `pca_3d.csv` | P2 | PC1, PC2, PC3, clase |
| `sammon_3d.csv` | P3 | dim1, dim2, dim3, clase (Sammon directo) |
| `sammon_pca_3d.csv` | P3 | dim1, dim2, dim3, clase (Sammon sobre PCA con k del 95%) |
| `sammon_stress_iteraciones.csv` | P3 | iteración, stress |
| `sammon_procrustes.csv` | P3 | proyecciones comparadas, disparidad de Procrustes (3f) |
| `sammon_vs_k.csv` | P1 | k, tiempo PCA, tiempo Sammon, tiempo total, stress final, exactitud k-NN (las dos versiones) |
| `autoencoder_3d.csv` | P4 | z1, z2, z3, clase |
| `autoencoder_perdida.csv` | P4 | época, pérdida entrenamiento, pérdida validación |
| `comparativa.csv` | P4 (con las filas de todos) | tabla 5a |

### 3.9 Funciones compartidas (Sección 0 del notebook)
P1 las programa, las prueba y las sube **antes** de que los demás empiecen:

- `cargar_y_estandarizar()` → regresa `X` (DataFrame), `X_std` (arreglo), `y` (texto: Maligno/Benigno), `feature_names`, `scaler`
- `evaluar_knn(Z, y)` → regresa media y desviación de la exactitud
- `stress_sammon(X_ref, Z)` → regresa el stress
- `error_reconstruccion(X_ref, X_rec)` → regresa el MSE
- `graficar_3d(Z, y, titulo, num_figura)` → scatter 3D con `COLORES_CLASE`
- `exportar_csv(df, nombre)` → guarda en `resultados/` y reemplaza `NaN` por `"no aplica"`

### 3.10 Convenciones de código
- Cabecera y comentarios **según "ReglasEvaluación"** (cada quien en sus celdas).
- Variables y comentarios en español.
- **Reiniciar el kernel y ejecutar todo** (`Restart & Run All`) antes de subir. El notebook se entrega **con las salidas visibles**, porque esa es la evidencia de funcionamiento.
- Cada sección solo usa variables y funciones definidas **antes** de ella en el notebook.

---

## 4. Tareas detalladas por persona

### P1 — Sección 0, Sección 1 y Sammon 3g–3i

**Sección 0 del notebook (prioridad máxima: es lo primero que se hace)**
- [x] Carga del dataset y verificación (dimensiones, faltantes, duplicados, balance de clases).
- [x] Definir `SEED`, `CLASES`, `COLORES_CLASE`, `COLORES_METODO`.
- [x] Programar y probar todas las funciones compartidas (sección 3.9).
- [x] Crear la carpeta `resultados/` y la plantilla de `comparativa.csv` con las columnas acordadas.
- [ ] Subir al repo y avisar al equipo.

**Sección 1 — Visualización inicial y estandarización (10 pts)**
- [x] **1a.** Calcular la varianza de las 30 variables **originales**, elegir las 6 de mayor varianza y graficar un diagrama de caja y bigotes por cada una (separado por clase si se ve bien).
- [x] **1b.** Estandarizar con `StandardScaler`. Comprobar con una tabla que media ≈ 0 y desviación ≈ 1.
- [x] **1c.** Repetir 1a con los datos estandarizados. **Usar las mismas 6 variables del 1a** (después de estandarizar todas tienen varianza 1, así que no se pueden volver a "elegir por varianza"; explicarlo en el reporte).
- [x] Escribir en el reporte por qué cambian las escalas y por qué estandarizar es necesario para PCA, Sammon y k-NN.

**Sección 3, incisos 3g–3i — Barrido de k (parte de los 30 pts de Sammon)**

Usa la función `pca_mas_sammon(X_std, k)` y la función de Sammon adaptada que P3 deja en el notebook. **No reprogramar Sammon**, para que los resultados sean consistentes con los de P3. Mientras P3 la sube, se avanza con la sección 1.

- [ ] **3g.** Correr `pca_mas_sammon` para k ∈ {3, 5, 10, 20, 30} con la misma semilla. Graficar **stress final contra k** (reportar el stress de la librería y el stress contra `X_std`, aclarando cuál es cuál).
- [ ] **3h.** Exactitud de k-NN con `evaluar_knn` para cada k. Hacer **las dos versiones** mientras el profe no conteste (ver sección 7):
  - Versión A: k-NN sobre los datos de PCA a k dimensiones.
  - Versión B: k-NN sobre la proyección de Sammon 3D obtenida desde cada k.
  - Graficar exactitud contra k (las dos versiones en la misma gráfica, con leyenda).
- [ ] **3i.** Tabla con: tiempo total del 3a (lo da P3), tiempo total c)+d), stress final y exactitud k-NN para cada k.
- [ ] Exportar `sammon_vs_k.csv` (el tablero lo usa para las gráficas contra k).
- [ ] Pasarle a P4 un párrafo corto con lo que observaste del barrido de k (para el 5b).
- [ ] ⚠️ Son 5 corridas de Sammon. Dejarlas corriendo con tiempo, no el último día.

---

### P2 — Sección 2 (PCA) y Sección 6 (tablero)

**Sección 2 — PCA (30 pts)**
- [ ] **2b PRIMERO** (P3 lo necesita): ajustar PCA con todas las componentes sobre `X_std`, hacer la tabla de varianza explicada y acumulada de los 10 primeros PC, y **reportar cuántos PC acumulan al menos 95%** de la varianza. Guardarlo en la variable `k95` y avisar a P3 en cuanto lo tengas.
- [ ] **2a.** PCA a 3D sobre `X_std` midiendo el tiempo de `fit_transform`.
- [ ] **2c.** Gráfica de barras de varianza explicada por PC con línea superpuesta de varianza acumulada. Marcar la línea del 95%. Las dos series están en porcentaje, así que basta **un solo eje**.
- [ ] **2d.** Círculo de correlaciones (PC1 vs PC2): flechas de las variables dentro del círculo unitario. Las correlaciones son `componentes × sqrt(varianza)`. Si 30 flechas se amontonan, etiquetar solo las más largas y explicarlo.
- [ ] **2e.** Scatter 3D de PC1, PC2, PC3 con `COLORES_CLASE`.
- [ ] **2f.** Curva de error de reconstrucción (MSE) contra k = 1…30.
- [ ] Calcular para la tabla 5a: `stress_sammon(X_std, Z_pca3)`, `evaluar_knn(Z_pca3, y)` y el MSE de reconstrucción con k = 3.
- [ ] Exportar `pca_varianza.csv`, `pca_error_reconstruccion.csv`, `pca_3d.csv` y la fila de PCA para `comparativa.csv`.

**Sección 6 — Tablero (35 pts)**
- [ ] **Empezar desde ya con datos de prueba** usando el formato de CSV acordado; al final solo se cambian los archivos.
- [ ] Ponerse de acuerdo con P4 para que la conclusión del tablero coincida con la del análisis 5b.
- [ ] **6a.** Leer únicamente los CSV de `resultados/` (nada de números escritos a mano). Lo que no aplique aparece como "no aplica".
- [ ] **6b.** Una **sola vista** que responda: **¿qué método conviene y por qué?** Sugerencia de jerarquía:
  1. Arriba: la conclusión en una frase y las métricas clave por método (tiempo, stress, k-NN, error de reconstrucción).
  2. En medio: las 4 proyecciones 3D (o 2D) lado a lado, con los mismos colores de clase.
  3. Abajo: stress contra k y exactitud k-NN contra k.
- [ ] Paleta con significado constante (`COLORES_CLASE` y `COLORES_METODO`), legible y **sin decoración que no aporte información**.
- [ ] **6c.** Párrafo de **máximo 150 palabras** con **tres decisiones de diseño** (por ejemplo, tipo de gráfica, paleta, distribución) y por qué ayudan a interpretar. Contar las palabras.
- [ ] **6d.** Herramienta: Power BI, Tableau o Python. Si es Python, que corra sin pasos raros (dejar instrucciones en el repo).
- [ ] Capturas del tablero funcionando para el reporte.

---

### P3 — Sección 3, incisos 3a–3f (Sammon)

Implementación de referencia: https://github.com/tompollard/sammon

**Antes de empezar:** leer las advertencias de Sammon en la sección 6.

- [ ] **PRIORIDAD (P1 la necesita):** programar y subir pronto `pca_mas_sammon(X_std, k)` en la Sección 3 del notebook. Hace 3c + 3d y regresa un diccionario con `t_pca`, `t_sammon`, `t_total`, `Z` (proyección 3D), `stress_libreria` y `stress_xstd`. P1 usará esos nombres en 3g–3i. Avisar a P1 cuando esté lista.
- [ ] Adaptar la función de tompollard para guardar el historial de stress (ver advertencias) y dejarla en una celda de la Sección 3, para que P1 use la misma.
- [ ] **3a.** Sammon a 3D sobre `X_std` con `SEED`, midiendo el tiempo total. Graficar la **curva de stress por iteración**. Guardar `Z_sammon` y `stress_libreria_directo`, que P1 también usará en 3g–3i.
- [ ] **3b.** Scatter 3D de la proyección de 3a.
- [ ] **3c.** PCA de `X_std` a k dimensiones (k = `k95`, el número de PC con ≥95% de varianza que calcula P2 en el 2b), midiendo el tiempo.
- [ ] **3d.** Sammon con la misma semilla sobre el resultado de 3c, midiendo el tiempo.
- [ ] **3e.** Scatter 3D de la proyección de 3d.
- [ ] **3f.** Procrustes entre 3a y 3d con `scipy.spatial.procrustes`. Reportar la **disparidad** (0 = idénticas) y explicar qué significa.
- [ ] Calcular para la tabla 5a, tanto para Sammon como para Sammon sobre PCA: `stress_sammon(X_std, Z)` y `evaluar_knn(Z, y)`.
- [ ] Guardar el **tiempo total del 3a** en la variable `t_sammon_directo`, que P1 usa en la tabla del 3i.
- [ ] Exportar `sammon_3d.csv`, `sammon_pca_3d.csv`, `sammon_stress_iteraciones.csv`, `sammon_procrustes.csv` y las filas de Sammon y Sammon sobre PCA para `comparativa.csv`.
- [ ] Pasarle a P4 un párrafo corto con lo que observaste de Sammon (para el 5b).

---

### P4 — Sección 4 (autocodificador) y Sección 5 (análisis)

Referencias: https://ekamperi.github.io/machine%20learning/2021/01/21/encoder-decoder-model.html y https://www.kaggle.com/code/saivarunk/dimensionality-reduction-using-keras-auto-encoder

**Sección 4 — Autocodificador (30 pts)**
- [ ] Definir la entrada (ver pregunta pendiente sobre "datos originales"; mientras, usar `X_std` y justificarlo).
- [ ] Arquitectura **no lineal** sugerida: `30 → 16 → 8 → 3 → 8 → 16 → 30`, activaciones no lineales (ReLU o tanh) en capas ocultas, salida lineal. Justificar la arquitectura en el reporte.
- [ ] Fijar semillas con `tf.keras.utils.set_random_seed(SEED)`.
- [ ] Entrenar con `validation_split` y `EarlyStopping` (restaurando los mejores pesos). Graficar pérdida de entrenamiento y validación por época.
- [ ] Medir **por separado**: i) tiempo de **entrenamiento** y ii) tiempo de **proyección** con el codificador ya entrenado.
- [ ] Graficar el **espacio latente** en 3D con `COLORES_CLASE`.
- [ ] Calcular el **error de reconstrucción** (MSE en el mismo espacio que PCA), `stress_sammon(X_std, Z_ae)` y `evaluar_knn(Z_ae, y)`.
- [ ] Exportar `autoencoder_3d.csv`, `autoencoder_perdida.csv` y la fila del autocodificador para `comparativa.csv`.

**Sección 5 — Análisis y conclusiones (35 pts)**
- [ ] **Mientras llegan los resultados:** escribir el marco del análisis, es decir, qué se espera de un método lineal (PCA), de uno que preserva distancias (Sammon) y de uno no lineal (autocodificador).
- [ ] **5a.** Juntar en `comparativa.csv` las filas de todos en **una tabla única**: PCA, Sammon, Sammon sobre PCA y autocodificador × tiempo, stress de Sammon, exactitud k-NN y error de reconstrucción ("no aplica" donde corresponda). Revisar que todos hayan usado las funciones compartidas; si un número no cuadra, avisar a quien lo generó.
- [ ] **5b.** Pedir a cada quien un párrafo corto sobre lo que observó en su parte y escribir el contraste. Debe responder:
  - ¿Qué diferencias hay en los resultados (tiempo, stress, k-NN, reconstrucción)?
  - ¿Cómo ayuda cada técnica a ver patrones en 3D (separación de clases, forma de los grupos, traslape)?
  - ¿PCA lineal vs Sammon (preserva distancias) vs autocodificador (no lineal), qué gana y qué pierde cada uno?
  - ¿Qué método conviene para este dataset y por qué?
- [ ] **Ponerse de acuerdo con P2:** la conclusión del análisis y la del tablero tienen que decir lo mismo.
- [ ] Mantener un tono honesto: no exagerar diferencias pequeñas (por ejemplo, si la exactitud de k-NN difiere por menos de la desviación estándar, decirlo).

---

## 5. Dependencias y orden de trabajo

```
Fase 1 (bloqueante)
  P1: Sección 0 + funciones compartidas ──────┐
  P2: tabla 2b (k con ≥95% de varianza) ──────┤
  P3: función pca_mas_sammon(k) ──────────────┤
                                              ▼
Fase 2 (en paralelo)
  P1: Sección 1 + barrido 3g–3i (necesita la función de P3)    P2: resto de PCA + tablero con datos de prueba
  P3: Sammon 3a–3f (necesita k)                                P4: autocodificador + marco del análisis
                                              │
                                              ▼
Fase 3 (integración)
  Todos exportan CSV → P4 arma tabla 5a → P2 conecta el tablero a los CSV reales
  Todos le pasan a P4 su párrafo → P4 escribe el 5b → P4 y P2 alinean la conclusión
  Cada quien redacta su sección del reporte
                                              │
                                              ▼
Fase 4 (cierre)
  Restart & Run All del notebook en una sola máquina → revisión cruzada → checklist → comprimido
```

**Quién espera a quién:**

| Quién | Espera | De quién |
|---|---|---|
| Todos | Sección 0 y funciones compartidas | P1 |
| P3 | k con ≥95% de varianza (2b) | P2 |
| P1 (3g–3i) | `pca_mas_sammon(k)` y la función de Sammon adaptada | P3 |
| P1 (3i) | Tiempo total del 3a | P3 |
| P4 (5a y 5b) | Filas de `comparativa.csv` y un párrafo de cada quien | Todos |
| P2 (tablero final) | Todos los CSV | Todos |

**Reglas de trabajo en el repo:**
- **Solo una persona tiene el notebook a la vez.** Un `.ipynb` da conflictos muy difíciles de resolver en Git.
- Turno: avisar en el grupo → `git pull` → editar **solo la sección propia** → guardar → `git commit` y `git push` → avisar que se libera.
- Si hay un conflicto en el notebook, no resolverlo a mano: avisar al equipo y rehacer el cambio sobre la versión de `main`.
- La Sección 0 solo la modifica P1. Si alguien necesita cambiar una función compartida, avisa en el grupo antes de subir.

---

## 6. Advertencias técnicas

**Generales**
- ⚠️ Estandarizar **antes** de PCA, Sammon y k-NN. Sin estandarizar dominan las variables de área y perímetro.
- ⚠️ Tiempos: medir solo la transformación y mantener el mismo equipo para todas las mediciones. Si alguien corre en Colab y otro en su laptop, los tiempos **no son comparables**. Lo ideal es correr la versión final de todos en la misma máquina.
- ⚠️ El `StandardScaler` se ajusta con todo el dataset antes del k-NN. Para esta práctica es aceptable porque lo que se compara son proyecciones, pero mencionarlo en el reporte como limitación.
- ⚠️ Las imágenes de código no cuentan como evidencia. Todo debe estar ejecutado con salidas visibles.

**PCA (P2)**
- ⚠️ Para el 2b ajustar PCA con **todas** las componentes (no solo 3), si no la varianza acumulada sale incompleta.
- ⚠️ Los signos de los componentes son arbitrarios; si una gráfica sale "volteada" respecto a otra fuente, no es error.

**Sammon (P3 y P1)**
- ⚠️ La función de tompollard **no guarda el historial de stress por iteración** (regresa solo la proyección y el stress final). Copiarla a una celda del notebook, citar la fuente y agregar una lista que guarde el stress en cada iteración, con un comentario que lo explique.
- ⚠️ La **semilla fija solo influye si la inicialización es aleatoria**. La función usa PCA por defecto, que es determinista, y no fija la semilla por su cuenta. Como el PDF pide semilla fija, usar `init='random'` y llamar a `np.random.seed(SEED)` antes de cada corrida. **Explicarlo en el reporte.**
- ⚠️ Sammon divide entre las distancias originales: **puntos duplicados (distancia 0) rompen el algoritmo**. P1 ya revisa duplicados en la Sección 0.
- ⚠️ Sammon es O(n²) por iteración; con 569 puntos corre bien, pero el 3g son 5 corridas más. Dejarlo corriendo con tiempo.
- ⚠️ P3 y P1 deben usar **exactamente la misma función de Sammon, los mismos parámetros y la misma semilla**. Si no, el resultado del 3d (P3) y el de k = k95 en el barrido (P1) no van a coincidir y se nota en la presentación.
- ⚠️ **k = 3 en el barrido:** PCA ya deja los datos en 3D, así que el stress de la librería debe acercarse a 0 sin que eso signifique que el método sea mejor. El stress contra `X_std` es el que permite comparar.
- ⚠️ **k = 30 en el barrido:** PCA solo rota los datos, así que con la misma semilla debe dar prácticamente lo mismo que el 3a. Sirve de comprobación.
- ⚠️ Recordar la diferencia de stress (sección 3.6): el de la librería es respecto a su entrada; el de la tabla comparativa es respecto a `X_std` en 30D.

**Autocodificador (P4)**
- ⚠️ Aun con semilla fija, TensorFlow puede no ser 100% reproducible (sobre todo en GPU). Mencionarlo en el reporte.
- ⚠️ Si se entrena con datos sin escalar, la pérdida se dispara y el MSE no es comparable con PCA.
- ⚠️ Con pocos datos (569) es fácil sobreajustar: usar validación y EarlyStopping.
- ⚠️ **TensorFlow en Windows:** si `pip install` falla con `No such file or directory` dentro de `tensorflow\include`, la ruta es demasiado larga. Hay que activar las rutas largas de Windows o crear el entorno en una carpeta de ruta corta, y volver a instalar.

**Tablero (P2)**
- ⚠️ Una sola vista. Nada de pestañas ni decoración.
- ⚠️ Números solo desde los CSV de la práctica.
- ⚠️ Justificación: máximo 150 palabras y exactamente tres decisiones de diseño explicadas.

---

## 7. Preguntas pendientes para el profesor

| # | Duda | Plan si no contesta |
|---|---|---|
| 1 | **3h:** ¿el k-NN es sobre los datos reducidos con PCA a k dimensiones, o sobre la proyección de Sammon hecha a partir de cada k? | Hacer **las dos versiones** (es barato) y reportarlas en la tabla del 3i, aclarando cuál es cuál. |
| 2 | **Punto 4:** dice "datos originales", pero una red neuronal necesita datos escalados. ¿Podemos usar los estandarizados? | El PDF lo pone en negritas, así que conviene **preguntar pronto**. Usar `X_std` y justificarlo en el reporte (escala, convergencia y comparabilidad del MSE con PCA). Alternativa si exige los originales: darlos como entrada con una capa `Normalization` dentro del modelo. |

Responsable de preguntar: _(nombre)_ — Fecha en que se preguntó: _(fecha)_ — Respuesta: _(pendiente)_

---

## 8. Reporte

**Cada quien escribe la sección de lo que programó.** Antes de empezar, definan entre todos:
- Quién arma la portada, el índice, la introducción y las referencias.
- Quién junta las secciones en un solo documento y revisa la numeración de figuras y tablas.
- Quién hace el `Restart & Run All` final del notebook, en una sola máquina. Los tiempos del reporte se toman de esa corrida.
- Quién arma el comprimido final con el nombre correcto.

Cada quien también se encarga de la cabecera y los comentarios de sus celdas según ReglasEvaluación.

- Formal, **dividido por secciones**, con **todas las figuras y tablas numeradas y con título** (por ejemplo, "Figura 3. Varianza explicada y acumulada por componente principal").
- Cada sección incluye: **propósito → procedimiento → evidencia del resultado → interpretación breve**.
- Incluir el equipo de cómputo usado para medir tiempos.
- Estructura sugerida:
  1. Portada
  2. Índice
  3. Introducción y descripción del conjunto de datos
  4. Sección 1 — Visualización inicial y estandarización (P1)
  5. Sección 2 — PCA (P2)
  6. Sección 3 — Sammon (3a–3f: P3, 3g–3i: P1)
  7. Sección 4 — Autocodificador (P4)
  8. Sección 5 — Análisis y conclusiones (P4, con párrafos de todos)
  9. Sección 6 — Tablero y justificación del diseño (P2)
  10. Referencias

---

## 9. Estructura del repositorio

```
Practica02/
├── README.md
├── requirements.txt               # Dependencias
├── Practica02.ipynb               # Notebook único: Sección 0 (P1) y Secciones 1 a 6 (todos)
├── resultados/                    # CSV exportados
├── figuras/                       # imágenes numeradas para el reporte
├── tablero/                       # archivo del tablero e instrucciones
├── reporte/
└── temp/                          # archivos personales (no se sube al repositorio)
```

---

## 10. Checklist final antes de entregar

- [ ] El notebook corre con **Restart & Run All** sin errores y tiene las salidas guardadas.
- [ ] Todas las celdas tienen cabecera según ReglasEvaluación y comentarios relevantes.
- [ ] Mismos colores de clase en todas las figuras y en el tablero.
- [ ] Todas las figuras y tablas del reporte están numeradas y tienen título.
- [ ] Cada sección del reporte tiene propósito y evidencia.
- [ ] Los CSV usan "no aplica" y no 0 donde no corresponde, y `comparativa.csv` ya no dice `pendiente`.
- [ ] La tabla 5a está completa con los 4 métodos.
- [ ] La justificación del tablero tiene ≤150 palabras y tres decisiones de diseño.
- [ ] Se resolvieron (o se documentaron) las dos preguntas pendientes.
- [ ] Todos entienden los cuatro métodos (el profe elige quién contesta teoría).
- [ ] El comprimido es ZIP o RAR, incluye el reporte y tiene el nombre según ReglasEvaluación.
- [ ] Se entrega antes de la fecha y hora límite.
- [ ] Los 4 asistimos a la evaluación presencial.
