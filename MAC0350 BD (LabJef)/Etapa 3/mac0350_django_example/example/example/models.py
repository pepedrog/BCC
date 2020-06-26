from django.db import models

class Exame(models.Model):
    id_exame = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=255)
    virus = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'exame'
        unique_together = (('tipo', 'virus'),)

class Gerencia(models.Model):
    id_gerencia = models.IntegerField(primary_key=True)
    id_servico = models.ForeignKey('Servico', models.CASCADE, db_column='id_servico')
    id_exame = models.ForeignKey(Exame, models.CASCADE, db_column='id_exame')

    class Meta:
        managed = False
        db_table = 'gerencia'
        unique_together = (('id_servico', 'id_exame'),)

class Perfil(models.Model):
    id_perfil = models.IntegerField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=255)
    tipo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'perfil'

class Pertence(models.Model):
    id_pertence = models.IntegerField(primary_key=True)
    id_servico = models.ForeignKey('Servico', models.CASCADE, db_column='id_servico')
    id_perfil = models.ForeignKey(Perfil, models.CASCADE, db_column='id_perfil')

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
    id_possui = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.CASCADE, db_column='id_usuario')
    id_perfil = models.ForeignKey(Perfil, models.CASCADE, db_column='id_perfil')

    class Meta:
        managed = False
        db_table = 'possui'
        unique_together = (('id_usuario', 'id_perfil'),)

class Servico(models.Model):
    id_servico = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    classe = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'servico'
        unique_together = (('nome', 'classe'),)

class Usuario(Pessoa):
    id_usuario = models.OneToOneField(Pessoa, models.CASCADE, db_column='id_usuario', primary_key=True, parent_link=True)
    area_de_pesquisa = models.CharField(max_length=255, blank=True, null=True)
    instituicao = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)
    id_tutor = models.ForeignKey('self', models.CASCADE, db_column='id_tutor', blank=True, null=True)

    perfis = models.ManyToManyField(Perfil, through='Possui')
    class Meta:
        managed = False
        db_table = 'usuario'
