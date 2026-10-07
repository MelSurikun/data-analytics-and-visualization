# Prácticas 1 y 2: Análisis Exploratorio, Integración, Limpieza, Transformación e Ingeniería de Características

**Instituto Politécnico Nacional**  
**Escuela Superior de Cómputo (ESCOM)**  
**Asignatura:** Analítica y Visualización de Datos  
**Profesor:** Ituriel Enrique Flores Estrada  
**Semestre:** Septiembre 2026  

---

## Descripción del Proyecto
Este repositorio contiene el desarrollo colaborativo y el reporte de la **Práctica 1 y 2**, enfocada en el flujo completo de preparación y análisis de datos. A partir de los datasets de **CarDekho** y **UCI Machine Learning Repository - Automobile**, se lleva a cabo un proceso iterativo de:
* Análisis Exploratorio de Datos (EDA Inicial y Final)
* Integración y Homologación de Fuentes Heterogéneas
* Filtrado y Selección Criterial de Datos
* Limpieza e Imputación de Valores Faltantes/Duplicados
* Transformación de Variables y Unidades
* Ingeniería de Características (*Feature Engineering*)
* Comparación de Impacto Estadístico y Conclusiones

---

## Distribución del Trabajo y Asignación por Persona

Las secciones se dividieron así (cada notebook lleva el nombre de su responsable):

| Persona | Secciones / Incisos | Notebook | Resumen |
| :--- | :--- | :--- | :--- |
| **Ricardo** | **A (1 – 3)** | `Seccion_A_Ricardo.ipynb` | EDA inicial: descripción de dimensiones, top/bottom 10, nulos, clases, estadísticos y gráficas (distribuciones, *pairplot*, mapas de calor, categóricas vs. `Precio_Venta`). |
| **Melanie** | **B (4 – 8)** | `Seccion_B_Melanie.ipynb` | Correspondencia entre dimensiones, incompatibilidades `name`/`make`, renombrado a español, `Marca`, `Marca_Homologada` y `tabla_homologacion_marcas`. |
| **Magaly** | **B (9, 10) + C (11 – 14)** | `Seccion_B9-10_C_Magaly.ipynb` | *Left join* con CarDekho como base, métricas de la integración y filtros simples, combinados (AND/OR/NOT) y categóricos. |
| **Magaly** | **D (15 – 20)** | `Seccion_D_Magaly.ipynb` | Nulos, observaciones eliminadas, duplicados, dimensiones innecesarias, homologación de categorías y comprobación de la limpieza. |
| **Santiago** | **E (21 – 24)** | `Seccion_E21-24_Santiago.ipynb` | Caracteres y unidades de `Millaje`, `Motor` y `Potencia_Máxima`, conversión a numérico, unificación de unidades entre fuentes y redondeo. |
| **Melanie** | **E (25 – 27)** | `Seccion_E25-27_Melanie.ipynb` | Transformación de `Precio_Venta` (lakhs y logaritmo), codificación de categóricas (binaria, one-hot y frecuencia) y comprobación de la Sección E. |
| **Melanie** | **F (28 – 31)** | `Seccion_F_Melanie.ipynb` | Ingeniería de características: `Antigüedad`, `Precio_por_Km` y `Vehiculo_Antiguo`, con fórmula, procedimiento y ejemplos comprobados. |
| **Ricardo** | **G (32, 33)** | `Seccion_G_H_Ricardo.ipynb` | EDA final sobre `dataset_final_procesado.csv`, reutilizando las funciones de `src/eda.py`. |
| **Ricardo** | **H (34)** | `Seccion_G_H_Ricardo.ipynb` | Comparación del EDA inicial contra el final (observaciones, calidad, estadísticos, clases, forma del precio y correlaciones) y conclusiones. |

---

## Estructura del Repositorio

```text
Practica01/
├── README.md                           # Documentación general y asignaciones (este archivo)
├── observaciones.md                    # Hallazgos y decisiones sobre los datos (bitácora del equipo)
├── Seccion_A_Ricardo.ipynb             # Sección A (1–3): EDA inicial
├── Seccion_B_Melanie.ipynb             # Sección B (4–8): homologación de marcas
├── Seccion_B9-10_C_Magaly.ipynb        # Sección B (9–10) y C (11–14): integración y filtrado
├── Seccion_D_Magaly.ipynb              # Sección D (15–20): limpieza
├── Seccion_E21-24_Santiago.ipynb       # Sección E (21–24): unidades, tipos y redondeo
├── Seccion_E25-27_Melanie.ipynb        # Sección E (25–27): precio, codificación y comprobación
├── Seccion_F_Melanie.ipynb             # Sección F (28–31): ingeniería de características
├── Seccion_G_H_Ricardo.ipynb           # Secciones G (32–33) y H (34): EDA final y conclusiones
├── data/
│   └── processed/                      # Resultado de cada etapa (los datos crudos se descargan por código)
│       ├── tabla_homologacion_marcas.csv # Inciso 8
│       ├── cardekho_integrado.csv      # Sección B (9–10)
│       ├── cardekho_limpio.csv         # Sección D
│       ├── cardekho_transformado.csv   # Sección E (21–24)
│       ├── cardekho_codificado.csv     # Sección E (25–27)
│       └── dataset_final_procesado.csv # Sección F: insumo de la Sección G
├── figuras/                            # Figuras del reporte (figura_A*, B*, E*, F*, G*, H*)
└── src/
    ├── homologacion.py                 # Funciones de la Sección B
    ├── eda.py                          # Funciones del EDA (Sección A; se reutilizan en G y H)
    ├── caracteristicas.py              # Funciones de las Secciones E (25–26) y F
    ├── requirements.txt                # Dependencias
    └── COMO_EJECUTAR_ParteMelanie.md   # Guía para crear el entorno y ejecutar
```

