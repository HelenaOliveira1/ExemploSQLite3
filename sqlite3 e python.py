"""
   Montagem completa do exemplo do link Gerenciando banco de dados SQLite3 com python - parte1
"""

print("----------Inicio do Programa---------\n")

import sqlite3
import io

#conctando sqlite3 para database clientes
conn = sqlite3.connect("clientes.db")

#definindo um cursor
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE clientes (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        cpf VARCHAR(11) NOT NULL,
        email TEXT NOT NULL,
        fone TEXT,
        cidade TEXT,
        uf VARCHAR(2) NOT NULL,
        criado_em DATE NOT NULL
);
""")

print("\nTabela criada com sucesso.\n")

#Insere um único conjunto de atributos para tabela cliente
cursor.execute("""
INSERT INTO clientes (nome, idade, cpf, email, fone, cidade, uf, criado_em)
VALUES ('Matheus', 19, '33333333333', 'matheus@email.com', '11-98765-4324', 'Campinas', 'SP', '2014-06-08')
""")

#Salva dados no banco
conn.commit()

print("\nUm conjunto de dados incluídos com sucesso!\n")

#cria uma lista com diversos dados
lista = [(
    'Fabio', 23, '44444444444', 'fabio@email.com', '1234-5678', 'Belo Horizonte', 'MG', '2014-06-09'),
    ('Joao', 21, '55555555555', 'joao@email.com', '11-1234-5600', 'Sao Paulo', 'SP', '2014-06-09'),
    ('Xavier', 24, '66666666666', 'xavier@email.com', '12-1234-5601', 'Campinas', 'SP', '2014-06-10'),
    ('Regis', 35, '00000000000', 'regis@email.com', '11-98765-4321', 'Sao Paulo', 'SP', '2014-06-08'),
    ('Aloisio', 87, '11111111111', 'aloisio@email.com', '98765-4322', 'Porto Alegre', 'RS', '2014-06-09'),
    ('Bruna', 21, '22222222222', 'bruna@email.com', '21-98765-4323', 'Rio de Janeiro', 'RJ', '2014-06-09'),
    ('Regis', 16, '88888888888', 'regislira@email.com', '11-96758-4321', 'Campina Grande', 'PB', '2014-06-08')]

#Insere todos os dados da lista de uma única ver na tabela
cursor.executemany("""
INSERT INTO clientes (nome, idade, cpf, email, fone, cidade, uf, criado_em)
VALUES (?,?,?,?,?,?,?,?)
""", lista)

#Salva dados no banco
conn.commit()

print("\nDiversos conjuntos de dados inseridos com sucesso!\n")

#Socilicitando dados do usuário
p_nome = input("Nome: ")
p_idade = input("Idade: ")
p_cpf = input("CPF: ")
p_email = input("Email: ")
p_fone = input("Fone: ")
p_cidade = input("Cidade: ")
p_uf = input("UF: ")
p_criado_em = input("Criado em (yyyy-mm-dd): ")

#inserindo dados na tabela
cursor.execute("""
INSERT INTO clientes (nome, idade, cpf, email, fone, cidade, uf, criado_em)
VALUES (?,?,?,?,?,?,?,?)
""", (p_nome, p_idade, p_cpf, p_email, p_fone, p_cidade, p_uf, p_criado_em))

conn.commit()

print("\nDados inseridos com sucesso.\n")

# lendo todos os dados 
cursor.execute("""
SELECT * FROM clientes;
""")

#Imprimindo todos os dados
print("\nImprimindo todos os dados: \n")
for linha in cursor.fetchall():
    print(linha,  "\n")

#atribui a uma variavél um tipo de busca com o SELECT de leitura de dados
sql = "SELECT * FROM clientes WHERE nome=?"

#Realiza a busca pelo nome Regis
cursor.execute(sql, [("Regis")])

#Imprime todos os resultados encontrados
print ("\nTodos os dados encontrados com o nome 'Regis': \n", cursor.fetchall())

#Imprime apenas o primeiro resultado encontrado
print ("\nPrimeiro dado encontrado com o nome 'Regis': \n", cursor.fetchone())

#Imprime todos os dados em ordem ascendente
print ("\nLista de todos os registros na tabela em ordem ascendente:\n")
for row in cursor.execute("SELECT rowid, * FROM clientes ORDER BY nome"):
   print (row, "\n")

#Realiza busca com o comando LIKE que busca frases parciais nos dados
print ("\nResultados de uma consulta parcial pelo inicio de fone 11:\n")
sql = """
SELECT * FROM clientes
WHERE fone LIKE '11%'"""
cursor.execute(sql)
for busca in cursor.fetchall():
    print(busca,  "\n")

print("\nBuscas feitas com sucesso!\n")

#Definindo dados para atualizar a tabela
id_cliente = 1
novo_fone = "11-1000-2014"
novo_criado_em = "2014-06-11"

# alterando os dados da tabela
cursor.execute("""
UPDATE clientes
SET fone = ?, criado_em = ?
WHERE id = ?
""", (novo_fone, novo_criado_em, id_cliente))

conn.commit()

print("\nDados atualizados com sucesso.\n")



# excluindo um registro da tabela
cursor.execute("""
DELETE FROM clientes
WHERE id = 8
""")

conn.commit()

print("\nRegistro excluido com sucesso.\n")

#Adicionando uma nova coluna na tabela de clientes
cursor.execute("""
ALTER TABLE clientes
ADD COLUMN bloqueado BOOLEAN;
""")

conn.commit()

print("\nNovo campo adicionado com sucesso.\n")

#Definindo a variavél nome_tabela
nome_tabela = "clientes"

# obtendo informações da tabela com o PRAGMA
cursor.execute('PRAGMA table_info({})'.format(nome_tabela))

colunas = [tupla[1] for tupla in cursor.fetchall()]

#Imprimindo cada coluna da tabela
for coluna in colunas:
    print("    ", coluna)

# listando as tabelas do bd
cursor.execute("""
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
""")

print("\nTabelas: \n")
for tabela in cursor.fetchall():
    print("   %s\n" %(tabela))

# obtendo o schema da tabela
cursor.execute("""
SELECT sql FROM sqlite_master WHERE type='table' AND name=?
""", (nome_tabela,))

print("\nSchema:\n", cursor.fetchall())

#Fazendo backup do banco de dados
    #Comando with diminui acoplamento temporal, que acontece quando uma coisa precisa
    #ser feita depois de outra, mesmo que seja dentro do mesmo módulo ou função.
with io.open("clientes_dump.sql", "w") as f:
    for linha in conn.iterdump():
        f.write("%s\n" %(linha))

print("\nBackup realizado com sucesso.")
print("Salvo como clientes_dump.sql\n")

#desconectando
conn.close()

#Conectando o backup
conn = sqlite3.connect("clientes_recuperado.db")

cursor = conn.cursor()

#Recupera backup
f = io.open("clientes_dump.sql", "r")
sql = f.read()
cursor.executescript(sql)

print("\nBanco de dados recuperado com sucesso.")
print("Salvo como clientes_recuperado.db\n")

conn.close()

print("\nExemplo concluído com sucesso!")
print("----------Fim do Programa---------\n")










