import mysql.connector
from mysql.connector import Error
import os
import streamlit as st

@st.cache_resource
def conectar():
    """
    Conecta ao banco Aiven MySQL com SSL usando st.secrets.
    """
    try:
        caminho_ca = os.path.join(os.path.dirname(__file__), st.secrets["SSL_CA_PATH"])
        conexao = mysql.connector.connect(
            host=st.secrets["MYSQL_HOST"],
            port=st.secrets["MYSQL_PORT"],
            user=st.secrets["MYSQL_USER"],
            password=st.secrets["MYSQL_PASSWORD"],
            database=st.secrets["MYSQL_DATABASE"],
            ssl_ca=caminho_ca,
            ssl_verify_cert=True
        )
        if conexao.is_connected():
            print("✅ Conexão bem-sucedida com o banco Aiven.")
            return conexao
    except Error as e:
        st.error(f"❌ Erro ao conectar: {e}")
        return None


def executar_query(query):
    conexao = conectar()
    if not conexao:
        return []

    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        st.error(f"Erro ao executar consulta: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()


def executar_comando(query, valores=None):
    conexao = conectar()
    if not conexao:
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
