import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="Goutte d'eau – MVP")
st.title("🌧️ Goutte d'eau – MVP")

etat_sol = st.number_input("Etat du sol", min_value=0, max_value=3, value=0, help='0 à 3 pour qualifié ...')
temps_present = st.number_input("Temps présent", min_value=0, max_value=100, value=2, help='0 à 100 pour qualifié ...')
pression_station = st.number_input("Pression station (Pa)", min_value=98420, max_value=103510, value=98420, help="Pression de l'air au niveau de la station en Pascal")
temps_passe = st.number_input("Temps passé", min_value=0, max_value=9, value=4, help="0 à 9 pour qualifié ...")

nebulosite = st.number_input("Nebulosite des nuages de l'étage inferieur", min_value=0, max_value=8, value=2, help='0 = ciel clair; 8 = ciel complètement couvert')
pression_mer = st.number_input("Pression au niveau mer (Pa)", min_value=98730, max_value=103840, value=98730, help="Pression de l'air au niveau de la mer en Pascal")
humidite = st.number_input("Humidité", min_value=10, max_value=100, value=50, help="0 à 100 pour qualifié le taux d'humidité")
temp_min = st.number_input("temperature minimale du sol sur 12 heures (en °c)", min_value=0, max_value=33, value=20)

api_url = "http://127.0.0.1:8000"

if st.button("Prédire"):
    try:
        params = {
            'etat_sol':etat_sol,
            'temps_present':temps_present,
            'pression_station':pression_station,
            'temps_passe':temps_passe,
            'nebulosite':nebulosite,
            'pression_mer':pression_mer,
            'humidite':humidite,
            'temp_min':temp_min,
        }
        r = requests.get(f"{api_url}/risk", params=params, timeout=10)
        if r.ok:
            prob = r.json()["prob_rain"]
            st.metric("Probabilité de pluie", f"{int(round(prob*100))}%")
        else:
            st.error(f"Erreur API: {r.status_code} - {r.text}")
    except Exception as e:
        st.error(f"Appel API impossible: {e}")