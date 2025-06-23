import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date
from database import Database
from models import Servico, ItemEstoque, Venda

class BarbeariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Barbearia")
        self.root.geometry("1000x600")
        
        # Conectar ao banco de dados
        self.db = Database()
        
        # Criar abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Abas do sistema
        self.criar_aba_servicos()
        self.criar_aba_caixa()
        self.criar_aba_estoque()
        self.criar_aba_relatorios()
        
        # Atualizar dados iniciais
        self.atualizar_lista_servicos()
        self.atualizar_lista_estoque()
        
    def criar_aba_servicos(self):
        # Frame principal
        self.aba_servicos = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_servicos, text="Serviços e Preços")
        
        # Frame de lista
        frame_lista = ttk.LabelFrame(self.aba_servicos, text="Serviços Disponíveis")
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para listar serviços
        self.tree_servicos = ttk.Treeview(frame_lista, columns=('ID', 'Nome', 'Preço', 'Tempo', 'Descrição'), show='headings')
        self.tree_servicos.heading('ID', text='ID')
        self.tree_servicos.heading('Nome', text='Nome')
        self.tree_servicos.heading('Preço', text='Preço (MZN)')
        self.tree_servicos.heading('Tempo', text='Tempo (min)')
        self.tree_servicos.heading('Descrição', text='Descrição')
        
        self.tree_servicos.column('ID', width=50)
        self.tree_servicos.column('Nome', width=150)
        self.tree_servicos.column('Preço', width=100)
        self.tree_servicos.column('Tempo', width=80)
        self.tree_servicos.column('Descrição', width=300)
        
        self.tree_servicos.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_servicos.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_servicos.configure(yscrollcommand=scrollbar.set)
        
        # Frame de botões
        frame_botoes = ttk.Frame(self.aba_servicos)
        frame_botoes.pack(fill='x', padx=10, pady=5)
        
        # Botões
        btn_adicionar = ttk.Button(frame_botoes, text="Adicionar Serviço", command=self.adicionar_servico)
        btn_adicionar.pack(side='left', padx=5)
        
        btn_editar = ttk.Button(frame_botoes, text="Editar Serviço", command=self.editar_servico)
        btn_editar.pack(side='left', padx=5)
        
        btn_remover = ttk.Button(frame_botoes, text="Remover Serviço", command=self.remover_servico)
        btn_remover.pack(side='left', padx=5)
    
    def criar_aba_caixa(self):
        # Frame principal
        self.aba_caixa = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_caixa, text="Caixa")
        
        # Frame de serviços
        frame_servicos = ttk.LabelFrame(self.aba_caixa, text="Selecionar Serviço")
        frame_servicos.pack(fill='x', padx=10, pady=10)
        
        # Combobox para selecionar serviço
        self.servico_var = tk.StringVar()
        self.combo_servicos = ttk.Combobox(frame_servicos, textvariable=self.servico_var, state='readonly')
        self.combo_servicos.pack(fill='x', padx=5, pady=5)
        
        # Frame de pagamento
        frame_pagamento = ttk.LabelFrame(self.aba_caixa, text="Forma de Pagamento")
        frame_pagamento.pack(fill='x', padx=10, pady=5)
        
        # Opções de pagamento
        self.forma_pagamento = tk.StringVar(value='Dinheiro')
        opcoes_pagamento = ['Dinheiro', 'Cartão de Débito', 'M-PESA', 'E-MOLA', 'Transferência Bancaria']
        
        for opcao in opcoes_pagamento:
            rb = ttk.Radiobutton(frame_pagamento, text=opcao, value=opcao, variable=self.forma_pagamento)
            rb.pack(side='left', padx=5, pady=5)
        
        # Botão de registrar venda
        btn_registrar = ttk.Button(self.aba_caixa, text="Registrar Venda", command=self.registrar_venda)
        btn_registrar.pack(pady=10)
        
        # Frame de histórico
        frame_historico = ttk.LabelFrame(self.aba_caixa, text="Histórico do Dia")
        frame_historico.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para histórico
        self.tree_vendas = ttk.Treeview(frame_historico, columns=('ID', 'Hora', 'Serviço', 'Valor', 'Pagamento'), show='headings')
        self.tree_vendas.heading('ID', text='ID')
        self.tree_vendas.heading('Hora', text='Hora')
        self.tree_vendas.heading('Serviço', text='Serviço')
        self.tree_vendas.heading('Valor', text='Valor (MZN)')
        self.tree_vendas.heading('Pagamento', text='Pagamento')
        
        self.tree_vendas.column('ID', width=50)
        self.tree_vendas.column('Hora', width=100)
        self.tree_vendas.column('Serviço', width=200)
        self.tree_vendas.column('Valor', width=100)
        self.tree_vendas.column('Pagamento', width=150)
        
        self.tree_vendas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Atualizar combobox de serviços
        self.atualizar_combobox_servicos()
        self.atualizar_historico_vendas()
    
    def criar_aba_estoque(self):
        # Frame principal
        self.aba_estoque = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_estoque, text="Controle de Estoque")
        
        # Frame de lista
        frame_lista = ttk.LabelFrame(self.aba_estoque, text="Itens em Estoque")
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview para listar estoque
        self.tree_estoque = ttk.Treeview(frame_lista, columns=('ID', 'Nome', 'Quantidade', 'Unidade', 'Mínimo', 'Custo'), show='headings')
        self.tree_estoque.heading('ID', text='ID')
        self.tree_estoque.heading('Nome', text='Nome')
        self.tree_estoque.heading('Quantidade', text='Quantidade')
        self.tree_estoque.heading('Unidade', text='Unidade')
        self.tree_estoque.heading('Mínimo', text='Nível Mínimo')
        self.tree_estoque.heading('Custo', text='Custo Unitário')
        
        self.tree_estoque.column('ID', width=50)
        self.tree_estoque.column('Nome', width=150)
        self.tree_estoque.column('Quantidade', width=80)
        self.tree_estoque.column('Unidade', width=80)
        self.tree_estoque.column('Mínimo', width=80)
        self.tree_estoque.column('Custo', width=100)
        
        self.tree_estoque.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_estoque.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_estoque.configure(yscrollcommand=scrollbar.set)
        
        # Frame de botões
        frame_botoes = ttk.Frame(self.aba_estoque)
        frame_botoes.pack(fill='x', padx=10, pady=5)
        
        # Botões
        btn_adicionar = ttk.Button(frame_botoes, text="Adicionar Item", command=self.adicionar_item_estoque)
        btn_adicionar.pack(side='left', padx=5)
        
        btn_editar = ttk.Button(frame_botoes, text="Editar Item", command=self.editar_item_estoque)
        btn_editar.pack(side='left', padx=5)
        
        btn_remover = ttk.Button(frame_botoes, text="Remover Item", command=self.remover_item_estoque)
        btn_remover.pack(side='left', padx=5)
        
        # Frame de alertas
        frame_alertas = ttk.LabelFrame(self.aba_estoque, text="Itens com Estoque Baixo")
        frame_alertas.pack(fill='x', padx=10, pady=10)
        
        self.label_alertas = ttk.Label(frame_alertas, text="Carregando...")
        self.label_alertas.pack(pady=5)
        
        # Atualizar alertas
        self.atualizar_alertas_estoque()
    
    def criar_aba_relatorios(self):
        # Frame principal
        self.aba_relatorios = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_relatorios, text="Relatórios")
        
        # Notebook para sub-abas
        self.sub_notebook = ttk.Notebook(self.aba_relatorios)
        self.sub_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Sub-aba de relatório diário
        self.criar_subaba_relatorio_diario()
        
        # Sub-aba de relatório mensal
        self.criar_subaba_relatorio_mensal()
    
    def criar_subaba_relatorio_diario(self):
        # Frame principal
        frame_diario = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(frame_diario, text="Relatório Diário")
        
        # Frame de seleção de data
        frame_data = ttk.Frame(frame_diario)
        frame_data.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_data, text="Data:").pack(side='left', padx=5)
        
        self.data_relatorio_diario = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        entry_data = ttk.Entry(frame_data, textvariable=self.data_relatorio_diario)
        entry_data.pack(side='left', padx=5)
        
        btn_atualizar = ttk.Button(frame_data, text="Atualizar", command=self.gerar_relatorio_diario)
        btn_atualizar.pack(side='left', padx=5)
        
        # Frame de resultados
        frame_resultados = ttk.LabelFrame(frame_diario, text="Resultados")
        frame_resultados.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Labels para mostrar os resultados
        self.label_total_vendas = ttk.Label(frame_resultados, text="Total de Vendas: MZN0.00")
        self.label_total_vendas.pack(anchor='w', padx=10, pady=5)
        
        self.label_qtd_servicos = ttk.Label(frame_resultados, text="Quantidade de Serviços: 0")
        self.label_qtd_servicos.pack(anchor='w', padx=10, pady=5)
        
        # Frame de formas de pagamento
        frame_pagamentos = ttk.LabelFrame(frame_resultados, text="Formas de Pagamento")
        frame_pagamentos.pack(fill='x', padx=10, pady=5)
        
        self.tree_pagamentos = ttk.Treeview(frame_pagamentos, columns=('Forma', 'Valor'), show='headings')
        self.tree_pagamentos.heading('Forma', text='Forma de Pagamento')
        self.tree_pagamentos.heading('Valor', text='Valor (MZN)')
        
        self.tree_pagamentos.column('Forma', width=150)
        self.tree_pagamentos.column('Valor', width=100)
        
        self.tree_pagamentos.pack(fill='x', padx=5, pady=5)
        
        # Gerar relatório para o dia atual
        self.gerar_relatorio_diario()
    
    def criar_subaba_relatorio_mensal(self):
        # Frame principal
        frame_mensal = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(frame_mensal, text="Relatório Mensal")
        
        # Frame de seleção de mês/ano
        frame_selecao = ttk.Frame(frame_mensal)
        frame_selecao.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_selecao, text="Mês:").pack(side='left', padx=5)
        
        self.mes_relatorio = tk.IntVar(value=date.today().month)
        combo_mes = ttk.Combobox(frame_selecao, textvariable=self.mes_relatorio, values=list(range(1, 13)), state='readonly')
        combo_mes.pack(side='left', padx=5)
        
        ttk.Label(frame_selecao, text="Ano:").pack(side='left', padx=5)
        
        self.ano_relatorio = tk.IntVar(value=date.today().year)
        combo_ano = ttk.Combobox(frame_selecao, textvariable=self.ano_relatorio, 
                                values=list(range(date.today().year-5, date.today().year+1)), state='readonly')
        combo_ano.pack(side='left', padx=5)
        
        btn_atualizar = ttk.Button(frame_selecao, text="Atualizar", command=self.gerar_relatorio_mensal)
        btn_atualizar.pack(side='left', padx=5)
        
        # Frame de resultados
        frame_resultados = ttk.LabelFrame(frame_mensal, text="Resultados")
        frame_resultados.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Labels para mostrar os resultados
        self.label_total_mensal = ttk.Label(frame_resultados, text="Total de Vendas no Mês: MZN0.00")
        self.label_total_mensal.pack(anchor='w', padx=10, pady=5)
        
        self.label_qtd_mensal = ttk.Label(frame_resultados, text="Quantidade de Serviços no Mês: 0")
        self.label_qtd_mensal.pack(anchor='w', padx=10, pady=5)
        
        # Frame de vendas por dia
        frame_vendas_dia = ttk.LabelFrame(frame_resultados, text="Vendas por Dia")
        frame_vendas_dia.pack(fill='x', padx=10, pady=5)
        
        self.tree_vendas_dia = ttk.Treeview(frame_vendas_dia, columns=('Dia', 'Vendas'), show='headings')
        self.tree_vendas_dia.heading('Dia', text='Dia')
        self.tree_vendas_dia.heading('Vendas', text='Vendas (MZN)')
        
        self.tree_vendas_dia.column('Dia', width=100)
        self.tree_vendas_dia.column('Vendas', width=100)
        
        self.tree_vendas_dia.pack(fill='x', padx=5, pady=5)
        
        # Frame de serviços mais vendidos
        frame_servicos = ttk.LabelFrame(frame_resultados, text="Serviços Mais Vendidos")
        frame_servicos.pack(fill='x', padx=10, pady=5)
        
        self.tree_servicos_vendidos = ttk.Treeview(frame_servicos, columns=('Serviço', 'Quantidade', 'Total'), show='headings')
        self.tree_servicos_vendidos.heading('Serviço', text='Serviço')
        self.tree_servicos_vendidos.heading('Quantidade', text='Quantidade')
        self.tree_servicos_vendidos.heading('Total', text='Total (MZN)')
        
        self.tree_servicos_vendidos.column('Serviço', width=200)
        self.tree_servicos_vendidos.column('Quantidade', width=100)
        self.tree_servicos_vendidos.column('Total', width=100)
        
        self.tree_servicos_vendidos.pack(fill='x', padx=5, pady=5)
        
        # Gerar relatório para o mês atual
        self.gerar_relatorio_mensal()
    
    # Métodos para serviços
    def atualizar_lista_servicos(self):
        # Limpar treeview
        for item in self.tree_servicos.get_children():
            self.tree_servicos.delete(item)
        
        # Obter serviços do banco de dados
        servicos = self.db.listar_servicos()
        
        # Adicionar serviços à treeview
        for servico in servicos:
            self.tree_servicos.insert('', 'end', values=servico)
    
    def adicionar_servico(self):
        # Janela para adicionar novo serviço
        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Serviço")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Variáveis para armazenar os valores
        self.nome_var = tk.StringVar()
        self.preco_var = tk.StringVar()
        self.tempo_var = tk.StringVar()
        self.descricao_var = tk.StringVar()
        
        # Campos do formulário
        ttk.Label(dialog, text="Nome do Serviço:*").pack(pady=(10, 0))
        entry_nome = ttk.Entry(dialog, textvariable=self.nome_var)
        entry_nome.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Preço (MZN):*").pack()
        entry_preco = ttk.Entry(dialog, textvariable=self.preco_var)
        entry_preco.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Tempo Médio (minutos):*").pack()
        entry_tempo = ttk.Entry(dialog, textvariable=self.tempo_var)
        entry_tempo.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Descrição (opcional):").pack()
        text_descricao = tk.Text(dialog, height=5)
        text_descricao.pack(fill='x', padx=10, pady=5)
        
        # Frame para botões
        frame_botoes = ttk.Frame(dialog)
        frame_botoes.pack(fill='x', pady=10)
        
        # Botão Cancelar
        btn_cancelar = ttk.Button(frame_botoes, text="Cancelar", command=dialog.destroy)
        btn_cancelar.pack(side='right', padx=5)
        
        # Botão Salvar
        btn_salvar = ttk.Button(
            frame_botoes, 
            text="Salvar", 
            command=lambda: self.salvar_servico(
                self.nome_var.get(),
                self.preco_var.get(),
                self.tempo_var.get(),
                text_descricao.get("1.0", tk.END).strip(),
                dialog
            )
        )
        btn_salvar.pack(side='right', padx=5)
        
        # Configurar foco inicial e comportamento da tecla Enter
        entry_nome.focus_set()
        dialog.bind('<Return>', lambda e: btn_salvar.invoke())
    
    def salvar_servico(self, nome, preco, tempo, descricao, dialog):
        # Validar campos
        if not nome or not preco or not tempo:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            preco = float(preco)
            tempo = int(tempo)
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número e tempo deve ser inteiro!")
            return
        
        # Adicionar ao banco de dados
        self.db.adicionar_servico(nome, preco, tempo, descricao if descricao else None)
        
        # Atualizar lista
        self.atualizar_lista_servicos()
        self.atualizar_combobox_servicos()
        
        # Fechar diálogo
        dialog.destroy()
        messagebox.showinfo("Sucesso", "Serviço adicionado com sucesso!")
    
    def editar_servico(self):
        # Obter item selecionado
        selecionado = self.tree_servicos.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um serviço para editar!")
            return
        
        item = self.tree_servicos.item(selecionado[0])
        servico_id, nome, preco, tempo, descricao = item['values']
        
        # Janela para editar serviço
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Serviço")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Campos do formulário
        ttk.Label(dialog, text="Nome do Serviço:").pack(pady=(10, 0))
        entry_nome = ttk.Entry(dialog)
        entry_nome.insert(0, nome)
        entry_nome.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Preço (MZN):").pack()
        entry_preco = ttk.Entry(dialog)
        entry_preco.insert(0, preco)
        entry_preco.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Tempo Médio (minutos):").pack()
        entry_tempo = ttk.Entry(dialog)
        entry_tempo.insert(0, tempo)
        entry_tempo.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Descrição (opcional):").pack()
        text_descricao = tk.Text(dialog, height=5)
        text_descricao.insert("1.0", descricao if descricao else "")
        text_descricao.pack(fill='x', padx=10, pady=5)
        
        # Botões
        frame_botoes = ttk.Frame(dialog)
        frame_botoes.pack(fill='x', pady=10)
        
        btn_cancelar = ttk.Button(frame_botoes, text="Cancelar", command=dialog.destroy)
        btn_cancelar.pack(side='right', padx=5)
        
        btn_salvar = ttk.Button(frame_botoes, text="Salvar", command=lambda: self.atualizar_servico(
            servico_id,
            entry_nome.get(),
            entry_preco.get(),
            entry_tempo.get(),
            text_descricao.get("1.0", tk.END).strip(),
            dialog
        ))
        btn_salvar.pack(side='right', padx=5)
        
        entry_nome.focus_set()
    
    def atualizar_servico(self, servico_id, nome, preco, tempo, descricao, dialog):
        # Validar campos
        if not nome or not preco or not tempo:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            preco = float(preco)
            tempo = int(tempo)
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número e tempo deve ser inteiro!")
            return
        
        # Atualizar no banco de dados
        self.db.atualizar_servico(servico_id, nome, preco, tempo, descricao if descricao else None)
        
        # Atualizar lista
        self.atualizar_lista_servicos()
        self.atualizar_combobox_servicos()
        
        # Fechar diálogo
        dialog.destroy()
        messagebox.showinfo("Sucesso", "Serviço atualizado com sucesso!")
    
    def remover_servico(self):
        # Obter item selecionado
        selecionado = self.tree_servicos.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um serviço para remover!")
            return
        
        item = self.tree_servicos.item(selecionado[0])
        servico_id, nome, *_ = item['values']
        
        # Confirmar remoção
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o serviço '{nome}'?"):
            # Remover do banco de dados
            self.db.remover_servico(servico_id)
            
            # Atualizar lista
            self.atualizar_lista_servicos()
            self.atualizar_combobox_servicos()
            
            messagebox.showinfo("Sucesso", "Serviço removido com sucesso!")
    
    # Métodos para caixa
    def atualizar_combobox_servicos(self):
        servicos = self.db.listar_servicos()
        valores = [f"{s[1]} - MZN{s[2]:.2f}" for s in servicos]
        self.combo_servicos['values'] = valores
        if valores:
            self.combo_servicos.current(0)
    
    def atualizar_historico_vendas(self):
        # Limpar treeview
        for item in self.tree_vendas.get_children():
            self.tree_vendas.delete(item)
        
        # Obter vendas do dia atual
        data_hoje = date.today().strftime('%Y-%m-%d')
        vendas = self.db.listar_vendas_por_periodo(f"{data_hoje} 00:00:00", f"{data_hoje} 23:59:59")
        
        # Adicionar vendas à treeview
        for venda in vendas:
            venda_id, data, servico, valor, pagamento = venda
            hora = datetime.strptime(data, '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
            self.tree_vendas.insert('', 'end', values=(venda_id, hora, servico, valor, pagamento))
    
    def registrar_venda(self):
        # Obter serviço selecionado
        servico_idx = self.combo_servicos.current()
        if servico_idx == -1:
            messagebox.showwarning("Aviso", "Selecione um serviço!")
            return
        
        # Obter dados do serviço
        servicos = self.db.listar_servicos()
        servico_id, nome, preco, *_ = servicos[servico_idx]
        forma_pagamento = self.forma_pagamento.get()
        
        # Registrar venda no banco de dados
        self.db.registrar_venda(servico_id, preco, forma_pagamento)
        
        # Atualizar histórico
        self.atualizar_historico_vendas()
        
        # Atualizar relatório diário
        self.gerar_relatorio_diario()
        
        messagebox.showinfo("Sucesso", f"Venda registrada: {nome} - MZN{preco:.2f} ({forma_pagamento})")
    
    # Métodos para estoque
    def atualizar_lista_estoque(self):
        # Limpar treeview
        for item in self.tree_estoque.get_children():
            self.tree_estoque.delete(item)
        
        # Obter itens do estoque
        estoque = self.db.listar_estoque()
        
        # Adicionar itens à treeview
        for item in estoque:
            self.tree_estoque.insert('', 'end', values=item)
    
    def atualizar_alertas_estoque(self):
        itens = self.db.listar_estoque()
        alertas = []
        
        for item in itens:
            id, nome, quantidade, unidade, nivel_minimo, custo = item
            if nivel_minimo is not None and quantidade <= nivel_minimo:
                alertas.append(f"{nome} - {quantidade} {unidade} (mínimo: {nivel_minimo})")
        
        if alertas:
            self.label_alertas.config(text="\n".join(alertas), foreground='red')
        else:
            self.label_alertas.config(text="Nenhum item com estoque baixo", foreground='green')
    
    def adicionar_item_estoque(self):
        # Janela para adicionar novo item
        dialog = tk.Toplevel(self.root)
        dialog.title("Adicionar Item ao Estoque")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Campos do formulário
        ttk.Label(dialog, text="Nome do Item:").pack(pady=(10, 0))
        entry_nome = ttk.Entry(dialog)
        entry_nome.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Quantidade:").pack()
        entry_quantidade = ttk.Entry(dialog)
        entry_quantidade.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Unidade de Medida:").pack()
        entry_unidade = ttk.Entry(dialog)
        entry_unidade.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Nível Mínimo (opcional):").pack()
        entry_minimo = ttk.Entry(dialog)
        entry_minimo.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Custo Unitário (opcional):").pack()
        entry_custo = ttk.Entry(dialog)
        entry_custo.pack(fill='x', padx=10, pady=5)
        
        # Botões
        frame_botoes = ttk.Frame(dialog)
        frame_botoes.pack(fill='x', pady=10)
        
        btn_cancelar = ttk.Button(frame_botoes, text="Cancelar", command=dialog.destroy)
        btn_cancelar.pack(side='right', padx=5)
        
        btn_salvar = ttk.Button(frame_botoes, text="Salvar", command=lambda: self.salvar_item_estoque(
            entry_nome.get(),
            entry_quantidade.get(),
            entry_unidade.get(),
            entry_minimo.get(),
            entry_custo.get(),
            dialog
        ))
        btn_salvar.pack(side='right', padx=5)
        
        entry_nome.focus_set()
    
    def salvar_item_estoque(self, nome, quantidade, unidade, minimo, custo, dialog):
        # Validar campos
        if not nome or not quantidade or not unidade:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            quantidade = int(quantidade)
            minimo = int(minimo) if minimo else None
            custo = float(custo) if custo else None
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e nível mínimo devem ser inteiros, custo deve ser número!")
            return
        
        # Adicionar ao banco de dados
        self.db.adicionar_item_estoque(nome, quantidade, unidade, minimo, custo)
        
        # Atualizar lista e alertas
        self.atualizar_lista_estoque()
        self.atualizar_alertas_estoque()
        
        # Fechar diálogo
        dialog.destroy()
        messagebox.showinfo("Sucesso", "Item adicionado ao estoque com sucesso!")
    
    def editar_item_estoque(self):
        # Obter item selecionado
        selecionado = self.tree_estoque.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para editar!")
            return
        
        item = self.tree_estoque.item(selecionado[0])
        item_id, nome, quantidade, unidade, minimo, custo = item['values']
        
        # Janela para editar item
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Item do Estoque")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Campos do formulário
        ttk.Label(dialog, text="Nome do Item:").pack(pady=(10, 0))
        entry_nome = ttk.Entry(dialog)
        entry_nome.insert(0, nome)
        entry_nome.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Quantidade:").pack()
        entry_quantidade = ttk.Entry(dialog)
        entry_quantidade.insert(0, quantidade)
        entry_quantidade.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Unidade de Medida:").pack()
        entry_unidade = ttk.Entry(dialog)
        entry_unidade.insert(0, unidade)
        entry_unidade.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Nível Mínimo (opcional):").pack()
        entry_minimo = ttk.Entry(dialog)
        entry_minimo.insert(0, minimo if minimo else "")
        entry_minimo.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dialog, text="Custo Unitário (opcional):").pack()
        entry_custo = ttk.Entry(dialog)
        entry_custo.insert(0, custo if custo else "")
        entry_custo.pack(fill='x', padx=10, pady=5)
        
        # Botões
        frame_botoes = ttk.Frame(dialog)
        frame_botoes.pack(fill='x', pady=10)
        
        btn_cancelar = ttk.Button(frame_botoes, text="Cancelar", command=dialog.destroy)
        btn_cancelar.pack(side='right', padx=5)
        
        btn_salvar = ttk.Button(frame_botoes, text="Salvar", command=lambda: self.atualizar_item_estoque(
            item_id,
            entry_nome.get(),
            entry_quantidade.get(),
            entry_unidade.get(),
            entry_minimo.get(),
            entry_custo.get(),
            dialog
        ))
        btn_salvar.pack(side='right', padx=5)
        
        entry_nome.focus_set()
    
    def atualizar_item_estoque(self, item_id, nome, quantidade, unidade, minimo, custo, dialog):
        # Validar campos
        if not nome or not quantidade or not unidade:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            quantidade = int(quantidade)
            minimo = int(minimo) if minimo else None
            custo = float(custo) if custo else None
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e nível mínimo devem ser inteiros, custo deve ser número!")
            return
        
        # Atualizar no banco de dados
        self.db.atualizar_item_estoque(item_id, nome, quantidade, unidade, minimo, custo)
        
        # Atualizar lista e alertas
        self.atualizar_lista_estoque()
        self.atualizar_alertas_estoque()
        
        # Fechar diálogo
        dialog.destroy()
        messagebox.showinfo("Sucesso", "Item atualizado com sucesso!")
    
    def remover_item_estoque(self):
        # Obter item selecionado
        selecionado = self.tree_estoque.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para remover!")
            return
        
        item = self.tree_estoque.item(selecionado[0])
        item_id, nome, *_ = item['values']
        
        # Confirmar remoção
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o item '{nome}'?"):
            # Remover do banco de dados
            self.db.remover_item_estoque(item_id)
            
            # Atualizar lista e alertas
            self.atualizar_lista_estoque()
            self.atualizar_alertas_estoque()
            
            messagebox.showinfo("Sucesso", "Item removido com sucesso!")
    
    # Métodos para relatórios
    def gerar_relatorio_diario(self):
        try:
            data = datetime.strptime(self.data_relatorio_diario.get(), '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Erro", "Data inválida! Use o formato AAAA-MM-DD")
            return
        
        relatorio = self.db.relatorio_diario(data.strftime('%Y-%m-%d'))
        
        # Atualizar labels
        self.label_total_vendas.config(text=f"Total de Vendas: MZN{relatorio['total_vendas']:.2f}")
        self.label_qtd_servicos.config(text=f"Quantidade de Serviços: {relatorio['qtd_servicos']}")
        
        # Atualizar treeview de formas de pagamento
        for item in self.tree_pagamentos.get_children():
            self.tree_pagamentos.delete(item)
        
        for forma, valor in relatorio['formas_pagamento']:
            self.tree_pagamentos.insert('', 'end', values=(forma, f"{valor:.2f}"))
    
    def gerar_relatorio_mensal(self):
        try:
            ano = self.ano_relatorio.get()
            mes = self.mes_relatorio.get()
        except tk.TclError:
            messagebox.showerror("Erro", "Ano e mês devem ser números!")
            return
        
        relatorio = self.db.relatorio_mensal(ano, mes)
        
        # Atualizar labels
        self.label_total_mensal.config(text=f"Total de Vendas no Mês: MZN{relatorio['total_vendas']:.2f}")
        self.label_qtd_mensal.config(text=f"Quantidade de Serviços no Mês: {relatorio['qtd_servicos']}")
        
        # Atualizar treeview de vendas por dia
        for item in self.tree_vendas_dia.get_children():
            self.tree_vendas_dia.delete(item)
        
        for dia, valor in relatorio['vendas_por_dia']:
            self.tree_vendas_dia.insert('', 'end', values=(dia, f"{valor:.2f}"))
        
        # Atualizar treeview de serviços mais vendidos
        for item in self.tree_servicos_vendidos.get_children():
            self.tree_servicos_vendidos.delete(item)
        
        for nome, qtd, total in relatorio['servicos_mais_vendidos']:
            self.tree_servicos_vendidos.insert('', 'end', values=(nome, qtd, f"{total:.2f}"))
    
    def __del__(self):
        # Fechar conexão com o banco de dados
        self.db.fechar_conexao()

if __name__ == "__main__":
    root = tk.Tk()
    app = BarbeariaApp(root)
    root.mainloop()