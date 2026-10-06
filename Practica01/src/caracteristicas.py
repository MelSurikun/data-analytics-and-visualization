"""
Autor:        Melanie
Fecha:        06 octubre 2026
Asignatura:   Analítica y Visualización de Datos (ESCOM - IPN)
Descripción:  Funciones de la Sección E (incisos 25 y 26) y de la Sección F
              (incisos 28 a 30): transformación de "Precio_Venta",
              codificación de categóricas y creación de "Antigüedad",
              "Precio_por_Km" y "Vehiculo_Antiguo".
Insumos:      data/processed/cardekho_transformado.csv (Sección E, 21-24)
Resultados:   Series y DataFrames con las nuevas dimensiones.

Nota: este archivo es un "módulo": solo define funciones y constantes.
Los notebooks Seccion_E25-27_Melanie.ipynb y Seccion_F_Melanie.ipynb lo
importan (import caracteristicas as fc) y llaman a sus funciones.
"""

import numpy as np   # Logaritmo y valores NaN
import pandas as pd  # Manejo de tablas (DataFrames) y columnas (Series)

from homologacion import ANIO_RECOLECCION  # Mismo año usado para derivar "Año"


# ---------------------------------------------------------------------------
# Inciso 25: transformación de "Precio_Venta"
# ---------------------------------------------------------------------------
INR_POR_LAKH = 100_000  # 1 lakh = 100,000 rupias (unidad usual de precios en India)


def precio_en_lakhs(precio):
    """Precio en lakhs = precio en INR / 100,000 (450,000 INR -> 4.5 lakhs)."""
    return precio / INR_POR_LAKH


def precio_logaritmico(precio):
    """Logaritmo natural del precio.

    Comprime los precios muy altos para reducir la asimetría. Solo está
    definido para precios mayores que 0 (en el dataset el mínimo es 40,000).
    """
    return np.log(precio)


# ---------------------------------------------------------------------------
# Inciso 26: codificación de dimensiones categóricas
# ---------------------------------------------------------------------------
def codificar_binaria(serie, valor_positivo):
    """1 si el valor es igual a valor_positivo y 0 en otro caso (int64)."""
    return (serie == valor_positivo).astype("int64")


def codificar_one_hot(df, columnas):
    """Una columna 0/1 por cada clase de cada dimensión (prefijo = dimensión).

    Se conservan todas las clases (sin drop_first) para que cada fila sume 1
    dentro de su grupo y la codificación se pueda leer sin consultar otra tabla.
    """
    return pd.get_dummies(df[columnas], prefix=columnas, dtype="int64")


def codificar_frecuencia(serie):
    """Reemplaza cada clase por la proporción de registros que la tienen (0 a 1)."""
    return serie.map(serie.value_counts(normalize=True))


# ---------------------------------------------------------------------------
# Sección F: ingeniería de características (incisos 28 a 30)
# ---------------------------------------------------------------------------
# Año de referencia: el mismo con el que se derivó "Año" (observación 1).
# El precio se fijó cuando se publicó el anuncio, así que la antigüedad
# relevante es la que tenía el auto en ese momento.
ANIO_REFERENCIA = ANIO_RECOLECCION

# Umbral (en años) a partir del cual un vehículo se considera antiguo.
UMBRAL_ANTIGUO = 10


def crear_antiguedad(anio, anio_referencia=ANIO_REFERENCIA):
    """Antigüedad = año de referencia - año de fabricación (2021 - 2012 -> 9)."""
    return (anio_referencia - anio).astype("int64")


def crear_precio_por_km(precio, km):
    """Precio_por_Km = Precio_Venta / Kilómetros.

    Si Kilómetros es 0 la división no está definida: se deja NaN en lugar de
    infinito (que rompería medias y gráficas) o de 0 (que diría que el auto
    no vale nada por kilómetro).
    """
    return (precio / km.where(km > 0)).astype("float64")


def crear_vehiculo_antiguo(antiguedad, umbral=UMBRAL_ANTIGUO):
    """1 si la antigüedad es mayor o igual al umbral y 0 en otro caso."""
    return (antiguedad >= umbral).astype("int64")
