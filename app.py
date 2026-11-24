"""Paso 3. Aplicación Flask de StudyBot.

Carga studybot_model.joblib una sola vez al iniciar y solo lo usa para predecir.
No hay reglas escritas a mano: la decisión APTO / NO APTO la toma el modelo KNN.
"""

from flask import Flask, render_template, request

from predictor import cargar_modelo, predecir

app = Flask(__name__)
modelo = cargar_modelo()  # Se carga al iniciar; no se vuelve a entrenar.
COLUMNAS = list(modelo.feature_names_in_)

# Solo textos para mostrar en el formulario. Los nombres de los campos son las columnas del modelo.
TEXTOS = {
    "silencio": ("Silencio", "El lugar es tranquilo"),
    "sombra": ("Sombra", "Protegido del sol directo"),
    "aire_acondicionado": ("Aire acondicionado", "Tiene clima"),
    "soporte_para_trabajar": ("Soporte para trabajar", "Mesa o superficie para la laptop"),
    "asientos": ("Asientos", "Hay dónde sentarse"),
    "asientos_comodos": ("Asientos cómodos", "Se puede estar sentado 30 minutos"),
    "enchufes": ("Enchufes", "Contactos para cargar"),
    "flujo_personas": ("Flujo de personas", "Pasa gente con frecuencia"),
    "banos_cerca": ("Baños cerca", "Sanitarios a poca distancia"),
    "cafeteria_cerca": ("Cafetería cerca", "Comida o bebida a poca distancia"),
    "internet_wifi": ("Internet / wifi", "Conexión disponible"),
}


@app.route("/", methods=["GET", "POST"])
def index():
    valores, errores, resultado = {}, {}, None
    if request.method == "POST":
        valores = {columna: request.form.get(columna, "") for columna in COLUMNAS}
        try:
            resultado = predecir(modelo, valores)
        except ValueError as error:
            errores = error.args[0]
    campos = [(columna, *TEXTOS.get(columna, (columna, ""))) for columna in COLUMNAS]
    return render_template(
        "index.html",
        campos=campos,
        valores=valores,
        errores=errores,
        resultado=resultado,
        k=modelo.n_neighbors,
    ), 400 if errores else 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
