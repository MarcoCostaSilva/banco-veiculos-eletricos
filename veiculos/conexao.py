import mysql.connector
import streamlit as st
import os

@st.cache_resource(show_spinner=True)
def conectar():
    """
    Retorna uma conexão MySQL segura usando SSL,
    pegando as credenciais do Streamlit secrets.
    """
    try:
        # caminho do certificado CA
        caminho_ca = os.path.join(os.path.dirname(__file__), st.secrets["SSL_CA_PATH"])

        conexao = mysql.connector.connect(
            host=st.secrets["MYSQL_HOST"],
            user=st.secrets["MYSQL_USER"],
            password=st.secrets["MYSQL_PASSWORD"],
            database=st.secrets["MYSQL_DATABASE"],
            port=int(st.secrets["MYSQL_PORT"]),
            ssl_ca=caminho_ca,
            ssl_verify_cert=True
        )
        return conexao

    except mysql.connector.Error as e:
        st.error(f"❌ Erro ao conectar no banco: {e}")
        return None
