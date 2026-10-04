"""
Autor:        Melanie
Fecha:        03 octubre 2026
Asignatura:   Analítica y Visualización de Datos (ESCOM - IPN)
Descripción:  Funciones de la Sección B (incisos 4 a 8): carga de datos,
              renombrado a español, extracción de "Marca", creación de
              "Marca_Homologada" y construcción de "tabla_homologacion_marcas".
Insumos:      Dataset CarDekho (Kaggle: manishkr1754/cardekho-used-car-data)
              Dataset UCI Automobile (UCI ML Repository, id=10)
Resultados:   DataFrames con dimensiones en español + tabla de homologación.

Nota: este archivo es un "módulo": solo define funciones y constantes.
No hace nada por sí mismo; el notebook Seccion_B_Melanie.ipynb lo importa
(import homologacion as hm) y llama a sus funciones en orden.
"""

import glob   # Buscar archivos por patrón (ej. "*.csv") dentro de una carpeta
import os     # Unir rutas de carpetas de forma compatible con Windows/Linux
import re     # Expresiones regulares (buscar patrones de texto como guiones)

import pandas as pd  # Manejo de tablas (DataFrames) y columnas (Series)


# ---------------------------------------------------------------------------
# Carga de datos
# Los datasets NO se guardan en el repositorio (regla del equipo). Cada
# función los descarga desde su fuente oficial con la librería que provee
# esa fuente (kagglehub para Kaggle, ucimlrepo para UCI).
# ---------------------------------------------------------------------------
def cargar_cardekho():
    """Descarga (o reutiliza la caché de) CarDekho mediante kagglehub.

    Regresa: DataFrame con 15,411 registros y 14 dimensiones.
    """
    # Se importa aquí (y no arriba) para que el módulo pueda usarse aunque
    # kagglehub no esté instalado, mientras no se llame a esta función.
    import kagglehub

    # dataset_download descarga el dataset la primera vez y lo guarda en
    # una caché local (~/.cache/kagglehub). Las siguientes veces reutiliza
    # esa copia, así que no vuelve a descargar. Regresa la carpeta destino.
    ruta = kagglehub.dataset_download("manishkr1754/cardekho-used-car-data")

    # La carpeta contiene un único CSV (cardekho_dataset.csv). Se busca con
    # glob para no depender del nombre exacto del archivo.
    archivo = glob.glob(os.path.join(ruta, "*.csv"))[0]
    return pd.read_csv(archivo)


def cargar_uci():
    """Descarga UCI Automobile con ucimlrepo y une atributos (X) con el precio (y).

    Regresa: DataFrame con 205 registros y 26 dimensiones.
    """
    from ucimlrepo import fetch_ucirepo

    # id=10 es el identificador de "Automobile" en el UCI ML Repository.
    automobile = fetch_ucirepo(id=10)

    # ucimlrepo separa los datos pensando en Machine Learning:
    #   - data.features -> X: las 25 dimensiones descriptivas
    #   - data.targets  -> y: la variable objetivo ("price")
    # Para el análisis se necesitan juntas, así que se concatenan por
    # columnas (axis=1). Ambas comparten el mismo índice de filas.
    return pd.concat([automobile.data.features, automobile.data.targets], axis=1)


# ---------------------------------------------------------------------------
# Inciso 6: renombrado a español
# Diccionarios {nombre_original: nombre_en_español}. Se usan con
# df.rename(columns=...), que crea un DataFrame NUEVO y no altera el original.
# ---------------------------------------------------------------------------
RENOMBRAR_CARDEKHO = {
    "Unnamed: 0": "Indice_Original",     # Índice que quedó al exportar el CSV
    "car_name": "Nombre",                # Marca + modelo (ej. "Maruti Alto")
    "brand": "Marca_Original",           # Fabricante ya incluido en el dataset
    "model": "Modelo",                   # Modelo (ej. "Alto")
    "vehicle_age": "Edad_Vehiculo",      # Años de antigüedad del vehículo
    "km_driven": "Kilómetros",           # Kilómetros recorridos
    "seller_type": "Tipo_Vendedor",      # Individual / Dealer / Trustmark Dealer
    "fuel_type": "Combustible",          # Petrol / Diesel / CNG / LPG / Electric
    "transmission_type": "Transmisión",  # Manual / Automatic
    "mileage": "Millaje",                # Rendimiento en km/l
    "engine": "Motor",                   # Cilindrada en cc
    "max_power": "Potencia_Máxima",      # Potencia en bhp
    "seats": "Asientos",                 # Número de asientos
    "selling_price": "Precio_Venta",     # Precio en rupias indias (INR)
}

