from django.db import models
from django.utils import timezone

# tudo que é criado aqui é adicionado à base de dados que vem por padrão no django/settings 'db.sqlite3'



class Categoria(models.Model):
    nome = models.CharField(max_length=250)

    def __str__(self) -> str:  # metodo magico, altera a forma que o objeto se apresenta
        return self.nome  # no admin ele vai se apresentar pelo nome da categoria("Família", "Amigos") em vez do texto padrão.


class Contato(models.Model):
    nome = models.CharField(max_length=250)  # limite do campo de texto
    sobrenome = models.CharField(max_length=250, blank=True) # blank True pq esse campo é opcional
    telefone = models.CharField(max_length=250)
    email = models.CharField(max_length=250, blank=True)
    data_criacao = models.DateField(default=timezone.now)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING) # associando. DO_NOTHING caso a categoria seja deletada
    exibir = models.BooleanField(default=True)
    foto = models.ImageField(blank=True, upload_to='fotos/%Y/%m/')

    def __str__(self) -> str:
        return self.nome

# fazer isso toda vez que criar ou alterar algum modelo:
# python manage.py makemigrations - 1º para criar os modelos
# pyhton manage.py migrate - 2º para aplicar os modelos na base de dados (tabelas)