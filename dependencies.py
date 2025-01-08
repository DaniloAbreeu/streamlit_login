import psycopg2
from dotenv import load_dotenv
import os 
from contextlib import contextmanager 

load_dotenv()

DATABASE = os.getenv("DATABASE")
HOST = os.getenv("HOST")
USERSERVER = os.getenv("USERSERVER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")

@contextmanager
def instance_cursor():
    connection = psycopg2.connect(
        database=DATABASE,
        host=HOST,
        user=USERSERVER,
        password=PASSWORD,
        port=PORT,
        options="-c client_encoding=UTF8"
    )
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Conexão com PostgresSQL fechada")


def consulta_geral():
    with instance_cursor() as cursor:
        query= ''' 
            SELECT *
            FROM REGISTROS
            '''
        cursor.execute(query)
        request = cursor.fetchall()
        return request

def consulta_nome(user):
    with instance_cursor() as cursor: 
        query= '''
            SELECT nome, usuario, senha
            FROM REGISTROS
            WHERE usuario = %s
            '''
        cursor.execute(query, (user,))
        resquest = cursor.fetchall()
        return resquest

def criar_tabela():
    connection = psycopg2.connect(database=DATABASE, host=HOST, user=USERSERVER, password=PASSWORD, port=PORT)
    cursor = connection.cursor()

    query= '''
        CREATE TABLE REGISTROS (
            nome varchar(255),
            usuario varchar(255),
            senha varchar(255)
        ) 
        '''
    

    cursor.execute(query)
    connection.commit()
    print('Tabela criada')
    if (connection):
        cursor.close()
        connection.close()
        print("Conexão com PostgresSQL fechada")


def add_registro(nome, user, senha):
    connection = psycopg2.connect(database=DATABASE, host=HOST, user= USERSERVER, password= PASSWORD, port= PORT)
    cursor = connection.cursor()

    query= ''' 
        INSERT INTO REGISTROS (nome, user, senha)
        VALUES (%s, %s, %s)
        '''
    cursor.execute(query,(nome,user,senha))
    connection.commit()
    if (connection):
        cursor.close()
        connection.close()
        print("Conexão com PostgresSQL fechada")

