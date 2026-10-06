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
| **Ricardo** | **G (32, 33)** | `Seccion_G_Ricardo.ipynb` | EDA final sobre `dataset_final_procesado.csv`, reutilizando las funciones de `src/eda.py`. |

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
├── data/
│   └── processed/                      # Resultado de cada etapa (los datos crudos se descargan por código)
│       ├── tabla_homologacion_marcas.csv # Inciso 8
│       ├── cardekho_integrado.csv      # Sección B (9–10)
│       ├── cardekho_limpio.csv         # Sección D
│       ├── cardekho_transformado.csv   # Sección E (21–24)
│       ├── cardekho_codificado.csv     # Sección E (25–27)
│       └── dataset_final_procesado.csv # Sección F: insumo de la Sección G
├── figuras/                            # Figuras generadas por los notebooks para el reporte
└── src/
    ├── homologacion.py                 # Funciones de la Sección B
    ├── eda.py                          # Funciones del EDA (Sección A; se reutilizan en la G)
    ├── caracteristicas.py              # Funciones de las Secciones E (25–26) y F
    ├── requirements.txt                # Dependencias
    └── COMO_EJECUTAR_ParteMelanie.md   # Guía para crear el entorno y ejecutar
```

Orden de ejecución: A → B → B9-10/C → D → E21-24 → E25-27 → F → G (cada notebook lee el CSV que deja el anterior).

> Los datasets **no** se suben al repositorio: CarDekho se descarga con `kagglehub` y UCI Automobile con `ucimlrepo` (ver `src/COMO_EJECUTAR_ParteMelanie.md`).

---

## Tecnologías y Librerías Utilizadas

* **Lenguaje:** Python 3.10+
* **Entorno:** Jupyter Notebook / JupyterLab
* **Procesamiento de Datos:** `pandas`, `numpy`
* **Visualización:** `matplotlib`, `seaborn`

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

3. **Instalar dependencias:**
   ```bash
   pip install pandas numpy matplotlib seaborn jupyter
   ```


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

*(Esta sección se completa al finalizar la ejecución global del proyecto)*
* **Registros finales retenidos:** `X,XXX` de `Y,YYY` iniciales.
* **Porcentaje de correspondencia en integración de marcas:** `XX.X%`
* **Nuevas características construidas:** `Antigüedad` (2021 − Año, de 0 a 29 años), `Precio_por_Km` (mediana de 11.82 INR/km) y `Vehiculo_Antiguo` (umbral de 10 años: 2,057 autos, 13.49 %).
