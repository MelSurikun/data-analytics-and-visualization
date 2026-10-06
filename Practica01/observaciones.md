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

  ## 4. Valores imposibles o extremos en CarDekho
- **Encontrada por:** Ricardo · **Fecha:** 04/10/2026
- **Afecta a:** incisos 15 y 24, nulos y validación de rangos (Santiago).
- **Observación:**
  - `seats` tiene 2 registros con valor 0 (Honda City y Nissan Kicks), lo cual es imposible.
  - `km_driven` tiene un máximo de 3,800,000 km en un Mahindra XUV500 de 5 años (unos 2,000 km por día) y otro registro con 1,325,000 km.
  - Por esos extremos, `km_driven` tiene un sesgo muy alto y casi no se correlaciona con el precio (−0.08).
- **Decisión:** se documenta en el EDA inicial y no se modifica. Se propone tratar `seats = 0` como nulo e imputarlo en el inciso 15, y definir en el inciso 24 un rango válido para `km_driven`. Pendiente de confirmar con Santiago.
- **Dónde está:** `Seccion_A_Ricardo.ipynb`, sección A.2 (estadísticos) y Figuras A.1 y A.3.

## 5. La clase `Electric` de CarDekho solo contiene Toyota Camry
- **Encontrada por:** Ricardo · **Fecha:** 04/10/2026
- **Afecta a:** incisos 11 a 14, filtros categóricos (Magaly), e inciso 26, codificación (Magaly).
- **Observación:** `fuel_type = Electric` tiene solo 4 registros (0.03 %) y los 4 son Toyota Camry, probablemente la versión híbrida. En las gráficas aparece como el combustible más caro, pero el promedio no es representativo.
- **Decisión:** se documenta. Se sugiere considerarla al filtrar o codificar, por ejemplo agrupándola con otra clase o excluyéndola, en lugar de tratarla como una categoría con peso propio.
- **Dónde está:** `Seccion_A_Ricardo.ipynb`, secciones A.2 (clases) y A.3 (Figura A.9).

## 6. UCI guarda puertas y cilindros como texto con palabras
- **Encontrada por:** Ricardo · **Fecha:** 04/10/2026
- **Afecta a:** incisos 21 y 22, conversión a numérico (Santiago).
- **Observación:** `num-of-doors` (`two`, `four`) y `num-of-cylinders` (`two` a `twelve`) son cuantitativas, pero el 100 % de sus valores son números escritos con palabras. `num-of-doors` además tiene 2 nulos.
- **Decisión:** en el EDA inicial se analizan por clase, sin calcular sus estadísticos. Deben convertirse a número con un diccionario de palabras (`two` → 2, `four` → 4, etc.) en el inciso 22.
- **Dónde está:** `Seccion_A_Ricardo.ipynb`, sección A.2 (texto y unidades), función `detectar_texto_cuantitativo` en `src/eda.py`.

## 7. Unidades de UCI convertidas a métrico y columnas `MPG_*` renombradas
- **Encontrada por:** Santiago · **Fecha:** 05/10/2026
- **Afecta a:** inciso 23 (Santiago) y a quien use el dataset transformado: incisos 25 a 27 y secciones F y G.
- **Observación:** CarDekho usa unidades métricas (km, km/l, cc) y UCI las de Estados Unidos (mpg, in³, pulgadas y libras). En el dataset limpio convivían las dos.
- **Decisión:** las unidades de CarDekho se toman como referencia y las dimensiones de UCI se **convierten**:
  - `MPG_Ciudad` y `MPG_Carretera`: de mpg a km/l (× 0.425144). Se **renombran** a `Millaje_Ciudad` y `Millaje_Carretera`, porque ya no están en millas por galón.
  - `Tamano_Motor`: de in³ a cc (× 16.387064).
  - `Altura`, `Ancho`, `Longitud`, `Distancia_Ejes`, `Diametro_Cilindro` y `Carrera_Piston`: de pulgadas a mm (× 25.4).
  - `Peso_Vacio`: de libras a kg (× 0.453592).
  - `Caballos_Fuerza` (hp) no se convierte: hp y bhp son la misma unidad.
  - `Precio` (USD) ya se había eliminado en el inciso 18, así que no hay monedas que unificar.
  - **Supuesto de la observación 3, comprobado:** la cilindrada calculada con el diámetro, la carrera y el número de cilindros coincide con `Tamano_Motor` (mediana de la razón: 1.00). Sí está en in³.
- **Dónde está:** `Seccion_E21-24_Santiago.ipynb`, sección E.23 · `data/processed/cardekho_transformado.csv`.

## 8. `Millaje` de los vehículos a gas está en km/kg
- **Encontrada por:** Santiago · **Fecha:** 05/10/2026
- **Afecta a:** inciso 23 (Santiago) y a las comparaciones de `Millaje` por combustible en las secciones G y H.
- **Observación:** según el diccionario de la Sección A, en los vehículos a gas (CNG y LPG) el rendimiento se publica en km/kg y no en km/l. Son 343 registros (2.25 %) del dataset limpio.
- **Decisión:** se **documenta y no se convierte**. Pasar de kilogramos a litros depende de la densidad del combustible, que no está en los datos. Al comparar `Millaje` conviene hacerlo por tipo de combustible.
- **Dónde está:** `Seccion_E21-24_Santiago.ipynb`, sección E.23.

