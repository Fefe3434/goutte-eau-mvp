import pandas as pd
import numpy as np
import sqlite3, joblib

import numpy as np, pandas as pd
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, classification_report

from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, precision_recall_curve, classification_report


print('Loading the dataset')
conn = sqlite3.connect("./data/goutte_mvp.sqlite")
df = pd.read_sql("SELECT * FROM features_daily", conn)
conn.close()
print(df.head())               

X = df.drop(columns=["label"]).values
y = df[["label"]].values
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, shuffle=False)

print('Training the model')
rf = RandomForestClassifier(
    n_estimators=500,
    max_depth=8,
    min_samples_leaf=5,
    class_weight="balanced_subsample",
    random_state=42,
    n_jobs=-1
)
rf.fit(Xtr, ytr)

proba = rf.predict_proba(Xte)[:, 1]
pred  = (proba >= 0.5).astype(int)
print('Claasification accuracy :',rf.score(Xte, yte))

print("\nAUC:", round(roc_auc_score(yte, proba), 3), "| F1:", round(f1_score(yte, pred), 3))
print(classification_report(yte, pred, digits=3))

print('Saving the model')

joblib.dump(rf, "./data/model.joblib")