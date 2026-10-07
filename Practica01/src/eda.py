#  I.   Nombre completo del estudiante : Ricardo González Manzano
#  II.  Grupo                          : 5AV1
#  III. Carrera                        : Licenciatura en Ciencia de Datos
#  IV.  Fecha de última modificación   : 07/10/2026
# -----------------------------------------------------------------------------
#  V.   DESCRIPCIÓN DE LA FUNCIONALIDAD
#  Módulo con las funciones del Análisis Exploratorio de Datos (EDA). Solo
#  define constantes y funciones; no hace nada por sí mismo. Lo importan:
#    - Seccion_A_Ricardo.ipynb : EDA inicial (incisos 1, 2 y 3).
#    - Sección G               : EDA final sobre los datos ya procesados
#                                (incisos 32 y 33), con las mismas funciones.
#    - Sección H               : comparación del EDA inicial contra el final
#                                (inciso 34).
#  Las funciones cubren: diccionario de dimensiones, nulos, dimensiones
#  cuantitativas guardadas como texto o con unidades, inconsistencias en
#  dimensiones cualitativas, clases y frecuencias, estadística descriptiva y
#  gráficas (distribuciones, pairplot, mapa de calor y categorías contra el
#  precio). Para G y H agrega el análisis gráfico de las dimensiones nuevas
#  y las comparaciones antes/después (estadísticos, clases, etapas y
#  correlaciones). Ninguna función modifica el DataFrame que recibe. Las gráficas se
#  guardan como PNG en la carpeta indicada por CARPETA_FIGURAS.
# =============================================================================

import os    # Rutas y creación de carpetas
import re    # Expresiones regulares para revisar texto

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker  # Formato de los números en los ejes
import seaborn as sns


# ---------------------------------------------------------------------------
# Constantes de las gráficas
# ---------------------------------------------------------------------------
COLOR_PRINCIPAL = "#2a78d6"  # Azul: frecuencias, distribuciones y dispersión
COLOR_PRECIO = "#eb6834"     # Naranja: gráficas contra el precio y diagonal del pairplot
COLOR_TEXTO = "#52514e"      # Gris oscuro: líneas de referencia (media/mediana)

# Carpeta (relativa a Practica01) donde se guardan las figuras del reporte.
CARPETA_FIGURAS = "figuras"


def configurar_estilo():
    """Aplica el estilo común de todas las gráficas del EDA.

    Fondo claro y cuadrícula tenue para que destaquen los datos; títulos en
    negritas y etiquetas pequeñas para que quepan en las cuadrículas.
    Parámetros: ninguno.
    Regresa: None.
    """
    sns.set_theme(style="whitegrid", rc={
        "grid.color": "#e6e5e1", "axes.edgecolor": "#b9b8b3",
        "axes.titlesize": 11, "axes.titleweight": "bold", "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8,
    })


# ---------------------------------------------------------------------------
# Incisos 1 y 2: descripción de las dimensiones, nulos, texto cuantitativo,
# inconsistencias, clases y estadísticos
# ---------------------------------------------------------------------------
# Valores de texto que en la práctica significan "dato faltante" aunque
# pandas no los reconozca como nulos.
NULOS_OCULTOS = {"?", "", "na", "n/a", "nan", "null", "none", "-"}

# Números escritos con palabras (UCI guarda puertas y cilindros así).
PALABRAS_NUMERO = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                   "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                   "eleven": 11, "twelve": 12}

# Número seguido de una unidad o símbolo, por ejemplo "1197 CC", "18.9 kmpl", "90 bhp".
# ^\s*-?\d+([.,]\d+)?  -> número entero o decimal al inicio
# \s*[^\d\s.,-].*$     -> después viene algo que no es número (la unidad)
PATRON_NUMERO_CON_UNIDAD = re.compile(r"^\s*-?\d+(?:[.,]\d+)?\s*[^\d\s.,-].*$")


def describir_dimensiones(df, descripciones, renombrar):
    """Construye el diccionario de dimensiones de un dataset.

    Parámetros:
        df (DataFrame): dataset original, sin modificar.
        descripciones (dict): {columna: (descripción, representación, unidad)},
            escrito a partir de la documentación de cada fuente.
        renombrar (dict): {columna: nombre en español} (de homologacion.py).
    Regresa:
        DataFrame con una fila por dimensión. El tipo de dato, los valores
        distintos y el ejemplo se calculan de los datos, no se escriben a mano.
    """
    filas = []
    for col in df.columns:
        descripcion, representacion, unidad = descripciones[col]
        no_nulos = df[col].dropna()
        filas.append({
            "Dimensión original": col,
            "Nombre en español": renombrar.get(col, col),
            "Descripción": descripcion,
            "Representación": representacion,
            "Tipo de dato": str(df[col].dtype),   # int64, float64 o str
            "Unidad de medida": unidad,
            "Valores distintos": df[col].nunique(),
            "Ejemplo": no_nulos.iloc[0] if len(no_nulos) else None,
        })
    return pd.DataFrame(filas)


