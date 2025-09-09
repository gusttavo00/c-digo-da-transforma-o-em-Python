# calculadora.py

class Calculadora:
    """Uma classe simples para operações matemáticas básicas."""

    def soma(self, a, b):
        """Retorna a soma de dois números."""
        return a + b

    def subtracao(self, a, b):
        """Retorna a subtração de dois números."""
        return a - b

    def multiplicacao(self, a, b):
        """Retorna a multiplicação de dois números."""
        return a * b

    def divisao(self, a, b):
        """Retorna a divisão de dois números.
        
        Levanta uma exceção ValueError se o denominador for zero.
        """
        if b == 0:
            raise ValueError("Não é possível dividir por zero.")
        return a / b