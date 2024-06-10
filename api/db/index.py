import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='db'
    )

def criar_tabelas(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionario (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        cargo VARCHAR(50) NOT NULL,
        salario DECIMAL(10, 2) NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS escala_de_trabalho (
        id INT AUTO_INCREMENT PRIMARY KEY,
        funcionario_id INT,
        data DATE NOT NULL,
        turno VARCHAR(50) NOT NULL,
        FOREIGN KEY (funcionario_id) REFERENCES funcionario(id)
    )
    """)
    
    cursor.close()

# Funções CRUD para a tabela 'login'
def criar_login(conexao, username, password):
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", (username, password))
    conexao.commit()
    cursor.close()

def ler_login(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM login")
    resultados = cursor.fetchall()
    cursor.close()
    return resultados

def atualizar_login(conexao, id, username, password):
    cursor = conexao.cursor()
    cursor.execute("UPDATE login SET username = %s, password = %s WHERE id = %s", (username, password, id))
    conexao.commit()
    cursor.close()

def deletar_login(conexao, id):
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM login WHERE id = %s", (id,))
    conexao.commit()
    cursor.close()

# Funções CRUD para a tabela 'funcionario'
def criar_funcionario(conexao, nome, cargo, salario):
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO funcionario (nome, cargo, salario) VALUES (%s, %s, %s)", (nome, cargo, salario))
    conexao.commit()
    cursor.close()

def ler_funcionario(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM funcionario")
    resultados = cursor.fetchall()
    cursor.close()
    return resultados

def atualizar_funcionario(conexao, id, nome, cargo, salario):
    cursor = conexao.cursor()
    cursor.execute("UPDATE funcionario SET nome = %s, cargo = %s, salario = %s WHERE id = %s", (nome, cargo, salario, id))
    conexao.commit()
    cursor.close()

def deletar_funcionario(conexao, id):
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM funcionario WHERE id = %s", (id,))
    conexao.commit()
    cursor.close()

# Funções CRUD para a tabela 'escala_de_trabalho'
def criar_escala(conexao, funcionario_id, data, turno):
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO escala_de_trabalho (funcionario_id, data, turno) VALUES (%s, %s, %s)", (funcionario_id, data, turno))
    conexao.commit()
    cursor.close()

def ler_escala(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM escala_de_trabalho")
    resultados = cursor.fetchall()
    cursor.close()
    return resultados

def atualizar_escala(conexao, id, funcionario_id, data, turno):
    cursor = conexao.cursor()
    cursor.execute("UPDATE escala_de_trabalho SET funcionario_id = %s, data = %s, turno = %s WHERE id = %s", (funcionario_id, data, turno, id))
    conexao.commit()
    cursor.close()

def deletar_escala(conexao, id):
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM escala_de_trabalho WHERE id = %s", (id,))
    conexao.commit()
    cursor.close()

# Script Principal
conexao = None

try:
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password'
    )
    if conexao.is_connected():
        cursor = conexao.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS db")
        cursor.close()
        conexao.close()

    conexao = conectar_bd()
    if conexao.is_connected():
        print("Conexão realizada com sucesso!")
        criar_tabelas(conexao)
        print("Tabelas criadas ou já existem.")

        # Testando CRUD para 'login'
        criar_login(conexao, 'user1', 'password1')
        print(ler_login(conexao))
        atualizar_login(conexao, 1, 'user1_updated', 'password1_updated')
        print(ler_login(conexao))
        deletar_login(conexao, 1)
        print(ler_login(conexao))

        # Testando CRUD para 'funcionario'
        criar_funcionario(conexao, 'Funcionario 1', 'Cargo 1', 3000.00)
        print(ler_funcionario(conexao))
        atualizar_funcionario(conexao, 1, 'Funcionario 1 atualizado', 'Cargo 1 atualizado', 3500.00)
        print(ler_funcionario(conexao))
        deletar_funcionario(conexao, 1)
        print(ler_funcionario(conexao))

        # Testando CRUD para 'escala_de_trabalho'
        criar_funcionario(conexao, 'Funcionario 2', 'Cargo 2', 4000.00)  # Cria o segundo funcionário
        funcionarios = ler_funcionario(conexao)  # Lê todos os funcionários
        for func in funcionarios:
            print(func)

        funcionario_id = funcionarios[-1][0]  # Pega o id do último funcionário inserido
        criar_escala(conexao, funcionario_id, '2024-06-10', 'Manhã')  # Usa o id do funcionário criado
        print(ler_escala(conexao))
        atualizar_escala(conexao, 1, funcionario_id, '2024-06-11', 'Tarde')
        print(ler_escala(conexao))
        deletar_escala(conexao, 1)
        print(ler_escala(conexao))

except mysql.connector.Error as err:
    print(f"Erro: {err}")
finally:
    if conexao and conexao.is_connected():
        conexao.close()
        print("Conexão encerrada.")