def columnas_por_representacion(diccionario, prefijo, como_texto=None):
    """Lista las dimensiones (en español) cuya representación empieza con "prefijo".

    Parámetros:
        diccionario (DataFrame): resultado de describir_dimensiones().
        prefijo (str): "Cuantitativa", "Cualitativa" o "Identificador".
        como_texto (bool o None): True -> solo las guardadas como texto;
            False -> solo las guardadas como número; None -> todas.
    Regresa:
        list[str] con los nombres en español, en el orden original.
    """
    mascara = diccionario["Representación"].str.startswith(prefijo)
    if como_texto is not None:
        es_texto = ~diccionario["Tipo de dato"].isin(["int64", "float64"])
        mascara &= es_texto if como_texto else ~es_texto
    return diccionario.loc[mascara, "Nombre en español"].tolist()


def resumen_nulos(df):
    """Total de observaciones, nulos y nulos ocultos de cada dimensión.

    Parámetros:
        df (DataFrame): dataset a revisar.
    Regresa:
        DataFrame con una fila por dimensión. "Nulos ocultos" cuenta textos
        como '?', '' o 'NA' que representan un faltante sin ser NaN.
    """
    total = len(df)
    nulos = df.isna().sum()
    ocultos = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            ocultos[col] = 0  # Una columna numérica no puede contener texto
        else:
            texto = df[col].dropna().astype(str).str.strip().str.lower()
            ocultos[col] = int(texto.isin(NULOS_OCULTOS).sum())
    tabla = pd.DataFrame({
        "Total de observaciones": total,
        "No nulos": total - nulos,
        "Nulos": nulos,
        "% nulos": nulos / total * 100,
        "Nulos ocultos": pd.Series(ocultos),
    })
    return tabla.rename_axis("Dimensión")


def detectar_texto_cuantitativo(df):
    """Revisa si cada dimensión guarda números como texto o con unidades.

    Para cada columna de texto calcula el porcentaje de valores (no nulos) que:
      - se convierten directamente a número ("3", "4.5");
      - son números escritos con palabras ("two", "four");
      - son un número seguido de una unidad o símbolo ("1197 CC", "90 bhp").
    Parámetros:
        df (DataFrame): dataset a revisar.
    Regresa:
        DataFrame con los porcentajes y un diagnóstico por dimensión.
    """
    filas = []
    for col in df.columns:
        serie = df[col].dropna()
        if pd.api.types.is_numeric_dtype(serie):
            filas.append({"Dimensión": col, "Tipo de dato": str(df[col].dtype),
                          "% número directo": 100.0, "% número en palabras": 0.0,
                          "% número con unidad": 0.0, "Ejemplos": "",
                          "Diagnóstico": "Numérica: sin unidades ni caracteres adicionales"})
            continue
        texto = serie.astype(str).str.strip()
        # errors="coerce" convierte en NaN lo que no es número; notna() marca los que sí lo son.
        pct_num = pd.to_numeric(texto, errors="coerce").notna().mean() * 100
        pct_pal = texto.str.lower().isin(PALABRAS_NUMERO).mean() * 100
        pct_uni = texto.str.match(PATRON_NUMERO_CON_UNIDAD).mean() * 100
        if pct_num + pct_pal >= 90:
            forma = "con palabras" if pct_pal > pct_num else "con dígitos"
            diagnostico = f"Cuantitativa guardada como texto ({forma})"
        elif pct_uni >= 50:
            diagnostico = "Cuantitativa con unidades o caracteres adicionales"
        else:
            diagnostico = "Cualitativa: texto propio de la categoría"
        filas.append({"Dimensión": col, "Tipo de dato": str(df[col].dtype),
                      "% número directo": pct_num, "% número en palabras": pct_pal,
                      "% número con unidad": pct_uni,
                      "Ejemplos": ", ".join(texto.unique()[:4]),
                      "Diagnóstico": diagnostico})
    return pd.DataFrame(filas).set_index("Dimensión")


