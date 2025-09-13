from django.contrib import admin
from .models import Produto

admin.site.register(Produto)

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade')
    search_fields = ('nome',)