import sqlite3

def criar_tabela():
    """Cria a tabela 'clientes' no banco de dados, se ela não existir."""
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()
    print("Tabela 'clientes' pronta para uso.")

def adicionar_cliente(nome, email):
    """Adiciona um novo cliente ao banco de dados."""
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", (nome, email))
        conn.commit()
        print(f"Cliente '{nome}' adicionado com sucesso.")
    except sqlite3.IntegrityError:
        print(f"Erro: O e-mail '{email}' já está cadastrado.")
    finally:
        conn.close()

def listar_clientes():
    """Lista todos os clientes cadastrados no banco de dados."""
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
        
    print("\n--- Lista de Clientes ---")
    for cliente in clientes:
        print(f"ID: {cliente[0]}, Nome: {cliente[1]}, Email: {cliente[2]}")
    print("-------------------------")

def atualizar_email(cliente_id, novo_email):
    """Atualiza o e-mail de um cliente com base no ID."""
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET email = ? WHERE id = ?", (novo_email, cliente_id))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"E-mail do cliente com ID {cliente_id} atualizado para '{novo_email}'.")
    else:
        print(f"Erro: Cliente com ID {cliente_id} não encontrado.")
        
    conn.close()

def excluir_cliente(cliente_id):
    """Exclui um cliente com base no ID."""
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"Cliente com ID {cliente_id} excluído com sucesso.")
    else:
        print(f"Erro: Cliente com ID {cliente_id} não encontrado.")
        
    conn.close()

def menu():
    """Exibe um menu interativo para o usuário."""
    print("\n--- Sistema de Gerenciamento de Clientes ---")
    print("1. Adicionar novo cliente")
    print("2. Listar todos os clientes")
    print("3. Atualizar e-mail de cliente")
    print("4. Excluir cliente")
    print("5. Sair")
    
    escolha = input("Escolha uma opção: ")
    return escolha

# --- Fluxo principal do programa ---
if __name__ == "__main__":
    criar_tabela()
    
    while True:
        escolha = menu()
        
        if escolha == '1':
            nome = input("Digite o nome do cliente: ")
            email = input("Digite o e-mail do cliente: ")
            adicionar_cliente(nome, email)
        
        elif escolha == '2':
            listar_clientes()
            
        elif escolha == '3':
            try:
                cliente_id = int(input("Digite o ID do cliente para atualizar: "))
                novo_email = input("Digite o novo e-mail: ")
                atualizar_email(cliente_id, novo_email)
            except ValueError:
                print("Erro: ID deve ser um número inteiro.")
        
        elif escolha == '4':
            try:
                cliente_id = int(input("Digite o ID do cliente para excluir: "))
                excluir_cliente(cliente_id)
            except ValueError:
                print("Erro: ID deve ser um número inteiro.")
        
        elif escolha == '5':
            print("Saindo do sistema. Até mais!")
            break
            
        else:
            print("Opção inválida. Tente novamente.")