def inconsistencias_cualitativas(df, columnas):
    """Busca problemas de representación en dimensiones cualitativas.

    Revisa cuatro casos:
      1. Clases con espacios al inicio o al final, o con espacios dobles.
      2. Clases que solo difieren en mayúsculas/minúsculas ("ISUZU" vs "Isuzu").
      3. Clases que solo difieren en separadores ("RediGO" vs "redi-GO").
      4. Clases cuyo texto completo es el inicio de otra clase ("CR" y "CR-V"):
         posibles nombres truncados o versiones del mismo concepto.
    Parámetros:
        df (DataFrame): dataset a revisar.
        columnas (list): dimensiones cualitativas guardadas como texto.
    Regresa:
        DataFrame con una fila por dimensión y los hallazgos de cada caso.
    """
    filas = []
    for col in columnas:
        clases = pd.Series(df[col].dropna().astype(str).unique())
        # Caso 1: espacios innecesarios.
        espacios = clases[(clases != clases.str.strip()) | clases.str.contains("  ")]
        # Caso 2: se agrupan las clases por su versión en minúsculas; si un
        # grupo tiene más de una clase, esas clases solo difieren en mayúsculas.
        minus = clases.str.strip().str.lower()
        grupos_may = [" / ".join(g) for _, g in clases.groupby(minus) if len(g) > 1]
        # Caso 3: además se quitan guiones, guiones bajos y espacios.
        clave = minus.str.replace(r"[-_\s]+", "", regex=True)
        grupos_sep = [" / ".join(g) for _, g in clases.groupby(clave)
                      if len(g) > 1 and g.str.lower().nunique() > 1]
        # Caso 4: se compara cada par de clases normalizadas; si una es el
        # comienzo exacto de la otra (y no son iguales) se reporta el par.
        unicas = dict(zip(clave, clases))  # clave normalizada -> texto original
        prefijos = [f"{unicas[a]} ⊂ {unicas[b]}"
                    for a in unicas for b in unicas
                    if a != b and len(a) >= 2 and b.startswith(a)]
        filas.append({
            "Dimensión": col,
            "Clases": len(clases),
            "Con espacios innecesarios": ", ".join(espacios) or "—",
            "Difieren solo en mayúsculas": "; ".join(grupos_may) or "—",
            "Difieren en separadores": "; ".join(grupos_sep) or "—",
            "Una clase es el inicio de otra": "; ".join(sorted(prefijos)) or "—",
        })
    return pd.DataFrame(filas).set_index("Dimensión")


def distribucion_clases(serie):
    """Frecuencia y porcentaje de cada clase de una dimensión.

    Parámetros:
        serie (Series): dimensión cualitativa (o discreta) a contar.
    Regresa:
        DataFrame ordenado de mayor a menor frecuencia. Los nulos aparecen
        como la clase "(nulo)" para no ocultarlos. El porcentaje se calcula
        sobre el total de observaciones.
    """
    conteo = serie.value_counts(dropna=False)
    conteo.index = conteo.index.map(lambda v: "(nulo)" if pd.isna(v) else v)
    return pd.DataFrame({"Observaciones": conteo,
                         "% del total": conteo / len(serie) * 100}).rename_axis(serie.name)


def estadisticos_cuantitativos(df, columnas):
    """Medidas descriptivas de las dimensiones cuantitativas (sin contar nulos).

    Parámetros:
        df (DataFrame): dataset.
        columnas (list): dimensiones cuantitativas guardadas como número.
    Regresa:
        DataFrame con media, mediana, moda, desviación estándar, varianza,
        mínimo, máximo, rango, cuartiles y rango intercuartílico (IQR).
    """
    filas = []
    for col in columnas:
        s = df[col].dropna()
        modas = s.mode()  # Puede haber más de una moda; se reporta la primera y cuántas hay
        q1, q2, q3 = s.quantile([0.25, 0.50, 0.75])
        filas.append({
            "Dimensión": col, "Observaciones": s.count(),
            "Media": s.mean(), "Mediana": s.median(),
            "Moda": modas.iloc[0], "N.º de modas": len(modas),
            "Desv. estándar": s.std(), "Varianza": s.var(),  # Muestrales (ddof=1)
            "Mínimo": s.min(), "Máximo": s.max(), "Rango": s.max() - s.min(),
            "Q1 (25 %)": q1, "Q2 (50 %)": q2, "Q3 (75 %)": q3, "IQR": q3 - q1,
        })
    return pd.DataFrame(filas).set_index("Dimensión")


