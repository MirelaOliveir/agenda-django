from django.contrib import admin
from .models import Categoria, Contato

class ContatoAdmin(admin.ModelAdmin):
    # esses valores serao exibidos no admin para cada cadastro admin/ contatos, na lista de contatos
    list_display = ('id', 'nome', 'sobrenome', 'telefone', 'email', 'categoria', 'data_criacao','exibir')
    list_display_links = ('id', 'nome', 'sobrenome')
    #list_filter = ('nome','sobrenome')
    list_per_page = 10 # quantos contatos serao exibidos por pagina
    search_fields = ('nome', 'sobrenome', 'telefone')
    list_editable = ('exibir', 'telefone')  # ativa edição desses campos na pagina admin

admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)