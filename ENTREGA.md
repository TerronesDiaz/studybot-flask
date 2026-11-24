# StudyBot · De modelo a aplicación web — Entrega

Modelo: KNN con k = 2 de la segunda entrega, entrenado con los mismos 52 lugares (división 80/20,
semilla 42) y las mismas 11 variables binarias del Dataset v1.0. Al volver a entrenarlo y guardarlo
con `train_model.py` obtiene el mismo accuracy en los 13 lugares de prueba que en el notebook: 1.0.

Orden de las variables en las tablas: silencio, sombra, aire_acondicionado, soporte_para_trabajar,
asientos, asientos_comodos, enchufes, flujo_personas, banos_cerca, cafeteria_cerca, internet_wifi.

## Pasos 1 y 2. Modelo guardado y función de predicción

`python train_model.py` guarda el modelo, lo vuelve a cargar y predice un lugar de prueba:

```text
Entrenamiento: 52 · Prueba: 13
Accuracy en prueba (k=2): 1.0000
Guardado en studybot_model.joblib
Modelo cargado: KNeighborsClassifier(n_neighbors=2)
Predicción para «Laboratorio computo mercadotecnia»: 1 (real: 1)
```

`python probar_prediccion.py` prueba `predecir()` antes de usar la página:

```text
Sala de estudio completa                         [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1] -> APTO     (vecinos aptos: 100%)
Explanada al aire libre                          [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0] -> NO APTO  (vecinos aptos: 0%)
Pasillo silencioso con clima, sin wifi ni mesa   [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0] -> NO APTO  (vecinos aptos: 50%)
Todo excepto silencio                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] -> APTO     (vecinos aptos: 100%)
Entrada inválida rechazada: {'silencio': 'Debe ser un número.'}
```

## Paso 4. Pruebas en la aplicación

| # | Entrada | Resultado | Interpretación |
| --- | --- | --- | --- |
| 1 | Sala de estudio completa `1 1 1 1 1 1 1 0 1 0 1` | **APTO** (2 de 2 vecinos aptos) | Tiene todo lo necesario y poca gente. Los dos lugares más parecidos del dataset son aptos. Resultado esperado. |
| 2 | Explanada al aire libre `0 0 0 0 1 0 0 1 0 1 0` | **NO APTO** (0 de 2 vecinos aptos) | Ruidosa, al sol, sin mesa ni enchufes ni wifi. Se parece a plazas y pasillos que en el dataset son no aptos. Resultado esperado. |
| 3 | Pasillo silencioso con clima, sin wifi ni mesa `1 0 1 0 1 1 1 1 1 0 0` | **NO APTO** (1 de 2 vecinos aptos, empate) | **Caso frontera.** Sus dos vecinos más cercanos están a la misma distancia (3 diferencias): *Laboratorio 4 de posgrado* (apto) y *Medios didácticos* (no apto). Con un empate, scikit-learn elige la clase menor (0 = NO APTO). Los cuatro lugares siguientes, a 4 diferencias, son todos aptos: con k = 3 el resultado sería APTO. Es discutible: tiene silencio, clima, enchufes y asientos cómodos, pero no tiene wifi ni mesa. |
| 4 | Todo excepto silencio `0 1 1 1 1 1 1 1 1 1 1` | **APTO** (2 de 2 vecinos aptos) | Coincide exactamente con *Cafetería el Sazón*, que en el dataset está marcada como apta. En la segunda entrega esperábamos que el silencio pesara más. KNN no pondera variables: repite la etiqueta de los lugares parecidos, aunque un lugar ruidoso no parezca apto. |

Capturas: [`evidencia/prueba1_sala_completa.png`](evidencia/prueba1_sala_completa.png),
[`evidencia/prueba2_explanada.png`](evidencia/prueba2_explanada.png),
[`evidencia/prueba3_frontera_empate.png`](evidencia/prueba3_frontera_empate.png),
[`evidencia/prueba4_sin_silencio.png`](evidencia/prueba4_sin_silencio.png).

Validación: si se envía `silencio=abc` o `internet_wifi=5`, la página responde con código 400 y
marca los campos («Debe ser un número.», «Debe ser 0 (no) o 1 (sí).») sin llamar al modelo.

**La app usa el modelo guardado, no reglas:**

- `app.py` no tiene `fit()` ni condiciones sobre las variables. La decisión sale de
  `modelo.predict()` en `predictor.py`.
- Si se quita `studybot_model.joblib`, la app no inicia: `FileNotFoundError: ... studybot_model.joblib`.
- El caso 3 muestra un comportamiento propio de KNN, un empate entre dos vecinos, que una regla escrita a mano no produciría.

## Paso 5. Reproducibilidad

Se copió el proyecto, sin `.venv`, a una carpeta nueva y se siguieron solo los pasos del README:
crear `.venv`, `pip install -r requirements.txt` y `python app.py`. La app inició en
`http://127.0.0.1:5000` y dio las mismas cuatro predicciones de la tabla: APTO, NO APTO, NO APTO y APTO.

## Respuestas

**1. ¿Qué contiene el archivo `studybot_model.joblib`?**
Un objeto `KNeighborsClassifier(n_neighbors=2)` de scikit-learn ya entrenado y serializado con joblib.
Como KNN no aprende pesos, el modelo guarda los 52 lugares de entrenamiento (sus 11 variables) y sus
etiquetas, además de k, la métrica de distancia (euclidiana), las clases `[0, 1]` y los nombres de las
columnas (`feature_names_in_`). No hay pipeline de preprocesamiento porque no se usó ninguno.

**2. ¿Por qué no se debe volver a ejecutar `fit()` dentro de la aplicación?**
Porque la app debe usar el modelo que ya evaluamos. Entrenar en cada petición sería lento,
necesitaría el dataset en el servidor y podría dar otro modelo (otros datos, otra división, otra
versión de las librerías). Entonces ya no se usaría el modelo validado. Entrenar y predecir son
etapas separadas: se entrena una vez, se guarda y la app solo predice.

**3. ¿Por qué la aplicación debe usar exactamente el mismo preprocesamiento del entrenamiento?**
Porque el modelo solo entiende los datos en el formato con que aprendió: mismas columnas, mismo orden
y misma escala. Si en el entrenamiento se escaló o codificó y en la app no, o al revés, las distancias
de KNN cambian y la predicción no es válida, aunque no aparezca ningún error. En este caso la entrada
son 11 valores 0/1 sin transformar, en el orden de `feature_names_in_`. Por eso la app arma un
DataFrame con esas columnas.

**4. ¿Qué diferencia hay entre ejecutar Flask localmente y desplegar una aplicación para uso real?**
`python app.py` usa el servidor de desarrollo de Flask: atiende solo en `127.0.0.1`, para una persona
y sin seguridad. Un despliegue real usa un servidor WSGI de producción (gunicorn, waitress) detrás de
HTTPS. Además tiene una dirección pública, aguanta varios usuarios a la vez, registra errores,
reinicia la app si falla, fija versiones de librerías y protege el servicio contra abusos.
