# test_calculadora.py

import unittest
from calculadora import Calculadora

class TestCalculadora(unittest.TestCase):
    """Classe de testes para a classe Calculadora."""

    def setUp(self):
        """Configurações iniciais para cada teste."""
        self.calc = Calculadora()
    
    def test_soma(self):
        """Testa o método de soma com valores positivos."""
        self.assertEqual(self.calc.soma(5, 3), 8)
    
    def test_soma_negativos(self):
        """Testa o método de soma com valores negativos."""
        self.assertEqual(self.calc.soma(-5, -3), -8)

    def test_subtracao(self):
        """Testa o método de subtração."""
        self.assertEqual(self.calc.subtracao(10, 4), 6)
    
    def test_multiplicacao(self):
        """Testa o método de multiplicação."""
        self.assertEqual(self.calc.multiplicacao(7, 8), 56)
        
    def test_divisao(self):
        """Testa o método de divisão com resultado exato."""
        self.assertEqual(self.calc.divisao(10, 2), 5)
    
    def test_divisao_com_float(self):
        """Testa o método de divisão com resultado decimal."""
        self.assertAlmostEqual(self.calc.divisao(10, 3), 3.3333333333333335)
        
    def test_divisao_por_zero(self):
        """Testa se o método de divisão levanta um erro ao dividir por zero."""
        with self.assertRaises(ValueError):
            self.calc.divisao(5, 0)
    
# Executa os testes quando o script é chamado diretamente
if __name__ == '__main__':
    unittest.main()