Orden de ejecución: A → B → B9-10/C → D → E21-24 → E25-27 → F → G/H (cada notebook lee el CSV que deja el anterior). Los notebooks se abren desde la carpeta `Practica01/`, porque usan las rutas relativas `src/`, `data/processed/` y `figuras/`.

> Los datasets **no** se suben al repositorio: CarDekho se descarga con `kagglehub` y UCI Automobile con `ucimlrepo` (ver `src/COMO_EJECUTAR_ParteMelanie.md`).

---

## Tecnologías y Librerías Utilizadas

* **Lenguaje:** Python 3.10+
* **Entorno:** Jupyter Notebook / JupyterLab
* **Procesamiento de Datos:** `pandas`, `numpy`
* **Visualización:** `matplotlib`, `seaborn`
* **Descarga de datos:** `kagglehub` (CarDekho) y `ucimlrepo` (UCI Automobile)

---

## Guía de Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/MelSurikun/data-analytics-and-visualization.git 
   cd data-analytics-and-visualization
   ```

2. **Crear y activar un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   # venv\Scripts\activate   # En Windows
   ```

3. **Instalar dependencias** (desde la carpeta `Practica01/`):
   ```bash
   pip install -r src/requirements.txt
   ```

4. **Ejecutar los notebooks** en el orden indicado arriba. La primera ejecución requiere internet para descargar los datasets.


---

## Reglas de Evaluación y Lineamientos Formales (ESCOM IPN)

Para cumplir cabalmente con la rúbrica institucional publicada por el profesor **Ituriel Enrique Flores Estrada**:

1. **Cabecera de Código y Comentarios:** Cada bloque sintáctico debe contar con la cabecera estándar especificada en el documento de *Reglas de Evaluación*, indicando autor, fecha, descripción de la celda e insumo/resultado.
2. **Evidencia de Funcionamiento:** Todas las celdas del Jupyter Notebook deben estar **ejecutadas** con sus correspondientes salidas visibles (tablas, `info()`, *pairplots*, etc.).
3. **Formato de Entrega:** La entrega comprimida (`.zip` o `.rar`) debe seguir el estándar de nomenclatura oficial de la materia.
4. **Evaluación Presencial:**
   * **Reporte (33%):** Estructura formal, secciones numeradas, nombres de figuras, análisis comparativos.
   * **Teoría (34%):** Fundamentación de decisiones técnicas (imputación, join, codificación, etc.).
   * **Código (33%):** Calidad, modularidad y ejecución correcta en la revisión presencial.

---

## Resumen de Resultados Finales

* **Registros finales retenidos:** 15,244 de 15,411 iniciales (98.9 %). Solo se eliminaron los 167 anuncios duplicados.
* **Dimensiones:** de 14 a 73 (42 tras la integración, 36 tras la limpieza, 70 tras la codificación y 73 con las características nuevas). 32 de ellas son columnas codificadas (binarias, one-hot y de frecuencia).
* **Correspondencia en la integración de marcas:** 12 de 30 fabricantes (40.0 %), que abarcan el 29.4 % de los registros de CarDekho. La integración es un *left join* por `Marca_Homologada` con UCI resumido a un registro por fabricante (0 duplicados).
* **Nulos:** la integración generó 273,793 nulos en 11,433 registros; se trataron en la Sección D (mediana y "Desconocido") y el dataset final no tiene nulos.
* **Transformación del precio:** `Precio_Venta_Log` reduce la asimetría de 10.11 a 0.56 y eleva la correlación de `Antigüedad` con el precio de −0.24 a −0.49.
* **Nuevas características construidas:** `Antigüedad` (2021 − Año, de 0 a 29 años), `Precio_por_Km` (mediana de 11.82 INR/km) y `Vehiculo_Antiguo` (umbral de 10 años: 2,057 autos, 13.49 %; precio mediano de 275,000 INR contra 600,000 de los no antiguos).
* **Pendientes documentados:** 2 registros con `Asientos = 0`, un registro con 3,800,000 km, variantes de escritura en `Modelo` (RediGO / redi-GO) y 6 registros idénticos que dejó el redondeo del inciso 24.