RENOMBRAR_UCI = {
    "symboling": "Nivel_Riesgo",                   # Riesgo asignado por aseguradoras (-3 a 3)
    "normalized-losses": "Perdidas_Normalizadas",  # Pérdida promedio por vehículo asegurado
    "make": "Fabricante",                          # Solo el fabricante (ej. "toyota")
    "fuel-type": "Tipo_Combustible",               # gas / diesel
    "aspiration": "Aspiracion",                    # std / turbo
    "num-of-doors": "Num_Puertas",
    "body-style": "Carroceria",                    # sedan, hatchback, etc.
    "drive-wheels": "Traccion",                    # fwd / rwd / 4wd
    "engine-location": "Ubicacion_Motor",          # front / rear
    "wheel-base": "Distancia_Ejes",                # pulgadas
    "length": "Longitud",                          # pulgadas
    "width": "Ancho",                              # pulgadas
    "height": "Altura",                            # pulgadas
    "curb-weight": "Peso_Vacio",                   # libras
    "engine-type": "Tipo_Motor",
    "num-of-cylinders": "Num_Cilindros",
    "engine-size": "Tamano_Motor",                 # pulgadas cúbicas
    "fuel-system": "Sistema_Combustible",
    "bore": "Diametro_Cilindro",
    "stroke": "Carrera_Piston",
    "compression-ratio": "Relacion_Compresion",
    "horsepower": "Caballos_Fuerza",               # hp
    "peak-rpm": "RPM_Maximas",
    "city-mpg": "MPG_Ciudad",                      # millas por galón en ciudad
    "highway-mpg": "MPG_Carretera",                # millas por galón en carretera
    "price": "Precio",                             # dólares (USD) de 1985
}


# ---------------------------------------------------------------------------
# Dimensión "Año" (no existe en esta versión de CarDekho)
# Supuesto documentado: el dataset se publicó en Kaggle en 2021, por lo que
# "vehicle_age" se interpreta como la edad del vehículo en ese año.
# Si el equipo decide otro año de referencia, solo se cambia esta constante.
# ---------------------------------------------------------------------------
ANIO_RECOLECCION = 2021


def crear_anio(edad, anio_referencia=ANIO_RECOLECCION):
    """Año de fabricación = año de recolección - edad del vehículo.

    Ejemplo: edad 9 con referencia 2021 -> 2012.
    Se convierte a int64 porque un año siempre es un número entero.
    """
    return (anio_referencia - edad).astype("int64")


def extraer_marca(nombre):
    """Marca = primera palabra de la dimensión "Nombre" (regla del inciso 6).

    Paso a paso para "Maruti Swift Dzire":
      .str.strip()  -> quita espacios al inicio/final
      .str.split()  -> ["Maruti", "Swift", "Dzire"]
      .str[0]       -> "Maruti"
    Limitación conocida: marcas de dos palabras ("Land Rover") quedan
    truncadas ("Land"); se corrige después en REGLAS_HOMOLOGACION.
    """
    return nombre.str.strip().str.split().str[0]


# ---------------------------------------------------------------------------
# Inciso 7: homologación de marcas
# Se hace en dos etapas:
#   1) limpiar_texto_marca(): reglas GENERALES que aplican a cualquier marca
#      (minúsculas, espacios, guiones, caracteres raros).
#   2) REGLAS_HOMOLOGACION: correcciones PARTICULARES que la limpieza general
#      no puede resolver (errores ortográficos, marcas truncadas, submarcas).
# ---------------------------------------------------------------------------
# Llave = valor ya limpio por la etapa 1; valor = (forma común, justificación).
# La justificación se reutiliza para llenar la tabla de homologación (inciso 8).
REGLAS_HOMOLOGACION = {
    "land": ("land rover",
             "Marca compuesta truncada por la regla 'primera palabra' (Land Rover)"),
    "alfa romero": ("alfa romeo",
                    "Error ortográfico en UCI: el fabricante es Alfa Romeo"),
    "peugot": ("peugeot",
               "Error ortográfico en UCI: el fabricante es Peugeot"),
    "mercedes amg": ("mercedes benz",
                     "AMG es la división deportiva de Mercedes-Benz (mismo fabricante)"),
}


def limpiar_texto_marca(marca):
    """Etapa 1 de la homologación: normalización general del texto.

    Ejemplo: "  Mercedes-Benz " -> "mercedes benz"
    """
    # astype("string") garantiza que se pueda usar .str aunque haya nulos.
    # lower() -> minúsculas ("BMW" -> "bmw"); strip() -> sin espacios extremos.
    s = marca.astype("string").str.lower().str.strip()
    # Guiones y guiones bajos se vuelven espacios ("alfa-romero" -> "alfa romero").
    s = s.str.replace(r"[-_]", " ", regex=True)
    # Se elimina todo lo que no sea letra, número o espacio (puntos, acentos, etc.).
    s = s.str.replace(r"[^a-z0-9 ]", "", regex=True)
    # Varios espacios seguidos se reducen a uno solo.
    return s.str.replace(r"\s+", " ", regex=True).str.strip()


