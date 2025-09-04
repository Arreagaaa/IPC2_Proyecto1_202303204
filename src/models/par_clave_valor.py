class ParClaveValor:
    """Clase simple para representar un par clave-valor"""

    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor

    def __str__(self):
        return f"{self.clave}: {self.valor}"