# ---------------------------------------------------------------------------
# Inciso 3: gráficas (cada una se guarda en CARPETA_FIGURAS)
# ---------------------------------------------------------------------------
def formato_compacto(valor, _posicion=None):
    """Escribe números grandes de forma corta para los ejes (2,500,000 -> "2.5 M").

    Parámetros:
        valor (float): número a escribir.
        _posicion: posición de la marca en el eje (la pide matplotlib; no se usa).
    Regresa:
        str con el número abreviado (k = miles, M = millones).
    """
    if abs(valor) >= 1e6:
        return f"{valor / 1e6:g} M"
    if abs(valor) >= 1e4:
        return f"{valor / 1e3:g} k"
    return f"{valor:,.0f}" if abs(valor) >= 1000 else f"{valor:g}"


def guardar_figura(fig, nombre_archivo):
    """Guarda una figura en la carpeta de figuras del reporte.

    Parámetros:
        fig (Figure): figura de matplotlib.
        nombre_archivo (str): nombre del PNG, por ejemplo "figura_A1_x.png".
    Regresa:
        str con la ruta donde quedó guardada.
    """
    os.makedirs(CARPETA_FIGURAS, exist_ok=True)  # Por si la carpeta aún no existe
    ruta = os.path.join(CARPETA_FIGURAS, nombre_archivo)
    fig.savefig(ruta, dpi=150, bbox_inches="tight")  # "tight" evita que se corten etiquetas
    return ruta


def crear_mosaico(columnas, n_clases, umbral=12, alto_ancha=4.2, alto_angosta=3.4):
    """Acomoda una subgráfica por dimensión según su número de clases.

    Las dimensiones con más de "umbral" clases ocupan un renglón completo
    (necesitan espacio para sus etiquetas); las demás se acomodan de tres en tres.
    Parámetros:
        columnas (list): dimensiones a graficar.
        n_clases (dict): {dimensión: número de barras que tendrá}.
        umbral (int): número de clases a partir del cual va a todo lo ancho.
        alto_ancha, alto_angosta (float): alto en pulgadas de cada tipo de renglón.
    Regresa:
        tuple (Figure, dict {dimensión: Axes}).
    """
    anchas = [c for c in columnas if n_clases[c] > umbral]
    angostas = [c for c in columnas if n_clases[c] <= umbral]
    mosaico = [[c, c, c] for c in anchas]
    for i in range(0, len(angostas), 3):
        fila = angostas[i:i + 3]
        mosaico.append(fila + ["."] * (3 - len(fila)))  # "." deja el hueco vacío
    alturas = [alto_ancha] * len(anchas) + [alto_angosta] * (len(mosaico) - len(anchas))
    fig, ejes = plt.subplot_mosaic(mosaico, figsize=(16, sum(alturas)),
                                   gridspec_kw={"height_ratios": alturas})
    return fig, ejes


