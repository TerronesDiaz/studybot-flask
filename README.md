# StudyBot · De modelo a aplicación web

Aplicación Flask que usa el modelo de la segunda entrega de StudyBot para decir si un lugar es
**APTO** o **NO APTO** para trabajar 30 minutos.

Autor: Francisco Javier Terrones Díaz · Aprendizaje Artificial, Maestría en Tecnologías de Internet,
Universidad de Colima.

- **Modelo:** KNN con k = 2 (`KNeighborsClassifier`), elegido por validación cruzada en la segunda entrega.
- **Datos:** [Dataset v1.0 de Kaggle](https://www.kaggle.com/datasets/schiaffino89/lugares-aptos-para-trabajar), 65 lugares, copiado en `data/`.
- **Variables (11, binarias 0/1):** `silencio`, `sombra`, `aire_acondicionado`, `soporte_para_trabajar`,
  `asientos`, `asientos_comodos`, `enchufes`, `flujo_personas`, `banos_cerca`, `cafeteria_cerca`, `internet_wifi`.
- **Preprocesamiento:** ninguno. Las variables ya son 0/1 y en la segunda entrega no se normalizaron.

Las pruebas realizadas y las respuestas a las preguntas están en [ENTREGA.md](ENTREGA.md).

## Ejecutar

Requiere Python 3.10 o superior. Desde la carpeta del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abre <http://127.0.0.1:5000>, marca Sí/No en cada variable y pulsa **Predecir**. Para detener el
servidor, pulsa Ctrl+C.

## Archivos

| Archivo | Para qué |
| --- | --- |
| `app.py` | Aplicación Flask. Carga `studybot_model.joblib` al iniciar; no entrena. |
| `predictor.py` | Función `predecir()`: valida los campos (numéricos, 0 o 1) y llama al modelo. |
| `templates/index.html` | Formulario y resultado. |
| `studybot_model.joblib` | Modelo KNN ya entrenado. |
| `train_model.py` | Paso 1: reproduce el entrenamiento de la segunda entrega y guarda el modelo. |
| `probar_prediccion.py` | Paso 2: prueba la función de predicción sin la página web. |
| `evidencia/` | Capturas de las pruebas en la aplicación. |

Los dos scripts siguientes son opcionales; la app funciona sin ejecutarlos:

```bash
python probar_prediccion.py   # prueba la función con cuatro combinaciones
python train_model.py         # vuelve a generar studybot_model.joblib (mismo resultado)
```
