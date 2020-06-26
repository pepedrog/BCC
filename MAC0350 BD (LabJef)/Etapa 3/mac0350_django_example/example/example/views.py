from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from collections import namedtuple
from django.template import loader

def index(request):
    return HttpResponse("MAC0350/2020: Data Management Example")

def query_usuario(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_usuario, cpf, nome, login, area_de_pesquisa, nascimento, \
                               endereco, instituicao \
                        from usuario, pessoa where id_usuario = id_pessoa')
        result = named_tuple_fetchall(cursor)
    
    template = loader.get_template('example/query_usuario.html')
    context = {'usuario_result_list': result,}
    
    return HttpResponse(template.render(context, request))

def query_servico(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM servico')
        result = named_tuple_fetchall(cursor)
    
    template = loader.get_template('example/query_servico.html')
    context = {'servico_result_list': result,}
    
    return HttpResponse(template.render(context, request))
    
def query_perfil(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM perfil')
        result = named_tuple_fetchall(cursor)
    
    template = loader.get_template('example/query_perfil.html')
    context = {'perfil_result_list': result,}

    return HttpResponse(template.render(context, request))


def query_exame(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM exame')
        result = named_tuple_fetchall(cursor)
    
    template = loader.get_template('example/query_exame.html')
    context = {'exame_result_list': result,}
    
    return HttpResponse(template.render(context, request))

def query_especial(request):
    with connection.cursor() as cursor:
        # Query 4.3 da etapa 2 (serviços que podem ser feitos pelos usuários)
        query = """ select distinct usuario.id_usuario as id, pessoa.nome as usuario, servico.nome as servico
                from usuario, possui, servico, pertence, tutelamento, pessoa
                where (pessoa.id_pessoa = usuario.id_usuario) and
                ((usuario.id_usuario = possui.id_usuario and 
                pertence.id_perfil = possui.id_perfil and
                servico.id_servico = pertence.id_servico) or
                (usuario.id_usuario = tutelamento.id_usuario_tutelado and
                servico.id_servico = tutelamento.id_servico)) """
        cursor.execute(query)
        result = named_tuple_fetchall(cursor)
    
    template = loader.get_template('example/query_especial.html')
    context = {'especial_result_list': result,}
    
    return HttpResponse(template.render(context, request))

"""
-- 4.3 Liste os serviços que podem ser utilizados pelos usuarios --

"""
#metodos auxiliares
def named_tuple_fetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    result = [nt_result(*row) for row in cursor.fetchall()]

    return result
