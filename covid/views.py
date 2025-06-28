from django.shortcuts import render
from cassandra.cluster import Cluster
import joblib
import pandas as pd
from uuid import uuid4
import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import pandas as pd
from django.http import HttpResponse

def predict(request):
    return render(request, 'predict.html', )


def result(request):
    model = joblib.load("covid_model.pkl")
    print("Modèle chargé avec succès")
    
    # Get values from the request
    try:
        val1 =float(request.GET.get('n1'))  # Default value set to 0.0
        val2 =float(request.GET.get('n2'))
        val3 =float(request.GET.get('n3'))
        val4 =float(request.GET.get('n4'))
        val5 =float(request.GET.get('n5'))
        val6 =float(request.GET.get('n6'))
        val7 =float(request.GET.get('n7'))
        val8 =float(request.GET.get('n8'))
        val9 =float(request.GET.get('n9'))
        val10 =float(request.GET.get('n10'))

    except ValueError:
        return HttpResponse("Invalid input: Please ensure all input values are numeric.")

    print("✅donnes arrive a result")
    
      #Connexion à Cassandra (si Cassandra est en local ou via Docker)
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()
    print("✅ Connexion réussie")

    #Création du keyspace s'il n'existe pas (bon pour la portabilité)
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS covid_keyspace 
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
    """)

    #Sélection du keyspace
    session.set_keyspace('covid_keyspace')

    #Création de la table pour stocker les prédictions si elle n'existe pas déjà
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
    pred = model.predict([[val1, val2, val3, val4, val5, val6, val7, val8,val9,val10]])
      # Insertion des nouveaux enregistrements prédits dans Cassandra
    patient_id = uuid4()
    session.execute(insert_query, (
        patient_id,
        int(val1),
        int(val2),
        int(val3),
        int(val4),
        int(val5),
        int(val6),
        int(val7),
        int(val8),
        int(val9),
        int(val10),
        int(pred[0]) ,
        datetime.datetime.now()       # Ajout du timestamp de la prédiction
    ))
    if pred[0]==1:
        result='true'
    else : 
        result='false'
    print("Prédictions insérées avec succès.")

    return render(request, 'predict.html', 
                  {'result':result ,
                    'val1': val1,
                    'val2': val2,
                    'val3': val3,
                    'val4': val4,
                    'val5': val5,
                    'val6': val6,
                    'val7': val7,
                    'val8': val8,
                    'val9': val9,
                    'val10': val10
                })
