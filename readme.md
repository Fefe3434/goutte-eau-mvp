# Projet Goutte d’eau – MVP 

Ce dépôt contient le **MVP du projet Goutte d’Eau**, dont l’objectif est de prédire le risque de pluie pour les agriculteurs grâce à l’IA et aux données météo issues de capteurs IoT.  

Il répond aux critères de la feuille de travail (C11 à C15) :  
- Architecture fonctionnelle claire et modulaire  
- API REST avec **FastAPI**  
- Interface utilisateur avec **Streamlit**  
- Base de données locale **SQLite**  
- Prise en compte de l’éco-responsabilité et de l’accessibilité  

---

## Démarrage 

### 1. Créer et activer un environnement virtuel 
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Préparer les données
Nettoyage, normalisation et création des features dans une base SQLite :
```bash
python data_cleaning.py
```

### 4. Entraîner le modèle
Apprentissage d’un **RandomForestClassifier** et export en `.joblib` :
```bash
python model_training.py
```

### 5. Lancer l’API backend 
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info
```
- Endpoint santé : `GET /health`  
- Endpoint prédiction : `GET /risk?param1=...&param2=...`

### 6. Lancer le frontend 
```bash
streamlit run app.py
```
Une interface web simple permet de tester le modèle et d’afficher la probabilité de pluie (%).

---

## Données 

- Lignes après préparation : **6231**
- Label (taux de pluie observée) : **22.9 %** (~0.229)
- Features sélectionnées (mutual information, TOP 8) :
  - `etat du sol`, `temps present`, `pression station`, `temps passe 1`,
  - `nebulosite des nuages de l' etage inferieur`, `pression au niveau mer`,
  - `humidite`, `temperature minimale du sol sur 12 heures (en °c)`
- Persistance en base SQLite : `goutte_mvp.sqlite`

---

## Modèle — Résultats observés 

- **Algorithme** : RandomForestClassifier (`scikit-learn`)  
- **Paramètres** : `n_estimators=500`, `max_depth=8`, `min_samples_leaf=5`, `class_weight=balanced_subsample`  
- **Export** : `data/model.joblib`  

### Scores
- Accuracy : **0.860**
- AUC-ROC : **0.893**
- F1-score : **0.681**

### Rapport de classification 
- Classe 0 (pas de pluie) — précision 0.908, rappel 0.913, F1 0.911 (n=971)  
- Classe 1 (pluie) — précision 0.689, rappel 0.674, F1 0.681 (n=276)  

### Cibles (qualité MVP)
- AUC-ROC > **0.85** atteint  
- F1-score > **0.75** non atteint (0.681 observé)  

### Pistes d’amélioration
- Ajustement du `class_weight` ou test de **BalancedRandomForest**  
- Calibration du seuil de décision  
- Rééchantillonnage (SMOTE, undersampling)  
- Feature engineering temporel (lags, moyennes mobiles, etc.)  

---

## Structure du dépôt
```
goutte-deau-mvp/
├── data/
│   ├── donnees-synop-essentielles-omm.csv   # Données météo brutes
│   ├── goutte_mvp.sqlite                    # Base SQLite avec features nettoyées
│   └── model.joblib                         # Modèle entraîné
│
├── app.py             # Interface Streamlit (UI utilisateur)
├── main.py            # API FastAPI (endpoints /health et /risk)
├── data_cleaning.py   # Nettoyage + préparation des données
├── model_training.py  # Entraînement du modèle et export
├── utils.py           # Fonctions utilitaires
├── requirements.txt   # Dépendances Python
└── README.md          # Documentation
```

---

## API — Endpoints

### `GET /health`
Retourne l’état du service et confirme que le modèle est chargé.  
Par défaut, le modèle est chargé depuis : `MODEL_PATH` (par défaut `./data/model.joblib`).

### `GET /risk`
Params attendus :  
- `etat_sol`, `temps_present`, `pression_station`, `temps_passe`,  
- `nebulosite`, `pression_mer`, `humidite`, `temp_min`

Exemple de réponse JSON :
```json
{
  "etat_sol": 0,
  "temps_present": 2,
  "pression_station": 102290,
  "humidite": 65,
  "temp_min": 12.0,
  "prob_rain": 0.67
}
```

