# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Amostra(models.Model):
    id_paciente = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='id_paciente')
    id_exame = models.ForeignKey('Exame', models.DO_NOTHING, db_column='id_exame')
    codigo_amostra = models.CharField(max_length=255)
    metodo_de_coleta = models.CharField(max_length=255)
    material = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'amostra'
        unique_together = (('id_paciente', 'id_exame', 'codigo_amostra'),)


class Exame(models.Model):
    id_exame = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=255)
    virus = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'exame'
        unique_together = (('tipo', 'virus'),)


class ExamplePerfil(models.Model):
    codigo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'example_perfil'


class ExampleUsuario(models.Model):
    cpf = models.CharField(max_length=11)
    nome = models.CharField(max_length=255)
    area_de_pesquisa = models.CharField(max_length=255, blank=True, null=True)
    instituicao = models.CharField(max_length=255, blank=True, null=True)
    data_de_nascimento = models.DateField()
    login = models.CharField(unique=True, max_length=255)
    senha = models.CharField(max_length=255)
    cpf_tutor = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'example_usuario'


class Gerencia(models.Model):
    id_servico = models.ForeignKey('Servico', models.DO_NOTHING, db_column='id_servico')
    id_exame = models.ForeignKey(Exame, models.DO_NOTHING, db_column='id_exame')

    class Meta:
        managed = False
        db_table = 'gerencia'
        unique_together = (('id_servico', 'id_exame'),)


class Paciente(models.Model):
    id_paciente = models.OneToOneField('Pessoa', models.DO_NOTHING, db_column='id_paciente')

    class Meta:
        managed = False
        db_table = 'paciente'


class Perfil(models.Model):
    id_perfil = models.IntegerField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=255)
    tipo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'perfil'


class Pertence(models.Model):
    id_servico = models.ForeignKey('Servico', models.DO_NOTHING, db_column='id_servico')
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')

    class Meta:
        managed = False
        db_table = 'pertence'
        unique_together = (('id_servico', 'id_perfil'),)


class Pessoa(models.Model):
    id_pessoa = models.IntegerField(primary_key=True)
    cpf = models.CharField(unique=True, max_length=11)
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    nascimento = models.DateField()

    class Meta:
        managed = False
        db_table = 'pessoa'


class Possui(models.Model):
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')

    class Meta:
        managed = False
        db_table = 'possui'
        unique_together = (('id_usuario', 'id_perfil'),)


class Realiza(models.Model):
    id_paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='id_paciente')
    id_exame = models.ForeignKey(Exame, models.DO_NOTHING, db_column='id_exame')
    codigo_amostra = models.CharField(max_length=255, blank=True, null=True)
    data_de_solicitacao = models.DateTimeField(blank=True, null=True)
    data_de_realizacao = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'realiza'
        unique_together = (('id_paciente', 'id_exame', 'data_de_realizacao'),)


class Realizou(models.Model):
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    id_servico = models.ForeignKey('Servico', models.DO_NOTHING, db_column='id_servico')
    id_exame = models.ForeignKey(Exame, models.DO_NOTHING, db_column='id_exame')
    data_realizacao = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'realizou'
        unique_together = (('id_usuario', 'id_servico', 'id_exame'),)


class Servico(models.Model):
    id_servico = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    classe = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'servico'
        unique_together = (('nome', 'classe'),)


class Tutelamento(models.Model):
    id_usuario_tutelado = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario_tutelado')
    id_tutor = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_tutor')
    id_servico = models.ForeignKey(Servico, models.DO_NOTHING, db_column='id_servico')
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')
    data_de_inicio = models.DateField()
    data_de_termino = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tutelamento'
        unique_together = (('id_usuario_tutelado', 'id_tutor', 'id_servico', 'id_perfil'),)


class Usuario(models.Model):
    id_usuario = models.OneToOneField(Pessoa, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    area_de_pesquisa = models.CharField(max_length=255, blank=True, null=True)
    instituicao = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)
    id_tutor = models.ForeignKey('self', models.DO_NOTHING, db_column='id_tutor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
