import streamlit as st
import pandas as pd
from conexao import conectar
from io import BytesIO
from docx import Document
from fpdf import FPDF

# ------------------- CONFIGURAÇÃO -------------------
st.set_page_config(page_title="Relatórios - Veículos Elétricos", layout="wide")

# ------------------- ESTILOS -------------------
st.markdown("""
<style>
/* Títulos e subtítulos */
h1, .stTitle { font-size: 2.8em !important; color: #1a5130; text-align: center; margin-bottom: 15px; }
h2, .stSubheader { font-size: 1.8em !important; color: #1a5130; margin-bottom: 10px; }

/* Cards de KPIs */
.kpi-card { background-color: #EAF6EA; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
.kpi-value { font-size: 2.4em; font-weight: 700; color: #1a5130; }
.kpi-label { font-size: 1.2em; color: #4a7856; }

/* Cards de resultados e filtros */
.card { background-color: #F2F8F2; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
.card-title { font-size: 1.6em; font-weight: 700; color: #1a5130; margin-bottom: 10px; }
.card-content { font-size: 1.1em; color: #333333; }

/* Tabela Streamlit */
.dataframe tbody tr:nth-child(even) {background-color: #f3f9f3;}
.dataframe thead {background-color: #d1e7d1; color: #1a5130;}
</style>
""", unsafe_allow_html=True)

# ------------------- CONEXÃO -------------------
conn = conectar()

# ------------------- FUNÇÕES AUXILIARES -------------------
@st.cache_data
def carregar(sql):
    return pd.read_sql(sql, conn)

def adicionar_opcao_todos(lista):
    return ["Todos"] + lista

# ------------------- FILTROS -------------------
st.sidebar.header("Filtros para Relatórios")

regioes_df = carregar("SELECT id_regiao, regiao FROM regiao ORDER BY regiao")
regioes_opts = adicionar_opcao_todos(regioes_df['regiao'].tolist())
regioes_sel = st.sidebar.multiselect("Região", regioes_opts)

if regioes_sel and "Todos" not in regioes_sel:
    ids_reg = regioes_df[regioes_df['regiao'].isin(regioes_sel)]['id_regiao'].tolist()
    estados_df = carregar(f"SELECT id_estado, estado, uf FROM estado WHERE id_regiao IN ({','.join(map(str, ids_reg))}) ORDER BY uf")
else:
    estados_df = carregar("SELECT id_estado, estado, uf FROM estado ORDER BY uf")
estados_opts = adicionar_opcao_todos(estados_df['estado'].tolist())
estados_sel = st.sidebar.multiselect("Estado", estados_opts)

if estados_sel and "Todos" not in estados_sel:
    ids_est = estados_df[estados_df['estado'].isin(estados_sel)]['id_estado'].tolist()
    cidades_df = carregar(f"SELECT id_cidade, cidade FROM cidade WHERE id_estado IN ({','.join(map(str, ids_est))}) ORDER BY cidade")
else:
    cidades_df = carregar("SELECT id_cidade, cidade FROM cidade ORDER BY cidade")
cidades_opts = adicionar_opcao_todos(cidades_df['cidade'].tolist())
cidades_sel = st.sidebar.multiselect("Cidade", cidades_opts)

btn_gerar = st.sidebar.button("Gerar Relatório")

# ------------------- EXECUÇÃO -------------------
if btn_gerar:
    query = "SELECT c.cidade, m.modelo, ct.quantidade, t.tecnologia, cv.classificacao FROM cidade_tipo_modelo ct " \
            "JOIN cidade c ON ct.id_cidade=c.id_cidade " \
            "JOIN modelo m ON ct.id_modelo=m.id_modelo " \
            "JOIN tecnologia t ON ct.id_tecnologia=t.id_tecnologia " \
            "JOIN classificacao_veiculo cv ON ct.id_classificacao=cv.id_classificacao WHERE 1=1"
    
    if regioes_sel and "Todos" not in regioes_sel:
        query += f" AND c.id_estado IN (SELECT id_estado FROM estado WHERE id_regiao IN ({','.join(map(str, ids_reg))}))"
    if estados_sel and "Todos" not in estados_sel:
        query += f" AND c.id_estado IN ({','.join(map(str, ids_est))})"
    if cidades_sel and "Todos" not in cidades_sel:
        ids_cid = cidades_df[cidades_df['cidade'].isin(cidades_sel)]['id_cidade'].tolist()
        query += f" AND c.id_cidade IN ({','.join(map(str, ids_cid))})"

    df = pd.read_sql(query, conn)
    
    if df.empty:
        st.warning("⚠️ Nenhum resultado encontrado.")
    else:
        st.subheader("📊 Dados do Relatório")
        st.dataframe(df, use_container_width=True)
        
        # ------------------- EXPORTAÇÃO -------------------
        buffer_excel = BytesIO()
        df.to_excel(buffer_excel, index=False)
        st.download_button("⬇️ Exportar Excel", data=buffer_excel.getvalue(), file_name="relatorio.xlsx")
