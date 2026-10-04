# Observaciones sobre los datos

En este archivo registramos los **hallazgos, diferencias con las instrucciones y decisiones** que vamos tomando sobre los datasets. Sirve para que todo el equipo esté enterado, para justificar las decisiones en el reporte y para preparar las preguntas de la evaluación presencial.

**Cómo agregar una observación:** copia el formato de abajo, ponle el siguiente número y anota quién la encontró, a qué incisos afecta y qué se decidió.

```markdown
## N. Título corto
- **Encontrada por:** Nombre · **Fecha:** dd/mm/aaaa
- **Afecta a:** incisos X, Y (persona responsable)
- **Observación:** qué encontramos en los datos.
- **Decisión:** qué hicimos y por qué.
- **Dónde está:** archivo / celda.
```

---

## 1. CarDekho no tiene la dimensión `year` (Año)
- **Encontrada por:** Melanie · **Fecha:** 03/10/2026
- **Afecta a:** inciso 6 (Melanie), filtros por año del inciso 11 (Magaly) y Antigüedad del inciso 28 (Melanie).
- **Observación:** el PDF menciona la dimensión "Año", pero la versión del dataset indicada por el profesor (`manishkr1754/cardekho-used-car-data`) no tiene `year`. En su lugar trae `vehicle_age`, la edad del vehículo en años.
- **Decisión:** se **deriva** `Año = 2021 − Edad_Vehiculo`.
  - **Supuesto:** se toma 2021 como año de recolección, por ser el año de publicación del dataset en Kaggle.
  - **Verificación:** un `assert` comprueba que `Año + Edad_Vehiculo = 2021` en todos los registros.
  - **Resultado:** Año va de 1992 a 2021.
  - Si el equipo decide otro año de referencia, basta con cambiar la constante `ANIO_RECOLECCION`.
- **Dónde está:** `src/homologacion.py` (`ANIO_RECOLECCION`, `crear_anio`) · `Seccion_B_Melanie.ipynb`, sección B.6.

## 2. CarDekho no tiene la dimensión `torque` (Torque)
- **Encontrada por:** Melanie · **Fecha:** 03/10/2026
- **Afecta a:** incisos 21, 22 y 24 (Santiago).
- **Observación:** el PDF pide limpiar y convertir "Torque", pero esta versión del dataset no la incluye. No puede calcularse a partir de otra dimensión y UCI Automobile tampoco la registra.
- **Decisión:** se **documenta su ausencia y no se imputa**. Inventar valores introduciría información fabricada. Los incisos 21–24 se aplican solo a `Millaje`, `Motor` y `Potencia_Máxima`.
- **Nota relacionada:** en esta versión, `mileage`, `engine` y `max_power` ya son numéricas (no traen "CC" ni "bhp" pegados). En los incisos 21–22 hay que demostrarlo con código (`dtypes`) en lugar de limpiar texto.
- **Dónde está:** `Seccion_B_Melanie.ipynb`, sección B.6.

## 3. Unidad de `engine-size` en UCI no documentada
- **Encontrada por:** Melanie · **Fecha:** 03/10/2026
- **Afecta a:** inciso 4 (Melanie) e inciso 23, unificación de unidades (Santiago).
- **Observación:** el repositorio UCI no indica en qué unidad está `engine-size`. Sus valores van de 61 a 326, mientras que el motor de CarDekho va de 793 a 6,592 cc.
- **Decisión:** se asume que `engine-size` está en **pulgadas cúbicas (in³)**.
  - **Justificación:** el rango es consistente con motores comunes medidos en in³, y la convención de la época en EE. UU. (1985) era usar esa unidad.
  - **Ejemplo:** 122 in³ × 16.387 = 2,000 cc, un motor típico de 2.0 L.
  - Si fueran cc, serían motores de 0.06 a 0.33 L, lo cual no es realista para coches.
  - **Conversión a cc:** `cc = in³ × 16.387`.
- **Dónde está:** `Seccion_B_Melanie.ipynb`, sección B.4 (tabla de correspondencias y comparación de escalas).