def graficar_distribuciones_cuantitativas(df, columnas, unidades, titulo, archivo):
    """Histograma con curva de densidad (KDE) de cada dimensión cuantitativa.

    Las líneas punteadas marcan la media (--) y la mediana (:); si están
    separadas, la distribución es asimétrica.
    Parámetros:
        df (DataFrame), columnas (list): datos y dimensiones a graficar.
        unidades (dict): {dimensión: unidad} para el eje X.
        titulo (str), archivo (str): título general y nombre del PNG.
    Regresa:
        Figure de matplotlib.
    """
    ncols = 3
    nfilas = int(np.ceil(len(columnas) / ncols))
    fig, ejes = plt.subplots(nfilas, ncols, figsize=(16, 3.6 * nfilas))
    ejes = np.atleast_1d(ejes).ravel()  # Arreglo plano para recorrerlo con zip
    for eje, col in zip(ejes, columnas):
        datos = df[col].dropna()
        # Discreta = enteros en un rango corto (p. ej. años o asientos): una barra por valor.
        # RPM_Maximas tiene pocos valores, pero separados por cientos: se trata como continua.
        discreta = bool((datos % 1 == 0).all() and datos.max() - datos.min() <= 30)
        sns.histplot(datos, ax=eje, kde=not discreta, discrete=discreta,
                     bins="auto" if discreta else 40, color=COLOR_PRINCIPAL,
                     edgecolor="white", linewidth=0.4)
        eje.axvline(datos.mean(), color=COLOR_TEXTO, ls="--", lw=1.2, label="Media")
        eje.axvline(datos.median(), color=COLOR_TEXTO, ls=":", lw=1.6, label="Mediana")
        eje.set_title(col)
        eje.set_xlabel(unidades.get(col, ""))
        eje.set_ylabel("Frecuencia")
        eje.xaxis.set_major_formatter(mticker.FuncFormatter(formato_compacto))
    for eje in ejes[len(columnas):]:
        eje.set_visible(False)  # Oculta los espacios sobrantes de la cuadrícula
    ejes[0].legend(fontsize=8)
    fig.suptitle(titulo, fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    guardar_figura(fig, archivo)
    return fig


def graficar_pairplot(df, columnas, titulo, archivo, altura=2.0,
                      color_puntos=COLOR_PRINCIPAL, color_diagonal=COLOR_PRECIO):
    """Pairplot: dispersión entre cada par de dimensiones cuantitativas.

    Se usan dos colores para distinguir los tipos de gráfica: los diagramas
    de dispersión (fuera de la diagonal) y los histogramas de la diagonal.
    Parámetros:
        df (DataFrame), columnas (list): datos y dimensiones a comparar.
        titulo (str), archivo (str): título y nombre del PNG.
        altura (float): tamaño en pulgadas de cada subgráfica.
        color_puntos (str): color de los diagramas de dispersión.
        color_diagonal (str): color de los histogramas de la diagonal.
    Regresa:
        PairGrid de seaborn.
    """
    rejilla = sns.pairplot(df[columnas], height=altura, diag_kind="hist",
                           plot_kws={"s": 9, "alpha": 0.35, "color": color_puntos,
                                     "edgecolor": "none"},
                           diag_kws={"color": color_diagonal, "edgecolor": "none", "bins": 30})
    # Números grandes abreviados (k, M) en lugar de notación científica (1e6).
    for eje in rejilla.axes.flat:
        eje.xaxis.set_major_formatter(mticker.FuncFormatter(formato_compacto))
        eje.yaxis.set_major_formatter(mticker.FuncFormatter(formato_compacto))
    rejilla.figure.suptitle(titulo, y=1.01, fontsize=14, fontweight="bold")
    guardar_figura(rejilla.figure, archivo)
    return rejilla


def graficar_mapa_calor(df, columnas, titulo, archivo):
    """Mapa de calor de la correlación de Pearson entre dimensiones cuantitativas.

    Solo se dibuja el triángulo inferior porque la matriz es simétrica.
    Rojo = correlación positiva, azul = negativa, blanco = sin correlación.
    Parámetros:
        df (DataFrame), columnas (list): datos y dimensiones.
        titulo (str), archivo (str): título y nombre del PNG.
    Regresa:
        DataFrame con la matriz de correlación completa.
    """
    corr = df[columnas].corr(method="pearson")
    mascara = np.triu(np.ones_like(corr, dtype=bool), k=1)  # True = celda oculta
    lado = max(7, 0.62 * len(columnas) + 2)
    fig, eje = plt.subplots(figsize=(lado, lado * 0.82))
    sns.heatmap(corr, mask=mascara, annot=True, fmt=".2f", cmap="RdBu_r",
                vmin=-1, vmax=1, center=0, square=True, linewidths=0.6,
                linecolor="white", annot_kws={"size": 8}, ax=eje,
                cbar_kws={"shrink": 0.7, "label": "Coeficiente de correlación de Pearson"})
    eje.set_title(titulo, fontsize=13, fontweight="bold", pad=12)
    fig.tight_layout()
    guardar_figura(fig, archivo)
    return corr


def graficar_distribuciones_cualitativas(df, columnas, titulo, archivo, max_clases=30):
    """Barras con la frecuencia de cada clase de las dimensiones cualitativas.

    Si una dimensión tiene más de "max_clases" clases, se grafican las más
    frecuentes y el resto se agrupa en una barra "Otras (k clases)".
    Parámetros:
        df (DataFrame), columnas (list): datos y dimensiones.
        titulo (str), archivo (str): título y nombre del PNG.
        max_clases (int): número máximo de barras individuales.
    Regresa:
        Figure de matplotlib.
    """
    conteos = {}
    for col in columnas:
        conteo = df[col].astype("string").fillna("(nulo)").value_counts()
        if len(conteo) > max_clases:
            resto = conteo.iloc[max_clases:]
            conteo = pd.concat([conteo.iloc[:max_clases],
                                pd.Series({f"Otras ({len(resto)} clases)": resto.sum()})])
        conteos[col] = conteo
    fig, ejes = crear_mosaico(columnas, {c: len(v) for c, v in conteos.items()})
    for col, conteo in conteos.items():
        eje = ejes[col]
        etiquetas = [str(v) for v in conteo.index]
        eje.bar(range(len(conteo)), conteo.values, color=COLOR_PRINCIPAL, width=0.75)
        eje.set_xticks(range(len(conteo)))
        muchas = len(conteo) > 6
        eje.set_xticklabels(etiquetas, rotation=60 if muchas else 0, ha="right" if muchas else "center")
        if len(conteo) <= 12:  # Con pocas barras se escribe el porcentaje encima
            pct = conteo.values / len(df) * 100
            for x, (v, p) in enumerate(zip(conteo.values, pct)):
                eje.text(x, v, f"{p:.1f} %", ha="center", va="bottom", fontsize=8, color=COLOR_TEXTO)
            eje.margins(y=0.15)
        eje.set_title(f"{col} ({df[col].nunique()} clases)")
        eje.set_ylabel("Observaciones")
        eje.yaxis.set_major_formatter(mticker.FuncFormatter(formato_compacto))
    fig.suptitle(titulo, fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.985))  # Deja espacio al título general
    guardar_figura(fig, archivo)
    return fig