## 9. Redondeo: valores que terminan en .5 y registros que quedan idénticos
- **Encontrada por:** Santiago · **Fecha:** 05/10/2026
- **Afecta a:** inciso 24 (Santiago), inciso 27 y Sección G (comprobación de duplicados y estadísticos).
- **Observación:**
  - `Millaje` tiene 715 valores que terminan exactamente en .5 y `Potencia_Máxima` tiene 1,092 (88.5 aparece 581 veces). Esos valores están a la misma distancia de dos enteros.
  - Después de redondear quedan 6 registros idénticos a otro. Antes solo se distinguían por los decimales de `Potencia_Máxima` (por ejemplo, 68.00 y 68.05).
- **Decisión:**
  - Se usa `round()` de pandas, que en esos casos elige el entero par (88.5 queda en 88 y 103.5 en 104). Así la media casi no cambia (`Potencia_Máxima`: de 100.608 a 100.611); la mediana pasa de 88.5 a 88.
  - Los 6 registros **no se eliminan**: eran distintos antes de redondear y la eliminación de duplicados corresponde al inciso 17. Si se vuelven a contar duplicados sobre el dataset transformado, `df.duplicated().sum()` da 6 por esta razón.
- **Dónde está:** `Seccion_E21-24_Santiago.ipynb`, sección E.24 y "Comprobación y exportación".

## 10. `Num_Puertas` y `Num_Cilindros` llegan como números (sobre la observación 6)
- **Encontrada por:** Santiago · **Fecha:** 05/10/2026
- **Afecta a:** incisos 21 y 22 (Santiago) y Sección A (Ricardo).
- **Observación:** con `hm.cargar_uci()`, `num-of-doors` llega como `float64` (2.0 y 4.0) y `num-of-cylinders` como `int64`. Así se promediaron por marca en la integración, y en el dataset limpio `Num_Puertas` y `Num_Cilindros` son numéricas.
- **Decisión:** en el inciso 22 no hay texto que convertir, por lo que el diccionario de palabras propuesto en la observación 6 no se aplica. Conviene confirmar con qué versión de UCI se generaron las Tablas A.11 a A.13, que las describen como texto.
- **Dónde está:** `Seccion_B_Melanie.ipynb`, sección B.4 (tipos de dato) · `Seccion_B9-10_C_Magaly.ipynb`, sección B.9.

## 11. Incisos 25 a 27 de la Sección E: transformación del precio y codificación
- **Encontrada por:** Melanie · **Fecha:** 06/10/2026
- **Afecta a:** incisos 25 a 27 (Melanie) y Sección G (Ricardo).
- **Observación:** el notebook de Santiago cubre los incisos 21 a 24. Los incisos 25 a 27 se hicieron en un notebook aparte.
- **Decisión:**
  - **Precio (25):** se conserva `Precio_Venta` (INR) y se agregan `Precio_Venta_Lakhs` (÷ 100,000) y `Precio_Venta_Log` (ln). El logaritmo baja la asimetría de 10.11 a 0.56.
  - **Codificación (26):**
    - binaria para `Transmisión` (`Transmision_Automatica`);
    - one-hot para `Combustible`, `Tipo_Vendedor` y las categóricas de UCI;
    - frecuencia para `Marca_Homologada` y `Modelo` (`*_Frec`).
  - Las columnas de texto originales **se conservan** para que la Sección G pueda graficarlas. El dataset pasa de 36 a 70 dimensiones.
  - Si en la G se calcula la correlación o el *pairplot* de "todas las cuantitativas", conviene excluir las columnas one-hot y las `*_Frec`, porque son códigos y no medidas.
- **Dónde está:** `Seccion_E25-27_Melanie.ipynb` · `src/caracteristicas.py` · `data/processed/cardekho_codificado.csv`.

## 12. No hay registros con `Kilómetros = 0`
- **Encontrada por:** Melanie · **Fecha:** 06/10/2026
- **Afecta a:** inciso 29 (Melanie).
- **Observación:** el mínimo de `Kilómetros` es 100 (un Hyundai Santro de 2020), así que no hay divisiones entre cero. Ese registro da el cuarto `Precio_por_Km` más alto (4,750 INR/km).
- **Decisión:** la regla queda programada de todos modos: si `Kilómetros = 0`, `Precio_por_Km` queda en NaN, y se demuestra con valores de prueba. No se usa infinito, porque rompe los estadísticos, ni 0, porque es un valor falso.
- **Dónde está:** `Seccion_F_Melanie.ipynb`, sección F.29 · `crear_precio_por_km` en `src/caracteristicas.py`.

## 13. Año de referencia de `Antigüedad` y umbral de `Vehiculo_Antiguo`
- **Encontrada por:** Melanie · **Fecha:** 06/10/2026
- **Afecta a:** incisos 28 y 30 (Melanie) y Sección G (Ricardo).
- **Observación:** el PDF pide fijar explícitamente el año de referencia y justificar el umbral.
- **Decisión:**
  - **Año de referencia: 2021** (`ANIO_REFERENCIA = ANIO_RECOLECCION`). Es el año del dataset y el mismo con el que se derivó `Año` (observación 1), así que `Antigüedad` coincide con la edad del auto al publicarse el anuncio.
  - **Umbral: 10 años.**
    - Es el percentil 90 de la antigüedad: 2,057 autos (13.49 %) quedan como antiguos.
    - En Delhi-NCR no pueden circular autos diésel de más de 10 años.
    - El precio mediano baja de 600,000 a 275,000 INR entre los dos grupos.
- **Dónde está:** `Seccion_F_Melanie.ipynb`, secciones F.28 y F.30 · constantes en `src/caracteristicas.py`.
