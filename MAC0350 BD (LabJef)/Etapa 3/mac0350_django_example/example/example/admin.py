from django.contrib import admin
from .models import Usuario, Perfil, Servico, Exame, Possui, Pertence, Gerencia

class GerenciaInline(admin.TabularInline):
    model = Gerencia
    extra = 1

class PertenceInline(admin.TabularInline):
    model = Pertence
    extra = 1

class PossuiInline(admin.TabularInline):
    model = Possui
    extra = 1

class ServicoAdmin(admin.ModelAdmin):
    inlines = (PertenceInline, GerenciaInline)

class PerfilAdmin(admin.ModelAdmin):
    inlines = (PertenceInline,)

class UsuarioAdmin(admin.ModelAdmin):
    inlines = (PossuiInline,)

class ExameAdmin(admin.ModelAdmin):
    inlines = (GerenciaInline,)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Servico, ServicoAdmin)
admin.site.register(Exame, ExameAdmin)