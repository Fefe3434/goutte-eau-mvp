import pandas as pd
import numpy as np
import sqlite3
from sklearn.feature_selection import mutual_info_classif

from utils import *

print('Loading the data')
CSV_PATH = "./data/donnees-synop-essentielles-omm.csv" 
df_raw = pd.read_csv(CSV_PATH, sep=";")
nan_means = df_raw.isna().mean()

print('Cleaning')
df = df_raw.drop(columns=nan_means[nan_means > 0.5].index) 

for col in df.select_dtypes(include="number").columns:
    df[col] = df[col].fillna(df[col].median())

print("Creating label")
cols_norm = {c: norm(c) for c in df.columns}
df = df.rename(columns=cols_norm)
df = df.select_dtypes(include="number")
df["label"] = (df["precipitations dans les 24 dernieres heures"] > 0).astype(int)
df = df.drop(columns=["precipitations dans les 12 dernieres heures", "precipitations dans les 6 dernieres heures", 
                      "precipitations dans les 3 dernieres heures", "precipitations dans la derniere heure",
                      "precipitations dans les 24 dernieres heures", "temperature minimale du sol sur 12 heures",
                      "temps passe 2"])

num_cols = [c for c in df.select_dtypes(include=[np.number]).columns
            if c not in ['label']]

num_cols = [c for c in num_cols if df[c].nunique(dropna=True) > 1]

print("Performing feature selection using mutual information")
X_full = df[num_cols].values
y_full = df['label'].values
mi = mutual_info_classif(X_full, y_full, random_state=42)
mi_rank = pd.Series(mi, index=num_cols).sort_values(ascending=False)

TOP_K = min(8, len(mi_rank)) 
selected = mi_rank.index[:TOP_K].tolist()
print("\nSelected features:", selected)

print("Saving to sql database")

conn = sqlite3.connect("./data/goutte_mvp.sqlite")
selected_with_label = selected + ['label']
df[selected_with_label].to_sql("features_daily", conn, if_exists="replace", index=False)
conn.close()

for col in df[selected_with_label].columns:
    print(df[col].describe())