def homologar_marca(marca):
    """Marca_Homologada = etapa 1 (limpieza) + etapa 2 (correcciones).

    Regresa una Series NUEVA; la columna de entrada no se modifica, tal como
    exige el inciso 7 ("sin modificar las dimensiones originales").
    """
    limpia = limpiar_texto_marca(marca)
    # Del diccionario de reglas solo se necesita la forma común (posición 0).
    correcciones = {k: v[0] for k, v in REGLAS_HOMOLOGACION.items()}
    # replace() cambia únicamente los valores que coinciden EXACTAMENTE con
    # una llave; el resto de las marcas se queda igual.
    return limpia.replace(correcciones)


def justificar(marca_original, marca_homologada):
    """Explica en texto qué regla convirtió una marca en su forma homologada.

    Se usa para llenar la columna "Justificación" de la tabla del inciso 8.
    """
    # Si la marca no existe en esa fuente (celda vacía tras el cruce), no hay nada que explicar.
    if pd.isna(marca_original):
        return None
    # Primero se revisa si aplicó una corrección particular (etapa 2).
    limpia = limpiar_texto_marca(pd.Series([marca_original])).iloc[0]
    if limpia in REGLAS_HOMOLOGACION:
        return REGLAS_HOMOLOGACION[limpia][1]
    # Si no, se enumeran las reglas generales (etapa 1) que cambiaron el texto.
    pasos = []
    if marca_original != marca_original.lower():
        pasos.append("minúsculas")
    if re.search(r"[-_]", marca_original):
        pasos.append("guion reemplazado por espacio")
    if marca_original != marca_original.strip():
        pasos.append("espacios eliminados")
    return ("Normalización: " + ", ".join(pasos)) if pasos else "Sin cambios necesarios"


# ---------------------------------------------------------------------------
# Inciso 8: tabla de homologación
# ---------------------------------------------------------------------------
def construir_tabla_homologacion(df_cd, df_uci):
    """Construye "tabla_homologacion_marcas" de forma reproducible.

    Procedimiento:
      1. Obtener las combinaciones únicas (Marca, Marca_Homologada) de cada fuente.
      2. Cruzarlas por Marca_Homologada con un OUTER join, que conserva las
         marcas de ambas fuentes, encuentren pareja o no. Así la tabla muestra
         también qué fabricantes NO tienen correspondencia.
      3. Agregar la justificación y una bandera de correspondencia.
    """
    # Paso 1: marcas únicas por fuente, renombradas como pide el inciso 8.
    cd = (df_cd[["Marca", "Marca_Homologada"]].drop_duplicates()
          .rename(columns={"Marca": "Marca_CarDekho"}))
    uci = (df_uci[["Marca", "Marca_Homologada"]].drop_duplicates()
           .rename(columns={"Marca": "Marca_UCI"}))

    # Paso 2: cruce externo. Si una marca solo existe en una fuente, la
    # columna de la otra queda vacía (NaN).
    tabla = cd.merge(uci, on="Marca_Homologada", how="outer")

    # Paso 3: texto de justificación para cada fila.
    def razon(fila):
        partes = []
        # Explica la transformación aplicada en cada fuente donde exista la marca.
        for fuente, col in (("CarDekho", "Marca_CarDekho"), ("UCI", "Marca_UCI")):
            if pd.notna(fila[col]):
                partes.append(f"{fuente}: {justificar(fila[col], fila['Marca_Homologada'])}")
        # Indica si la marca encontró pareja en la otra fuente.
        if pd.isna(fila["Marca_CarDekho"]):
            partes.append("Sin equivalente en CarDekho")
        elif pd.isna(fila["Marca_UCI"]):
            partes.append("Sin equivalente en UCI")
        else:
            partes.append("Correspondencia encontrada")
        return " | ".join(partes)

    tabla["Justificación"] = tabla.apply(razon, axis=1)  # axis=1 -> fila por fila
    # True solo si la marca aparece en ambas fuentes.
    tabla["Correspondencia"] = tabla["Marca_CarDekho"].notna() & tabla["Marca_UCI"].notna()

    # Orden: primero las marcas con correspondencia, luego alfabético.
    return (tabla[["Marca_CarDekho", "Marca_UCI", "Marca_Homologada",
                   "Correspondencia", "Justificación"]]
            .sort_values(["Correspondencia", "Marca_Homologada"], ascending=[False, True])
            .reset_index(drop=True))
