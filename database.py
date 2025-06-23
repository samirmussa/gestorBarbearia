import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='barbearia.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Tabela de serviços (cortes de cabelo)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            tempo_medio INTEGER NOT NULL,  
            descricao TEXT
        )
        ''')
        
        # Tabela de materiais/estoque
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            unidade_medida TEXT NOT NULL,
            nivel_minimo INTEGER,
            custo_unitario REAL
        )
        ''')
        
        # Tabela de vendas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            servico_id INTEGER NOT NULL,
            valor REAL NOT NULL,
            forma_pagamento TEXT NOT NULL,
            FOREIGN KEY (servico_id) REFERENCES servicos(id)
        )
        ''')
        
        # Tabela de despesas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL
        )
        ''')
        
        self.conn.commit()

    # Métodos para serviços
    def adicionar_servico(self, nome, preco, tempo_medio, descricao=None):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO servicos (nome, preco, tempo_medio, descricao)
        VALUES (?, ?, ?, ?)
        ''', (nome, preco, tempo_medio, descricao))
        self.conn.commit()
        return cursor.lastrowid

    def listar_servicos(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM servicos ORDER BY nome')
        return cursor.fetchall()

    def atualizar_servico(self, servico_id, nome, preco, tempo_medio, descricao=None):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE servicos 
        SET nome=?, preco=?, tempo_medio=?, descricao=?
        WHERE id=?
        ''', (nome, preco, tempo_medio, descricao, servico_id))
        self.conn.commit()

    def remover_servico(self, servico_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM servicos WHERE id=?', (servico_id,))
        self.conn.commit()

    # Métodos para estoque
    def adicionar_item_estoque(self, nome, quantidade, unidade_medida, nivel_minimo=None, custo_unitario=None):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO estoque (nome, quantidade, unidade_medida, nivel_minimo, custo_unitario)
        VALUES (?, ?, ?, ?, ?)
        ''', (nome, quantidade, unidade_medida, nivel_minimo, custo_unitario))
        self.conn.commit()
        return cursor.lastrowid

    def listar_estoque(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM estoque ORDER BY nome')
        return cursor.fetchall()

    def atualizar_item_estoque(self, item_id, nome, quantidade, unidade_medida, nivel_minimo=None, custo_unitario=None):
        cursor = self.conn.cursor()
        cursor.execute('''
        UPDATE estoque 
        SET nome=?, quantidade=?, unidade_medida=?, nivel_minimo=?, custo_unitario=?
        WHERE id=?
        ''', (nome, quantidade, unidade_medida, nivel_minimo, custo_unitario, item_id))
        self.conn.commit()

    def remover_item_estoque(self, item_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM estoque WHERE id=?', (item_id,))
        self.conn.commit()

    # Métodos para vendas
    def registrar_venda(self, servico_id, valor, forma_pagamento):
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO vendas (data, servico_id, valor, forma_pagamento)
        VALUES (?, ?, ?, ?)
        ''', (data_atual, servico_id, valor, forma_pagamento))
        self.conn.commit()
        return cursor.lastrowid

    def listar_vendas_por_periodo(self, data_inicio, data_fim):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT v.id, v.data, s.nome, v.valor, v.forma_pagamento 
        FROM vendas v
        JOIN servicos s ON v.servico_id = s.id
        WHERE v.data BETWEEN ? AND ?
        ORDER BY v.data
        ''', (data_inicio, data_fim))
        return cursor.fetchall()

    # Métodos para relatórios
    def relatorio_diario(self, data):
        cursor = self.conn.cursor()
        
        # Total de vendas do dia
        cursor.execute('''
        SELECT SUM(valor) 
        FROM vendas 
        WHERE date(data) = date(?)
        ''', (data,))
        total_vendas = cursor.fetchone()[0] or 0
        
        # Quantidade de serviços realizados
        cursor.execute('''
        SELECT COUNT(*) 
        FROM vendas 
        WHERE date(data) = date(?)
        ''', (data,))
        qtd_servicos = cursor.fetchone()[0] or 0
        
        # Formas de pagamento
        cursor.execute('''
        SELECT forma_pagamento, SUM(valor) 
        FROM vendas 
        WHERE date(data) = date(?)
        GROUP BY forma_pagamento
        ''', (data,))
        formas_pagamento = cursor.fetchall()
        
        return {
            'total_vendas': total_vendas,
            'qtd_servicos': qtd_servicos,
            'formas_pagamento': formas_pagamento
        }

    def relatorio_mensal(self, ano, mes):
        cursor = self.conn.cursor()
        
        # Total de vendas do mês
        cursor.execute('''
        SELECT SUM(valor) 
        FROM vendas 
        WHERE strftime('%Y', data) = ? AND strftime('%m', data) = ?
        ''', (str(ano), f"{mes:02d}"))
        total_vendas = cursor.fetchone()[0] or 0
        
        # Quantidade de serviços realizados
        cursor.execute('''
        SELECT COUNT(*) 
        FROM vendas 
        WHERE strftime('%Y', data) = ? AND strftime('%m', data) = ?
        ''', (str(ano), f"{mes:02d}"))
        qtd_servicos = cursor.fetchone()[0] or 0
        
        # Vendas por dia
        cursor.execute('''
        SELECT date(data), SUM(valor) 
        FROM vendas 
        WHERE strftime('%Y', data) = ? AND strftime('%m', data) = ?
        GROUP BY date(data)
        ORDER BY date(data)
        ''', (str(ano), f"{mes:02d}"))
        vendas_por_dia = cursor.fetchall()
        
        # Serviços mais vendidos
        cursor.execute('''
        SELECT s.nome, COUNT(*), SUM(v.valor)
        FROM vendas v
        JOIN servicos s ON v.servico_id = s.id
        WHERE strftime('%Y', v.data) = ? AND strftime('%m', v.data) = ?
        GROUP BY s.nome
        ORDER BY COUNT(*) DESC
        LIMIT 5
        ''', (str(ano), f"{mes:02d}"))
        servicos_mais_vendidos = cursor.fetchall()
        
        return {
            'total_vendas': total_vendas,
            'qtd_servicos': qtd_servicos,
            'vendas_por_dia': vendas_por_dia,
            'servicos_mais_vendidos': servicos_mais_vendidos
        }

    def fechar_conexao(self):
        self.conn.close()