"""Paso 2. Prueba la función predecir() con varias combinaciones antes de crear la página."""

from predictor import cargar_modelo, predecir

COLUMNAS = [
    "silencio", "sombra", "aire_acondicionado", "soporte_para_trabajar", "asientos",
    "asientos_comodos", "enchufes", "flujo_personas", "banos_cerca", "cafeteria_cerca",
    "internet_wifi",
]

CASOS = {
    "Sala de estudio completa": [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    "Explanada al aire libre": [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    "Pasillo silencioso con clima, sin wifi ni mesa": [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0],
    "Todo excepto silencio": [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
}

modelo = cargar_modelo()
for nombre, valores in CASOS.items():
    resultado = predecir(modelo, dict(zip(COLUMNAS, valores)))
    print(f"{nombre:48} {valores} -> {resultado['etiqueta']:8} "
          f"(vecinos aptos: {resultado['prob_apto']:.0%})")

# Validación: un valor no numérico debe rechazarse antes de llegar al modelo.
try:
    predecir(modelo, {**dict(zip(COLUMNAS, CASOS["Explanada al aire libre"])), "silencio": "mucho"})
except ValueError as error:
    print("Entrada inválida rechazada:", error)
