from django.shortcuts import render, get_object_or_404, redirect
from .models import Contato
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages
from pathlib import Path
import sqlite3
from accounts.models import FormContato


def index(request):

    contatos = Contato.objects.order_by('-id').filter(exibir=True)  
    # filter- só mostra o q tiver essa condição , "exibir=True"
    #Contato.objects.all - seleciona todos os contatos da base de dados
    # Contato.objects.order_by - seleciona tds e ordena por ("nome"), "-nome" significa ordem decescrente

    paginator = Paginator(contatos, 10) #exibe 5 contatos por pagina
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos  # <- envia os items da base de dado para o html
    })


def ver_contato(request, contato_id):
    contato = get_object_or_404(Contato,id=contato_id)  # ver um contato de cada vez pelo id, ou mostra erro 404 pagina nao encontrada

    if not contato.exibir:
        raise Http404()

    return render(request, 'contatos/ver_contato.html', {
        'contato': contato  # <- envia o item selecionado da base de dado para o html
    }) 


def busca(request):
    termo = request.GET.get('termo')
    campos = Concat('nome', Value(' '),'sobrenome') # Value simula acrescenta o espaço entre as duas palavras
   
    if termo is None or not termo:
        messages.add_message(request, messages.ERROR, 'O campo de busca não pode ficar vazio.')
        return redirect('index')

    contatos = Contato.objects.annotate(
        nome_completo = campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )# __icontains - se contiver pelo menos parte do termo buscado)
        # Q buscas complexas e o "|" como "OU" = 'nome "OR" sobrenome', em vez de AND

    paginator = Paginator(contatos, 5) 
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos  
    })



def delete(request, contato_id):
    BASE_DIR = Path(__file__).resolve().parent.parent
    try:
        conexao = sqlite3.connect( BASE_DIR / 'db.sqlite3' )
        cursor = conexao.cursor()

        cursor.execute("DELETE FROM contatos_contato WHERE id=:id", {"id": contato_id})
        conexao.commit()

        cursor.close()
        conexao.close()

        messages.success(request, 'Contato excluído com sucesso.')
        return redirect('/')
    except:
        messages.info(request, 'Nenhum contato excluído.')
        return redirect('/')


def editar(request, contato_id):
    contato = Contato.objects.get(id=contato_id) # se estiver postando, POST, se não não, apenas None
    form = FormContato(request.POST or None, request.FILES or None, instance=contato) #instance p preencher campos com as infos de contato
    if form.is_valid():

        form.save()
        messages.success(request, 'Dados do contato foram editados com sucesso')
        return redirect('ver_contato', contato_id)
    
    return render(request, 'contatos/editar.html', {'contato': contato, 'form': form }) 




"""
def editar(request, contato_id):
    contato = get_object_or_404(Contato,id=contato_id) 
    BASE_DIR = Path(__file__).resolve().parent.parent
    name = request.POST.get('nome')

    '''    if request.method =='POST':
        conexao = sqlite3.connect( BASE_DIR / 'db.sqlite3' )
        cursor = conexao.cursor()

        cursor.execute('UPDATE contatos_contato SET nome=:nome WHERE id=:id', 
        {
            "nome": name,
            
            "id": contato_id
         })
        conexao.commit()

        cursor.close()
        conexao.close()

        messages.success(request, 'Contato alterado com sucesso.')
        return redirect('ver_contato')
    else:'''

        #messages.error(request, 'Não foi possível alterar o contato.')
    return render(request, 'contatos/editar.html', {
        'contato': contato 
    }) """