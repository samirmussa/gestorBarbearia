from datetime import datetime

class Servico:
    def __init__(self, id, nome, preco, tempo_medio, descricao=None):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.tempo_medio = tempo_medio  # em minutos
        self.descricao = descricao

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f} ({self.tempo_medio} min)"

class ItemEstoque:
    def __init__(self, id, nome, quantidade, unidade_medida, nivel_minimo=None, custo_unitario=None):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.unidade_medida = unidade_medida
        self.nivel_minimo = nivel_minimo
        self.custo_unitario = custo_unitario

    def __str__(self):
        return f"{self.nome} - {self.quantidade} {self.unidade_medida}"

class Venda:
    def __init__(self, id, data, servico_id, valor, forma_pagamento):
        self.id = id
        self.data = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        self.servico_id = servico_id
        self.valor = valor
        self.forma_pagamento = forma_pagamento

    def __str__(self):
        return f"{self.data.strftime('%d/%m/%Y %H:%M')} - R${self.valor:.2f} ({self.forma_pagamento})"