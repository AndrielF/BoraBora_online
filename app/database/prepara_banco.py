import mysql.connector
from mysql.connector import errorcode


print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin123'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS `usuarios`;")
cursor.execute("CREATE DATABASE `usuarios`;")
cursor.execute("USE `usuarios`;")

# criando tabelas
TABLES = {}
TABLES['Participantes'] = ('''
      CREATE TABLE `participantes` (
      `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
      `email` varchar(120) NOT NULL,
      `telefone` bigint(15) NOT NULL,
      `nome` varchar(120) NOT NULL,
      `cpf` varchar(12) NOT NULL,
      `nascimento` int(15) NOT NULL,
      `genero` varchar(30) NOT NULL,
      `usuario` varchar(30) NOT NULL,
      `senha` varchar(30) NOT NULL
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES['Organizadores'] = ('''
      CREATE TABLE `organizadores` (
      `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
      `email` varchar(120) NOT NULL,
      `telefone` bigint(15) NOT NULL,
      `nome` varchar(120) NOT NULL,
      `cnpj` varchar(20) NOT NULL,
      `ramo` varchar(30) NOT NULL,
      `usuario` varchar(30) NOT NULL,
      `senha` varchar(30) NOT NULL
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES['Eventos'] = ('''
      CREATE TABLE `eventos` (
      `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
      `titulo` varchar(120) NOT NULL,
      `data` varchar(60) NOT NULL,
      `local` varchar(120) NOT NULL,
      `descricao` varchar(120) NOT NULL,
      `ingressos` int(15) NOT NULL,
      `preco` int(15) NOT NULL,
      `organizador` varchar(30) NOT NULL
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')


for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo participantes
participantes_sql = 'INSERT INTO participantes (email, telefone, nome, cpf, nascimento, genero, usuario, senha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
participantes = [
    ('andriel@email.com', '11999999999', 'Andriel', '12345678901', '02011999', 'Masculino', 'andriel', '123'),
    ('fernanda@email.com', '11999999999', 'Fernanda', '12345678901', '03011999', 'Feminino', 'fernanda', '123'),
    ('marcos@email.com', '11999999999', 'Marcos', '12345678901', '04011999', 'Masculino', 'marcos', '123'),
    ('lisandra@email.com', '11999999999', 'Lisandra', '12345678901', '01011999', 'Feminino', 'lisandra', '123'),
]
cursor.executemany(participantes_sql, participantes)

cursor.execute('select * from participantes')
print(' -------------  Participantes:  -------------')
for participante in cursor.fetchall():
    print(participante)


# inserindo organizadores
organizadores_sql = 'INSERT INTO organizadores (email, telefone, nome, cnpj, ramo, usuario, senha) VALUES (%s, %s, %s, %s, %s, %s, %s)'
organizadores = [
      ('empresa_pastel@email.com', '11999999999', 'Nome Empresa XYZ', '12345678901', 'pastel', 'empresa_pastel', '123'),
      ('graus_festas@email.com', '11999999999', 'Mil Grau Festas', '12345678901', 'graus', 'graus_festas', '123'),
      ('user_bla@email.com', '11999999999', 'nome_BlaBlaBla', '12345678901', 'ramo_blabla', 'user_bla', '123'),
]
cursor.executemany(organizadores_sql, organizadores)

cursor.execute('select * from organizadores')
print(' -------------  Organizadores:  -------------')
for organizado in cursor.fetchall():
    print(organizado)


# inserindo eventos
eventos_sql = 'INSERT INTO eventos (titulo, data, local, descricao, ingressos, preco, organizador) VALUES (%s, %s, %s, %s, %s, %s, %s)'
eventos = [
      ('Conferência de Tecnologia', '15 de março de 2023', 'Centro de Convenções', 'A conferência de tecnologia anual, com palestras de especialistas do setor.', '100', '100', 'empresa 1'),
      ('Exposição de Arte Moderna', '25 de abril de 2023', 'Museu de Arte Contemporânea', 'Uma exposição de arte moderna com obras de artistas locais e internacionais.', '200', '200', 'empresa 2'),
      ('Torneio de Golfe Beneficente', '8 de maio de 2023', 'Clube de Golfe da Cidade', 'Um torneio de golfe para arrecadar fundos para uma instituição de caridade local.', '300', '300', 'empresa 3'),
      ('Evento 4', '04012020', 'Local 4', 'Descrição 4', '400', '400', 'empresa 4'),
      ('Evento 5', '05012020', 'Local 5', 'Descrição 5', '500', '500', 'empresa 5'),
      ('Evento 6', '06012020', 'Local 6', 'Descrição 6', '600', '600', 'empresa 6'),
]
cursor.executemany(eventos_sql, eventos)

cursor.execute('select * from eventos')
print(' -------------  Eventos:  -------------')
for evento in cursor.fetchall():
      print(evento)


# commitando se não nada tem efeito
conn.commit()
cursor.close()
conn.close()