def precio_por_categoria(df, categoria, precio):
    """Agrupa las observaciones por categoría y ordena por precio promedio.

    Parámetros:
        df (DataFrame): dataset.
        categoria (str): dimensión categórica (eje X).
        precio (str): dimensión de precio (eje Y).
    Regresa:
        DataFrame con observaciones, precio promedio y precio mediano por
        categoría, de mayor a menor precio promedio. Los nulos de precio se
        excluyen del promedio.
    """
    tabla = (df.groupby(categoria)[precio]
               .agg(Observaciones="count", **{"Precio promedio": "mean",
                                                "Precio mediano": "median"})
               .sort_values("Precio promedio", ascending=False))
    return tabla


def graficar_categorias_vs_precio(df, columnas, precio, unidad_precio, titulo, archivo, max_clases=30):
    """Barras del precio promedio por categoría, de mayor a menor.

    Eje X: clases de la dimensión categórica; eje Y: precio promedio.
    Si hay más de "max_clases" clases, se muestran las "max_clases" más caras.
    Parámetros:
        df (DataFrame), columnas (list), precio (str): datos, categóricas y precio.
        unidad_precio (str): unidad para el eje Y (p. ej. "INR").
        titulo (str), archivo (str): título y nombre del PNG.
        max_clases (int): número máximo de barras por dimensión.
    Regresa:
        Figure de matplotlib.
    """
    tablas = {c: precio_por_categoria(df, c, precio)["Precio promedio"] for c in columnas}
    fig, ejes = crear_mosaico(columnas, {c: min(len(t), max_clases) for c, t in tablas.items()})
    for col, serie in tablas.items():
        total = len(serie)
        serie = serie.iloc[:max_clases]
        eje = ejes[col]
        eje.bar(range(len(serie)), serie.values, color=COLOR_PRECIO, width=0.75)
        eje.set_xticks(range(len(serie)))
        muchas = len(serie) > 6
        eje.set_xticklabels([str(v) for v in serie.index], rotation=60 if muchas else 0,
                            ha="right" if muchas else "center")
        sufijo = f" — {max_clases} más caras de {total}" if total > max_clases else ""
        eje.set_title(f"{col}{sufijo}")
        eje.set_ylabel(f"{precio} promedio ({unidad_precio})")
        eje.yaxis.set_major_formatter(mticker.FuncFormatter(formato_compacto))
    fig.suptitle(titulo, fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.985))  # Deja espacio al título general
    guardar_figura(fig, archivo)
    return fig


