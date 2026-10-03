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

Para maximizar la eficiencia y el trabajo en equipo, las secciones de la práctica fueron divididas según el siguiente esquema de trabajo:

| Persona | Secciones / Incisos Asignados | Resumen de Responsabilidades y Entregables |
| :--- | :--- | :--- |
| **Ricardo** | **A (1, 2, 3) + G (32, 33) + E (25)** | **EDA Inicial y Final + Transformación de Precio:**<br>• Carga, inspección general (top/bottom 10) y dimensiones cuantitativas/cualitativas.<br>• Métricas estadísticas (media, mediana, moda, std, IQR) y gráficos iniciales (*pairplot*, mapas de calor, distribuciones y comparativas contra `Precio_Venta`).<br>• Transformación adecuada de la variable `Precio_Venta` (Inciso 25).<br>• Reutilización de pipeline para el EDA Post-Procesamiento (Sección G) y análisis de variables generadas. |
| **Melanie** | **B (4 - 8) + F (28 - 31)** | **Homologación Pre-Integración e Ingeniería de Características:**<br>• Análisis de equivalencias e incompatibilidades entre `name` (CarDekho) y `make` (UCI).<br>• Renombrado a español y extracción de `Marca`.<br>• Creación de `Marca_Homologada` y construcción de `tabla_homologacion_marcas` con justificaciones.<br>• Creación y validación de variables numéricas/categóricas: `Antigüedad`, `Precio_por_Km` y `Vehiculo_Antiguo`. |
| **Magaly** | **B (9, 10) + C (11 - 14) + D (17, 18, 20) + E (26)** | **Integración, Filtrados, Deduplicación y Codificación:**<br>• Ejecución del *Left Join* tomando CarDekho como base y métricas del cruce.<br>• Aplicación de filtros simples (4+), combinados AND/OR/NOT (3+) y categóricos (3+), registrando métricas antes/después.<br>• Eliminación de duplicados post-integración, depuración de columnas innecesarias/redundantes y comprobaciones (Inciso 20).<br>• Codificación de variables categóricas (*One-Hot / Label Encoding*). |
| **Santiago** | **D (15, 16, 19) + E (21 - 24, 27)** | **Tratamiento de Nulos, Homologación Texto y Limpieza de Unidades:**<br>• Estrategia e imputación/eliminación de valores nulos (cuantitativos y cualitativos).<br>• Homologación de texto y categorías inconsistentes.<br>• Extracción de caracteres/unidades en `Millaje`, `Motor`, `Potencia_Máxima` y `Torque`.<br>• Conversión a tipos numéricos, unificación de unidades entre fuentes, redondeos y validación de rangos/nulos. |

---

## Estructura del Repositorio

```text
.
├── README.md                           # Documentación general y asignaciones (este archivo)
├── Prácticas_1_y_2_Analitica.ipynb     # Jupyter Notebook principal con la ejecución
├── data/
│   ├── raw/
│   │   ├── CarDekho.csv                # Dataset original 1
│   │   └── Automobile_UCI.csv          # Dataset original 2
│   └── processed/
│       ├── tabla_homologacion.csv      # Tabla de correspondencia de marcas
│       └── dataset_final_procesado.csv # Dataset resultante tras el pipeline completo
├── docs/
│   └── Reporte_Practica_1_y_2.pdf      # Reporte formal impreso/digital
└── src/                                # Scripts/módulos auxiliares de Python (opcional)
```

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
* **Nuevas características construidas:** `Antigüedad`, `Precio_por_Km`, `Vehiculo_Antiguo`.