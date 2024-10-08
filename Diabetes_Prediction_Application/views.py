from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def index(request):
    return render(request, 'index.html', {})
    
def predict1(request):
    return render(request, 'predict.html', )
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

@csrf_exempt
def result1(request):
    url = "data/diabetes.csv" 
    data = pd.read_csv(url)
 
    # Balance the data
    count_class_0, count_class_1 = data['Outcome'].value_counts()

    # Divide by class
    df_class_0 = data[data['Outcome'] == 0]
    df_class_1 = data[data['Outcome'] == 1]

    df_class_1_over = df_class_1.sample(count_class_0, replace=True)
    data = pd.concat([df_class_0, df_class_1_over], axis=0)

    X = data.drop('Outcome', axis=1)
    y = data['Outcome']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2024)

    model = RandomForestClassifier(criterion = 'entropy', max_depth = 17, max_features = 'log2', min_samples_leaf = 1, min_samples_split = 2, n_estimators = 200,random_state=42)
    model.fit(X_train, y_train)

    # Get values from the request
    try:
        val1 =request.GET.get('n1')  # Default value set to 0.0
        val2 =request.GET.get('n2')
        val3 =request.GET.get('n3')
        val4 =request.GET.get('n4')
        val5 =request.GET.get('n5')
        val6 =request.GET.get('n6')
        val7 =request.GET.get('n7')
        val8 =request.GET.get('n8')
    except ValueError:
        return HttpResponse("Invalid input: Please ensure all input values are numeric.")

    pred = model.predict([[val1, val2, val3, val4, val5, val6, val7, val8]])

    if pred == 1:
        result = 'true'
    elif pred == 0:
        result ='false'
    else :
        result='none'

    return render(request, 'predict.html', {'result': result,'val1': val1,
    'val2': val2,
    'val3': val3,
    'val4': val4,
    'val5': val5,
    'val6': val6,
    'val7': val7,
    'val8': val8})