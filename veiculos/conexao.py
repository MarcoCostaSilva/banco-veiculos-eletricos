import mysql.connector
import streamlit as st
import os

@st.cache_resource(show_spinner=True)
def conectar():
    """
    Cria e retorna uma conexão segura com o banco MySQL usando SSL.
    As credenciais e o caminho do certificado são obtidos do arquivo .streamlit/secrets.toml.
    """
    try:
        # Caminho do certificado CA
        caminho_ca = os.path.join(os.path.dirname(__file__), st.secrets["SSL_CA_PATH"])

        # Verifica se o certificado existe
        if not os.path.exists(caminho_ca):
            st.error(f"⚠️ Certificado SSL não encontrado no caminho: {caminho_ca}")
            return None

        # Conecta ao banco
        conexao = mysql.connector.connect(
            host=st.secrets["MYSQL_HOST"],
            user=st.secrets["MYSQL_USER"],
            password=st.secrets["MYSQL_PASSWORD"],
            database=st.secrets["MYSQL_DATABASE"],
            port=int(st.secrets.get("MYSQL_PORT", 3306)),
            ssl_ca=caminho_ca,
            ssl_verify_cert=True
        )

        if conexao.is_connected():
            st.success("🔐 Conexão segura com o banco estabelecida com sucesso!")
            return conexao
        else:
            st.error("❌ Falha ao conectar: conexão não foi estabelecida.")
            return None

    except mysql.connector.Error as e:
        st.error(f"❌ Erro ao conectar no banco: {e}")
        print(f"[DEBUG] Erro MySQL: {e}")
        try:
            if 'conexao' in locals() and conexao.is_connected():
                conexao.close()
        except:
            pass
        return None
