from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd

# Chargement des données d'entraînement
df = pd.read_csv('data/covid_data.csv')

# Création de la colonne cible : 1 si le patient est COVID+ (classes 1,2,3), sinon 0
df['covid_result'] = df['CLASIFFICATION_FINAL'].apply(lambda x: 1 if x in [1,2,3] else 0)

# Suppression des colonnes peu corrélées ou inutiles pour l'entraînement
drops = [
    'PREGNANT',
    'OTHER_DISEASE',
    'TOBACCO',
    'USMER',
    'INMSUPR',
    'ASTHMA',
    'COPD',
    'OBESITY',
    'ICU',
    'CLASIFFICATION_FINAL',  # remplacée par covid_result
    'DATE_DIED'              # inutile pour la prédiction
]
df = df.drop(columns=drops, axis=1)

# Séparation des features et de la cible
X = df.drop('covid_result', axis=1)
Y = df['covid_result']

# Split des données pour entraînement et test
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.2, random_state=25)

print('Entrainement du modele')
# Entraînement du modèle Random Forest
model = RandomForestClassifier(criterion='entropy', n_estimators=200, random_state=25)
model.fit(Xtrain.values, Ytrain.values)

print("✅ Model done")

joblib.dump(model, 'covid_model.pkl')  # Ajoute ça après l'entraînement
