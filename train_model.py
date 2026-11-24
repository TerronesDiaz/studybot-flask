"""Paso 1. Guarda el modelo de la segunda entrega en studybot_model.joblib.

Reproduce el entrenamiento del notebook Proyecto_Guedea_Terrones.ipynb:
- Dataset v1.0 de Kaggle (schiaffino89/lugares-aptos-para-trabajar).
- Las mismas 11 variables binarias; se quitan Lugar y Target.
- División 80/20 con np.random.seed(42): 52 lugares para entrenar y 13 para probar.
- KNeighborsClassifier con k = 2, el k elegido por validación cruzada.
- Sin preprocesamiento: todas las variables ya son 0/1 y no se normalizaron.

Este script es el único lugar donde se ejecuta fit(). La aplicación solo carga el archivo.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

BASE = Path(__file__).parent
DATASET = BASE / "data" / "Dataset v1.0.csv"
MODEL_PATH = BASE / "studybot_model.joblib"
K = 2

df = pd.read_csv(DATASET)
X = df.drop(columns=["Lugar", "Target"])
y = df["Target"]

# La misma división que en la segunda entrega.
np.random.seed(42)
indices = np.arange(len(X))
np.random.shuffle(indices)
limite = int(len(X) * 0.80)
X_train, X_test = X.iloc[indices[:limite]], X.iloc[indices[limite:]]
y_train, y_test = y.iloc[indices[:limite]], y.iloc[indices[limite:]]

# Se entrena con un DataFrame para que el modelo guarde los nombres de las columnas
# (feature_names_in_). Así la app sabe qué variables pedir y en qué orden.
modelo = KNeighborsClassifier(n_neighbors=K)
modelo.fit(X_train, y_train)
print(f"Entrenamiento: {len(X_train)} · Prueba: {len(X_test)}")
print(f"Accuracy en prueba (k={K}): {accuracy_score(y_test, modelo.predict(X_test)):.4f}")

joblib.dump(modelo, MODEL_PATH)
print(f"Guardado en {MODEL_PATH.name}")

# Verificación: cargar el archivo guardado y predecir un lugar de prueba.
cargado = joblib.load(MODEL_PATH)
fila = X_test.iloc[[0]]
lugar = df.loc[fila.index[0], "Lugar"]
print(f"Modelo cargado: {cargado}")
print(f"Columnas: {list(cargado.feature_names_in_)}")
print(f"Predicción para «{lugar}»: {cargado.predict(fila)[0]} (real: {y_test.iloc[0]})")
