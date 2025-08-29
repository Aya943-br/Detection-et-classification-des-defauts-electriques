import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ========================
# Configuration de la page
# ========================
st.set_page_config(
    page_title="Détection et Classification des Défauts",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ========================
# CSS Dark Mode Bleu Marine
# ========================
dark_css_blue = """
<style>
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #0b1a2d !important; /* bleu marine foncé */
  color: white;
}

.stApp {
  background-color: #0b1a2d !important; /* fond bleu marine */
}

h1, h2, h3, h4, h5, h6 {
  background: -webkit-linear-gradient(90deg, #00bfff, #1e90ff); /* dégradé bleu clair -> bleu roi */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

p, li, span {
  color: white;
}

.stButton>button {
  background-color: #1e90ff;
  color: white;
  font-weight: 600;
  border-radius: 12px;
  padding: 10px 20px;
  margin-top: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.stButton>button:hover {
  background-color: #104e8b; /* bleu marine foncé */
}
</style>
"""
st.markdown(dark_css_blue, unsafe_allow_html=True)

# ========================
# Dark Mode pour Matplotlib & Seaborn
# ========================
plt.style.use("dark_background")
sns.set_theme(style="darkgrid", palette="Blues")

# ========================
# Hero Section
# ========================
st.markdown('<div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:15vh; padding:20px; text-align:center;">', unsafe_allow_html=True)
st.markdown('<h1>📦 Détection et Classification des Défauts Électriques</h1>', unsafe_allow_html=True)

# ========================
# Section 1 : Classification
# ========================
st.markdown('<h2>🔹 Classification des Défauts</h2>', unsafe_allow_html=True)
CLASS_FILE_PATH = r"C:\Users\Dell\Desktop\detection et classification des defauts electriques\model\classData.csv"

try:
    df_class = pd.read_csv(CLASS_FILE_PATH)
    st.success(f"Fichier de classification chargé : `{CLASS_FILE_PATH}`")
except FileNotFoundError:
    st.error(f"❌ Fichier introuvable : `{CLASS_FILE_PATH}`")
    st.stop()

required_cols = ['G', 'C', 'B', 'A']
if not all(col in df_class.columns for col in required_cols):
    st.error(f"❌ Colonnes manquantes : {required_cols}")
    st.stop()

df_class['label'] = df_class['G'].astype(str) + df_class['C'].astype(str) + df_class['B'].astype(str) + df_class['A'].astype(str)
class_counts = df_class['label'].value_counts().sort_index()

st.subheader("📊 Répartition des Classes")

for class_name, count in class_counts.items():
    st.write(f"🧩 Classe {class_name} : **{count}** instances")

# Graphique en disque (camembert)
fig_class, ax_class = plt.subplots(figsize=(6,6))
colors = sns.color_palette("Blues", len(class_counts))
wedges, texts, autotexts = ax_class.pie(
    class_counts.values,
    labels=class_counts.index,
    autopct='%1.1f%%',
    colors=colors,
    startangle=90,
    textprops={'fontsize':12, 'color':'white'}
)
ax_class.axis("equal")
fig_class.patch.set_facecolor("#0b1a2d")
ax_class.set_title("Répartition des Classes", fontsize=16, pad=15, color='#00bfff')
st.pyplot(fig_class)

# ========================
# Section 2 : Détection
# ========================
st.markdown('<h2>🔹 Détection des Pièces Défectueuses</h2>', unsafe_allow_html=True)
DETECT_FILE_PATH = r"C:\Users\Dell\Desktop\detection et classification des defauts electriques\model\detect_dataset.xlsx"

if os.path.exists(DETECT_FILE_PATH):
    df_detect = pd.read_excel(DETECT_FILE_PATH)
    if 'Output (S)' in df_detect.columns:
        non_defect = (df_detect['Output (S)'] == 0).sum()
        defect = (df_detect['Output (S)'] != 0).sum()

        st.markdown('<h3>📊 Résumé des détections</h3>', unsafe_allow_html=True)
        st.write(f"✅ Pièces sans défaut : **{non_defect}**")
        st.write(f"❌ Pièces avec défaut : **{defect}**")

        fig_detect, ax_detect = plt.subplots(figsize=(5,5))
        colors = sns.color_palette("Blues", 2)
        wedges, texts, autotexts = ax_detect.pie(
            [non_defect, defect],
            labels=["Sans défaut", "Avec défaut"],
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize':12, 'color':'white'}
        )
        ax_detect.axis("equal")
        fig_detect.patch.set_facecolor('#0b1a2d')
        ax_detect.set_title("Répartition des Pièces Détectées", fontsize=16, pad=15, color='#00bfff')
        st.pyplot(fig_detect)
    else:
        st.error("❌ La colonne 'Output (S)' est absente du fichier.")
else:
    st.error(f"❌ Fichier introuvable : `{DETECT_FILE_PATH}`")

# ========================
# Section 3 : Distribution des Variables
# ========================
st.markdown('<h2>🔹 Distribution des Variables Numériques</h2>', unsafe_allow_html=True)

numeric_cols = df_class.select_dtypes(include=['int64','float64']).columns
for col in numeric_cols:
    fig, ax = plt.subplots(figsize=(6,4))
    sns.histplot(df_class[col], kde=True, color="deepskyblue", ax=ax)
    ax.set_facecolor("#0b1a2d")
    fig.patch.set_facecolor("#0b1a2d")
    ax.set_title(f"Distribution de {col}", color="#00bfff")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("white")
    st.pyplot(fig)

# ========================
# Section 4 : Heatmap de corrélation
# ========================

# Section 4 : Heatmap de corrélation
st.markdown('<h2>🔹 Corrélations entre Variables</h2>', unsafe_allow_html=True)

if len(numeric_cols) > 1:
    fig, ax = plt.subplots(figsize=(8,6))
    corr = df_class[numeric_cols].corr()
    sns.heatmap(
        corr, 
        annot=True, 
        cmap="Blues", 
        ax=ax, 
        cbar=True, 
        annot_kws={"color": "white"}  # chiffres blancs
    )
    ax.set_facecolor("#0b1a2d")
    fig.patch.set_facecolor("#0b1a2d")
    ax.set_title("Matrice de Corrélation", color="#00bfff")
    
    # Labels axes X et Y en blanc
    ax.tick_params(axis='x', colors='white', rotation=45)
    ax.tick_params(axis='y', colors='white')
    
    # Légende (colorbar) en blanc
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.label.set_color("white")  # label de la légende
    cbar.ax.tick_params(colors="white")     # ticks de la légende
    
    st.pyplot(fig)



st.markdown('</div>', unsafe_allow_html=True)
