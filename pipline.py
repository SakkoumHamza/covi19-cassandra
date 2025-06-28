# Connexion à Cassandra
from cassandra.cluster import Cluster
import pandas as pd
from uuid import uuid4
import datetime


# Connexion à Cassandra (si Cassandra est en local ou via Docker)
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()

# Création du keyspace s'il n'existe pas (bon pour la portabilité)
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS covid_keyspace 
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

# Sélection du keyspace
session.set_keyspace('covid_keyspace')

# Création de la table pour stocker les prédictions si elle n'existe pas déjà
session.execute("""
CREATE TABLE IF NOT EXISTS covid_patients (
    patient_id uuid,
    medical_unit int,
    sex int,
    patient_type int,
    intubed int,
    pneumonia int,
    age int,
    diabetes int,
    hipertension int,
    cardiovascular int,
    renal_chronic int,
    covid_result int,
    prediction_date timestamp,
    PRIMARY KEY ((patient_id))
);
""")

# Préparation de la requête d'insertion pour plus de performance
insert_query = session.prepare("""
    INSERT INTO covid_patients (
        patient_id,
        medical_unit,
        sex,
        patient_type,
        intubed,
        pneumonia,
        age,
        diabetes,
        hipertension,
        cardiovascular,
        renal_chronic,
        covid_result,
        prediction_date
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
""")

# Nouveaux patients à prédire
new_patients = pd.read_csv('data/new_patients.csv')
new_patients['COVID_RESULT'] = model.predict(new_patients) 

# Insertion des nouveaux enregistrements prédits dans Cassandra
for _, row in new_patients.iterrows():
    patient_id = uuid4()
    session.execute(insert_query, (
        patient_id,
        int(row['MEDICAL_UNIT']),
        int(row['SEX']),
        int(row['PATIENT_TYPE']),
        int(row['INTUBED']),
        int(row['PNEUMONIA']),
        int(row['AGE']),
        int(row['DIABETES']),
        int(row['HIPERTENSION']),
        int(row['CARDIOVASCULAR']),
        int(row['RENAL_CHRONIC']),
        int(row['COVID_RESULT']),    
        datetime.datetime.now()       # Ajout du timestamp de la prédiction
    ))

print("Prédictions insérées avec succès.")
