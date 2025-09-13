from django.test import TestCase
from .models import Produto
from django.urls import reverse

class ProdutoTests(TestCase):

    def setUp(self):
        self.produto = Produto.objects.create(
            nome='Teste', descricao='Descricao teste', preco=10.50, quantidade=5
        )

    def test_listar_produtos(self):
        response = self.client.get(reverse('listar_produtos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Teste')

    def test_criar_produto(self):
        response = self.client.post(reverse('criar_produto'), {
            'nome': 'Novo Produto', 'descricao': 'Descricao', 'preco': 20.00, 'quantidade': 3
        })
        self.assertEqual(response.status_code, 302)  # redireciona
        self.assertTrue(Produto.objects.filter(nome='Novo Produto').exists())

    def test_atualizar_produto(self):
        response = self.client.post(reverse('atualizar_produto', args=[self.produto.pk]), {
            'nome': 'Teste Editado', 'descricao': 'Descricao', 'preco': 15.00, 'quantidade': 10
        })
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'Teste Editado')

    def test_excluir_produto(self):
        response = self.client.post(reverse('excluir_produto', args=[self.produto.pk]))
        self.assertFalse(Produto.objects.filter(pk=self.produto.pk).exists())
