// Simulation pour détection
function detect() {
  const result = document.getElementById("defectPredictionResult");
  result.innerText = "Détection effectuée. (Simulation)";
}

// Simulation pour classification
function classify() {
  const result = document.getElementById("defectPredictionResult");
  result.innerText = "Classification réussie. (Simulation)";
}

// Récupérer les valeurs des inputs
function getInputs() {
  function parseOrZero(val) {
    const num = parseFloat(val);
    return isNaN(num) ? 0 : num;  // si vide ou invalide, retourne 0
  }

  return {
    IA: parseOrZero(document.getElementById('IA').value),
    IB: parseOrZero(document.getElementById('IB').value),
    IC: parseOrZero(document.getElementById('IC').value),
    VA: parseOrZero(document.getElementById('VA').value),
    VB: parseOrZero(document.getElementById('VB').value),
    VC: parseOrZero(document.getElementById('VC').value)
  };
}

// Appel à Flask pour prédiction
async function predictDefect() {
  const inputs = getInputs();
  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(inputs)
    });
    const data = await response.json();
    document.getElementById('defectPredictionResult').innerText =
      `Prédiction défaut : ${data.prediction} (${data.label}) - Confiance modèle : ${data.confidence}%`;
  } catch (error) {
    console.error("Erreur lors de la prédiction :", error);
    document.getElementById('defectPredictionResult').innerText =
      "Erreur lors de la prédiction. Vérifiez la console.";
  }
}

// Appel à Flask pour classification
async function classifyDefect() {
  const inputs = getInputs();
  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(inputs)
    });
    const data = await response.json();
    document.getElementById('defectPredictionResult').innerText =
      `Type de défaut : ${data.label} (Code : ${data.prediction}) - Confiance modèle : ${data.confidence}%`;
  } catch (error) {
    console.error("Erreur lors de la classification :", error);
    document.getElementById('defectPredictionResult').innerText =
      "Erreur lors de la classification. Vérifiez la console.";
  }
}