# ---------------------------------------------------------------------------
# Inciso 33: análisis gráfico de las dimensiones nuevas (Sección G)
# ---------------------------------------------------------------------------
def graficar_nuevas_caracteristicas(df, titulo, archivo, umbral=10):
    """Análisis gráfico de Antigüedad, Precio_por_Km y Vehiculo_Antiguo.

    Cuatro paneles:
      (a) distribución de Antigüedad, con las barras de los vehículos antiguos
          (Antigüedad >= umbral) en otro color y una línea en el umbral;
      (b) Precio_Venta mediano por cada año de Antigüedad;
      (c) distribución de Precio_por_Km en escala logarítmica, con su mediana;
      (d) caja de Precio_Venta (escala log) para cada grupo de Vehiculo_Antiguo.
    Parámetros:
        df (DataFrame): dataset con Antigüedad, Precio_por_Km, Vehiculo_Antiguo
            y Precio_Venta.
        titulo (str), archivo (str): título general y nombre del PNG.
        umbral (int): años a partir de los cuales un vehículo es antiguo.
    Regresa:
        Figure de matplotlib.
    """
    fig, ejes = plt.subplots(2, 2, figsize=(15, 9.5))
    (eje_a, eje_b), (eje_c, eje_d) = ejes

    # (a) Distribución de Antigüedad: una barra por año.
    conteo = df["Antigüedad"].value_counts().sort_index()
    colores = [COLOR_PRECIO if anios >= umbral else COLOR_PRINCIPAL for anios in conteo.index]
    eje_a.bar(conteo.index, conteo.values, color=colores, width=0.8)
    eje_a.axvline(umbral - 0.5, color=COLOR_TEXTO, ls="--", lw=1.2)
    eje_a.text(umbral - 0.4, conteo.max() * 0.92, f"Umbral: {umbral} años",
               fontsize=9, color=COLOR_TEXTO)
    eje_a.set_title("(a) Distribución de Antigüedad")
    eje_a.set_xlabel("años")
    eje_a.set_ylabel("Vehículos")

    # (b) Precio mediano por año de antigüedad.
    mediana = df.groupby("Antigüedad")["Precio_Venta"].median()
    eje_b.plot(mediana.index, mediana.values, marker="o", ms=4, lw=2, color=COLOR_PRINCIPAL)
    eje_b.set_title("(b) Precio_Venta mediano por Antigüedad")
    eje_b.set_xlabel("años")
    eje_b.set_ylabel("Precio_Venta mediano (INR)")
    eje_b.yaxis.set_major_formatter(mticker.FuncFormatter(formato_compacto))

    # (c) Precio_por_Km en escala log: con escala lineal todo quedaría en la primera barra.
    ppk = df["Precio_por_Km"].dropna()
    ppk = ppk[ppk > 0]  # El logaritmo solo existe para valores positivos
    bins = np.logspace(np.log10(ppk.min()), np.log10(ppk.max()), 50)
    eje_c.hist(ppk, bins=bins, color=COLOR_PRINCIPAL, edgecolor="white", linewidth=0.4)
    eje_c.set_xscale("log")
    eje_c.axvline(ppk.median(), color=COLOR_TEXTO, ls=":", lw=1.6,
                  label=f"Mediana: {ppk.median():.2f}")
    eje_c.legend(fontsize=8)
    eje_c.set_title("(c) Distribución de Precio_por_Km (escala log)")
    eje_c.set_xlabel("INR por km")
    eje_c.set_ylabel("Vehículos")

    # (d) Precio por grupo de Vehiculo_Antiguo.
    grupos = [df.loc[df["Vehiculo_Antiguo"] == g, "Precio_Venta"].dropna() for g in (0, 1)]
    cajas = eje_d.boxplot(grupos, widths=0.5, patch_artist=True,
                          medianprops={"color": COLOR_TEXTO},
                          flierprops={"marker": "o", "markersize": 2, "alpha": 0.3})
    for caja, color in zip(cajas["boxes"], (COLOR_PRINCIPAL, COLOR_PRECIO)):
        caja.set_facecolor(color)
        caja.set_alpha(0.75)
    eje_d.set_xticks([1, 2])
    eje_d.set_xticklabels([f"No antiguo (0)\nn = {len(grupos[0]):,}",
                           f"Antiguo (1)\nn = {len(grupos[1]):,}"])
    eje_d.set_yscale("log")
    eje_d.yaxis.set_major_formatter(mticker.FuncFormatter(formato_compacto))
    eje_d.set_title("(d) Precio_Venta según Vehiculo_Antiguo")
    eje_d.set_ylabel("Precio_Venta (INR, escala log)")

    fig.suptitle(titulo, fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    guardar_figura(fig, archivo)
    return fig


# ---------------------------------------------------------------------------
# Inciso 34: comparación del EDA inicial contra el final (Sección H)
# ---------------------------------------------------------------------------
MEDIDAS_COMPARACION = ["Observaciones", "Media", "Mediana", "Desv. estándar", "Mínimo", "Máximo"]


def comparar_estadisticos(est_antes, est_despues, pares, medidas=None):
    """Compara medidas descriptivas de las mismas dimensiones antes y después.

    Parámetros:
        est_antes, est_despues (DataFrame): tablas de estadisticos_cuantitativos.
        pares (list): tuplas (dimensión antes, dimensión después). Si los nombres
            difieren, la fila se rotula "antes → después".
        medidas (list): medidas a comparar (por omisión MEDIDAS_COMPARACION).
    Regresa:
        DataFrame con índice (Dimensión, Medida) y columnas Antes, Después,
        Diferencia y Cambio %. El cambio % queda NaN cuando el valor de antes
        es 0, porque no se puede dividir entre cero.
    """
    medidas = MEDIDAS_COMPARACION if medidas is None else medidas
    filas = []
    for antes, despues in pares:
        etiqueta = antes if antes == despues else f"{antes} → {despues}"
        for medida in medidas:
            v_antes = float(est_antes.loc[antes, medida])
            v_despues = float(est_despues.loc[despues, medida])
            filas.append({"Dimensión": etiqueta, "Medida": medida,
                          "Antes": v_antes, "Después": v_despues,
                          "Diferencia": v_despues - v_antes,
                          "Cambio %": (v_despues - v_antes) / abs(v_antes) * 100
                                      if v_antes != 0 else np.nan})
    return pd.DataFrame(filas).set_index(["Dimensión", "Medida"])


def comparar_clases(antes, despues):
    """Observaciones y porcentaje de cada clase antes y después.

    Parámetros:
        antes, despues (Series): la misma dimensión cualitativa en dos momentos.
            El nombre de la tabla se toma de "despues".
    Regresa:
        DataFrame con Obs. antes, % antes, Obs. después, % después y
        Diferencia (pp), en puntos porcentuales. Incluye las clases que solo
        existen en uno de los dos momentos (con 0 en el otro) y se ordena de
        mayor a menor por observaciones después y luego antes.
    """
    conteo_antes = antes.value_counts()
    conteo_despues = despues.value_counts()
    tabla = pd.DataFrame({"Obs. antes": conteo_antes,
                          "Obs. después": conteo_despues}).fillna(0).astype("int64")
    tabla["% antes"] = tabla["Obs. antes"] / len(antes) * 100
    tabla["% después"] = tabla["Obs. después"] / len(despues) * 100
    tabla["Diferencia (pp)"] = tabla["% después"] - tabla["% antes"]
    tabla = tabla.sort_values(["Obs. después", "Obs. antes"], ascending=False)
    tabla = tabla[["Obs. antes", "% antes", "Obs. después", "% después", "Diferencia (pp)"]]
    return tabla.rename_axis(despues.name)


def graficar_etapas(tabla, titulo, archivo):
    """Barras con las observaciones y las dimensiones del dataset en cada etapa.

    Parámetros:
        tabla (DataFrame): índice = etapa; columnas "Observaciones" y "Dimensiones".
        titulo (str), archivo (str): título general y nombre del PNG.
    Regresa:
        Figure de matplotlib.
    """
    fig, ejes = plt.subplots(1, 2, figsize=(15, 4.8))
    for eje, col, color in zip(ejes, ["Observaciones", "Dimensiones"], [COLOR_PRINCIPAL, COLOR_PRECIO]):
        valores = tabla[col]
        x = range(len(valores))
        eje.bar(x, valores.values, color=color, width=0.65)
        for xi, v in zip(x, valores.values):
            eje.text(xi, v, f"{v:,}", ha="center", va="bottom", fontsize=8, color=COLOR_TEXTO)
        eje.set_xticks(list(x))
        eje.set_xticklabels(valores.index, rotation=25, ha="right")
        eje.set_title(col)
        eje.margins(y=0.12)
        eje.yaxis.set_major_formatter(mticker.FuncFormatter(formato_compacto))
    fig.suptitle(titulo, fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    guardar_figura(fig, archivo)
    return fig


def graficar_comparacion_correlaciones(tabla, titulo, archivo):
    """Barras horizontales con la correlación de cada dimensión con el precio.

    Una barra por columna de la tabla (p. ej. inicial, final con Precio_Venta
    y final con su logaritmo). Las celdas NaN (dimensiones que no existían al
    inicio) no se dibujan.
    Parámetros:
        tabla (DataFrame): índice = dimensión; columnas = momentos a comparar.
        titulo (str), archivo (str): título y nombre del PNG.
    Regresa:
        Figure de matplotlib.
    """
    colores = [COLOR_PRINCIPAL, COLOR_PRECIO, "#1fb07f", COLOR_TEXTO]
    n_filas, n_cols = tabla.shape
    alto = 0.8 / n_cols  # Grosor de cada barra dentro del grupo
    fig, eje = plt.subplots(figsize=(11, 0.55 * n_filas * 1.2 + 1))
    y_base = np.arange(n_filas)
    for i, col in enumerate(tabla.columns):
        valores = tabla[col].fillna(0)  # NaN -> barra de largo 0 (no se ve)
        eje.barh(y_base - 0.4 + alto * (i + 0.5), valores.values, height=alto,
                 color=colores[i % len(colores)], label=col)
    eje.set_yticks(y_base)
    eje.set_yticklabels(tabla.index)
    eje.invert_yaxis()  # Primera fila de la tabla arriba
    eje.axvline(0, color=COLOR_TEXTO, lw=0.8)
    eje.set_xlim(-1, 1)
    eje.set_xlabel("Coeficiente de correlación de Pearson")
    eje.legend(fontsize=8, loc="lower right")
    eje.set_title(titulo, fontsize=13, fontweight="bold")
    fig.tight_layout()
    guardar_figura(fig, archivo)
    return fig
