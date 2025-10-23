from flask import Flask, render_template, request
from SOLUCION_BAUXITA import optimizar_bauxita

app = Flask(__name__)
PLALU = ['B','C','D','E']

@app.route("/", methods=["GET", "POST"])
def home():
    resultado = None
    if request.method == "POST":
        # Capturar preferencias del usuario
        preferencias_w = {}
        for planta in PLALU:
            preferencias_w[planta] = 1 if request.form.get(planta) == "1" else 0

        resultado = optimizar_bauxita(preferencias_w)

    return render_template("home.html", plantas=PLALU, resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)

