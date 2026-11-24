"""Paso 2. Función de predicción: recibe los valores de entrada y devuelve APTO / NO APTO.

Solo carga studybot_model.joblib y llama a predict / predict_proba. No entrena nada.
"""

from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path(__file__).with_name("studybot_model.joblib")
ETIQUETAS = {0: "NO APTO", 1: "APTO"}


def cargar_modelo(path=MODEL_PATH):
    return joblib.load(path)


def validar(valores, columnas):
    """Convierte cada campo a número y comprueba que sea 0 o 1.

    Devuelve (fila, errores): fila es un dict columna -> int; errores, columna -> mensaje.
    """
    fila, errores = {}, {}
    for columna in columnas:
        texto = str(valores.get(columna, "")).strip()
        try:
            numero = float(texto)
        except ValueError:
            errores[columna] = "Debe ser un número."
            continue
        if numero not in (0, 1):
            errores[columna] = "Debe ser 0 (no) o 1 (sí)."
            continue
        fila[columna] = int(numero)
    return fila, errores


def predecir(modelo, valores):
    """Predice si un lugar es apto con el modelo ya entrenado.

    valores: dict con una entrada por cada columna del modelo (0 o 1).
    Devuelve un dict con la etiqueta, la clase y la proporción de vecinos aptos.
    Lanza ValueError si falta un campo o no es numérico 0/1.
    """
    columnas = list(modelo.feature_names_in_)
    fila, errores = validar(valores, columnas)
    if errores:
        raise ValueError(errores)

    # Mismas columnas, mismo orden y mismos nombres que en el entrenamiento.
    X = pd.DataFrame([fila], columns=columnas)
    clase = int(modelo.predict(X)[0])
    indice_apto = list(modelo.classes_).index(1)
    prob_apto = float(modelo.predict_proba(X)[0][indice_apto])
    return {"clase": clase, "etiqueta": ETIQUETAS[clase], "prob_apto": prob_apto}
