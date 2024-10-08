from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


@login_required
def predict2(request):
    # Logic for the prediction page
    return render(request, 'dashboard/predict.html',{'username': request.user.username})
    
    
@login_required
def diets(request):
    # Logic for the diets page
    return render(request, 'dashboard/diets.html',{'username': request.user.username})
    
@login_required
def doctors(request):
    # Logic for the doctors page
    return render(request, 'dashboard/doctors.html',{'username': request.user.username})

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

@login_required
def contact_doctor(request):
    email_sent =False
    doctor_email = subject = message = ''
    if request.method == 'POST':
        doctor_email = request.POST['doctor-mail']
        subject = request.POST['subject']
        message = request.POST['message']
        from_email = settings.DEFAULT_FROM_EMAIL

        try:
            send_mail(subject, message, from_email, [doctor_email])
            email_sent = True
            messages.success(request, 'Votre message a été envoyé avec succès.')
        except Exception as e:
            messages.error(request, f'Une erreur s\'est produite lors de l\'envoi de votre message: {e}')

    return render(request, 'dashboard/doctors.html',{
        'email_sent': email_sent,
        'mail': request.POST['doctor-mail'],  # Pass doctor email as context variable
        'subject': request.POST['subject'],
        'message': request.POST['message'],
        'username':request.user.username})
        
from django.contrib.auth import logout

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')  # Redirect to login page after logout
    else:
        return redirect('home')
        
@login_required
def result2(request):
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

    model = RandomForestClassifier(criterion = 'entropy', max_depth = 17, max_features = 'log2',
    min_samples_leaf = 1, min_samples_split = 2, n_estimators = 200,random_state=42)
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
        result = 'false'
    else :
        result='none'

    return render(request, 'dashboard/predict.html', {'result': result,'username':request.user.username,
    'val1': val1,
    'val2': val2,
    'val3': val3,
    'val4': val4,
    'val5': val5,
    'val6': val6,
    'val7': val7,
    'val8': val8
    })