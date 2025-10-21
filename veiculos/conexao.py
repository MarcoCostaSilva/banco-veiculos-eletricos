import streamlit as st
import mysql.connector
from mysql.connector import Error
import os

@st.cache_resource
def conectar():
    """
    Cria e retorna uma conexão segura com o banco de dados MySQL (Aiven Cloud),
    usando credenciais armazenadas em st.secrets e certificado SSL (ca.pem).
    """
    try:
        # Caminho dinâmico para o arquivo ca.pem (funciona no Streamlit Cloud)
        caminho_ca = os.path.join(os.path.dirname(__file__), "ca.pem")

        conexao = mysql.connector.connect(
            host=st.secrets["MYSQL_HOST"],
            port=st.secrets["MYSQL_PORT"],
            user=st.secrets["MYSQL_USER"],
            password=st.secrets["MYSQL_PASSWORD"],
            database=st.secrets["MYSQL_DB"],
            ssl_ca=caminho_ca,
            ssl_verify_cert=True
        )

        if conexao.is_connected():
            print("✅ Conexão bem-sucedida com o banco de dados Aiven.")
            return conexao

    except Error as e:
        st.error(f"❌ Erro ao conectar ao banco de dados: {e}")
        return None


def executar_query(query):
    """
    Executa consultas SQL de leitura (SELECT) e retorna os resultados em formato de lista de dicionários.
    """
    conexao = conectar()
    if conexao is None:
        return []

    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except Error as e:
        st.error(f"Erro ao executar consulta: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()


def executar_comando(query, valores=None):
    """
    Executa comandos SQL de escrita (INSERT, UPDATE, DELETE).
    """
    conexao = conectar()
    if conexao is None:
        return False

    cursor = conexao.cursor()
    try:
        cursor.execute(query, valores)
        conexao.commit()
        return True
    except Error as e:
        st.error(f"Erro ao executar comando: {e}")
        return False
    finally:
        cursor.close()
import streamlit as st
import mysql.connector
from mysql.connector import Error
import os

@st.cache_resource
def conectar():
    """
    Cria e retorna uma conexão segura com o banco de dados MySQL (Aiven Cloud),
    usando credenciais armazenadas em st.secrets e certificado SSL (ca.pem).
    """
    try:
        # Caminho dinâmico para o arquivo ca.pem (funciona no Streamlit Cloud)
        caminho_ca = os.path.join(os.path.dirname(__file__), "ca.pem")

        conexao = mysql.connector.connect(
            host=st.secrets["MYSQL_HOST"],
            port=st.secrets["MYSQL_PORT"],
            user=st.secrets["MYSQL_USER"],
            password=st.secrets["MYSQL_PASSWORD"],
            database=st.secrets["MYSQL_DB"],
            ssl_ca=caminho_ca,
            ssl_verify_cert=True
        )

        if conexao.is_connected():
            print("✅ Conexão bem-sucedida com o banco de dados Aiven.")
            return conexao

    except Error as e:
        st.error(f"❌ Erro ao conectar ao banco de dados: {e}")
        return None


def executar_query(query):
    """
    Executa consultas SQL de leitura (SELECT) e retorna os resultados em formato de lista de dicionários.
    """
    conexao = conectar()
    if conexao is None:
        return []

    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except Error as e:
        st.error(f"Erro ao executar consulta: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()


def executar_comando(query, valores=None):
    """
    Executa comandos SQL de escrita (INSERT, UPDATE, DELETE).
    """
    conexao = conectar()
    if conexao is None:
        return False

    cursor = conexao.cursor()
    try:
        cursor.execute(query, valores)
        conexao.commit()
        return True
    except Error as e:
        st.error(f"Erro ao executar comando: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()
