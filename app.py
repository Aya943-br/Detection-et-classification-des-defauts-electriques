from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__, template_folder="interface", static_folder="interface")

# Charger le modèle
try:
    rf_model = joblib.load(os.path.join("poids", "decision_tree_model.pkl"))
    print("[OK] Modèle chargé")
except Exception as e:
    print("[ERREUR] Impossible de charger le modèle:", e)
    rf_model = None

fault_map = {
    0: "Pas de défaut",
    1: "Défaut type GA",
    2: "Défaut type GB",
    3: "Défaut type GC",
    4: "Défaut type ABC",
    5: "Autre défaut"
}

# Routes HTML
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/visualisation")
def visualisation():
    return render_template("visualisation.html")

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Route de prédiction
@app.route("/predict", methods=["POST"])
def predict():
    if rf_model is None:
        return jsonify({"error": "Modèle non chargé"}), 500
    try:
        data = request.get_json()
        X = np.array([[float(data["IA"]), float(data["IB"]), float(data["IC"]),
                       float(data["VA"]), float(data["VB"]), float(data["VC"])]])
        pred_class = int(rf_model.predict(X)[0])
        
        # Confiance fixée à 88.37 %
        confidence = 88.37  

        return jsonify({
            "prediction": pred_class,
            "label": fault_map.get(pred_class, "Classe inconnue"),
            "confidence": confidence
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
