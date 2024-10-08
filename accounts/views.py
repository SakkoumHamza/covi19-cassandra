# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import CustomUser  # Utilisez le modèle utilisateur personnalisé
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import EmailVerificationCode
def auth_view(request):
    return render(request,'accounts/auth.html')

def generate_verification_code():
    return str(random.randint(100000, 999999))

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if not username or not email or not password:
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, 'accounts/auth.html')
        
        # Check if username already exists
        if get_user_model().objects.filter(username=username).exists():
            messages.error(request, "Le nom d'utilisateur existe déjà.")
            return render(request, 'accounts/auth.html')
        
        # Check if email already exists
        if get_user_model().objects.filter(email=email).exists():
            messages.error(request, "L'email existe déjà.")
            return render(request, 'accounts/auth.html')
        
        user_type = 'client'
        user = get_user_model().objects.create_user(username=username, email=email, password=password, user_type=user_type)
        user.is_active = False  # User is not active until email is verified
        user.save()
        
        code = generate_verification_code()
        EmailVerificationCode.objects.create(user=user, code=code)
        
        email_subject = "Votre code de vérification"
        email_message = f"Votre code de vérification est {code}"
        
        send_mail(email_subject, email_message, settings.EMAIL_HOST_USER, [user.email])
        messages.success(request, "Inscription réussie. Vérifiez votre email pour le code de vérification.")
        return redirect('verify_email', user_id=user.id)
    return render(request, 'accounts/auth.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Vous êtes connecté en tant que {username}.")
            return redirect('dashboard')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'accounts/auth.html')


def dashboard_view(request):
    # Example view for client dashboard
    if not request.user.is_authenticated or request.user.user_type != 'client':
        return redirect('login')  # Redirect to login if not authenticated or not client
    
    # Logic for client dashboard here
    return render(request, 'dashboard/predict.html', {'username': request.user.username})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import CustomUser, EmailVerificationCode


def verify_email_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    email_verified = False
    if request.method == 'POST':
        code = request.POST['code']
        try:
            verification_code = EmailVerificationCode.objects.get(user=user, code=code)
            if verification_code:
                user.is_active = True
                user.save()
                login(request,user)
                verification_code.delete()  # Optionally delete the code after successful verification
                email_verified = True
        except EmailVerificationCode.DoesNotExist:
            messages.error(request, "Code de vérification invalide.")
    return render(request, 'accounts/verify_email.html', {'user': user,'email_verified': email_verified})
    