from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import FormContato

def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('username')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Você fez login com sucesso.')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    messages.success(request, 'Você deslogou, volte sempre :)')
    return redirect("/")



def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    username = request.POST.get('username')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not username or not senha or not senha2:
        messages.error(request, 'Por favor, preencha todos os campos.')
        return render(request, 'accounts/register.html')

    if len(senha) < 6 or not any(chr.isdigit() for chr in senha) or not any(chr.isalpha() for chr in senha):
        messages.error(request, 'Sua senha deve ter pelo menos 8 dígitos, conter números e letras.')
        return render(request, 'accounts/register.html')
        # any(chr.isdigit() for chr in senha) -- CHECANDO SE EXISTE ALGUM (any) NUMERO / LETRA

    if senha != senha2:
        messages.error(request, 'As senhas devem ser iguais.')
        return render(request, 'accounts/register.html')

    if len(username) < 6:
        messages.error(request, 'O nome de usuário deve ter pelo menos 6 caracteres.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
        if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário e email já existem.')
            return render(request, 'accounts/register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Opa, esse usuário já existe. Tente outro')
            return render(request, 'accounts/register.html')
        if  User.objects.filter(email=email).exists():
            messages.error(request, 'Esse email já está cadastrado.')
            return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Registrado com sucesso.')

    user= User.objects.create_user(username=username, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save
    return redirect('login')

   

@login_required(redirect_field_name='login') # vai ser jogado para pagina 'login' caso nao esteja logado
def dashboard(request):

    if request.method != "POST":
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form' : form})
    
   
    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
            messages.error('Erro ao salvar contato.')
            form = FormContato(request.POST)
            return render(request, 'accounts/dashboard.html', {'form' : form})
    
    form.save()
    messages.success(request, f'Prontinho! Novo contato {request.POST.get("nome")} {request.POST.get("sobrenome")} adicionado.')
    return redirect('dashboard')