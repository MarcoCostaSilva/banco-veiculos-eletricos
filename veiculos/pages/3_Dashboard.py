import streamlit as st
import pandas as pd
from conexao import conectar
import plotly.express as px

# ------------------- CONFIGURAÇÃO -------------------
st.set_page_config(page_title="Analytics - Veículos Elétricos", layout="wide")
st.markdown('<h1>📈 Analytics - Veículos Elétricos</h1>', unsafe_allow_html=True)
st.sidebar.header("Filtros de Análise")

# ------------------- CONEXÃO -------------------
conn = conectar()

# ------------------- CSS PARA ESTILO PROFISSIONAL -------------------
st.markdown("""
<style>
/* Botões */
div.stButton > button:first-child {
    font-weight: bold;
    border-radius: 10px;
    height: 45px;
    margin-top: 10px;
}
div.stButton > button#pesquisar {
    background-color: #1a5130 !important;
    color: white !important;
}
div.stButton > button#limpar {
    background-color: #4a7856 !important;
    color: white !important;
}
div.stButton > button:hover {
    opacity: 0.85;
}

/* Sidebar */
.stSidebar .css-1d391kg input, .stSidebar .css-1d391kg select {
    font-size: 1.1em;
}

/* Títulos e cards */
h1 {
    font-size: 2.5em;
    color: #1a5130;
    text-align: center;
}
h2 {
    font-size: 1.8em;
    color: #4a7856;
}
.kpi-card {
    background-color: #dff0d8;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
}
.kpi-value {
    font-size: 2.2em;
    font-weight: 700;
    color: #1a5130;
}
.kpi-label {
    font-size: 1.3em;
    color: #4a7856;
}
</style>
""", unsafe_allow_html=True)

# ------------------- FUNÇÕES AUXILIARES -------------------
def adicionar_opcao_todos(lista):
    return ["Todos"] + lista

def sql_in_list(int_list):
    return "(" + ",".join(str(x) for x in int_list) + ")"

@st.cache_data
def carregar(sql):
    return pd.read_sql(sql, conn)

# ------------------- CARREGAR OPÇÕES -------------------
regioes_df = carregar("SELECT id_regiao, regiao FROM regiao ORDER BY regiao")
regioes_opts = adicionar_opcao_todos(regioes_df['regiao'].tolist())
regioes_sel = st.sidebar.multiselect("Região", regioes_opts)

if regioes_sel and "Todos" not in regioes_sel:
    ids_reg = regioes_df[regioes_df['regiao'].isin(regioes_sel)]['id_regiao'].tolist()
    estados_df = carregar(f"SELECT id_estado, estado, uf FROM estado WHERE id_regiao IN {sql_in_list(ids_reg)} ORDER BY uf")
else:
    estados_df = carregar("SELECT id_estado, estado, uf FROM estado ORDER BY uf")
estados_opts = adicionar_opcao_todos(estados_df['estado'].tolist())
estados_sel = st.sidebar.multiselect("Estado", estados_opts)

if estados_sel and "Todos" not in estados_sel:
    ids_est = estados_df[estados_df['estado'].isin(estados_sel)]['id_estado'].tolist()
    cidades_df = carregar(f"SELECT id_cidade, cidade, id_estado FROM cidade WHERE id_estado IN {sql_in_list(ids_est)} ORDER BY cidade")
else:
    cidades_df = carregar("SELECT id_cidade, cidade, id_estado FROM cidade ORDER BY cidade")
cidades_opts = adicionar_opcao_todos(cidades_df['cidade'].tolist())
cidades_sel = st.sidebar.multiselect("Cidade", cidades_opts)

classif_df = carregar("SELECT id_classificacao, classificacao FROM classificacao_veiculo ORDER BY classificacao")
classif_opts = adicionar_opcao_todos(classif_df['classificacao'].tolist())
classif_sel = st.sidebar.multiselect("Classificação", classif_opts)

tec_df = carregar("SELECT id_tecnologia, tecnologia FROM tecnologia ORDER BY tecnologia")
tec_opts = adicionar_opcao_todos(tec_df['tecnologia'].tolist())
tec_sel = st.sidebar.multiselect("Tecnologia", tec_opts)

# ------------------- BOTÕES -------------------
st.sidebar.markdown("---")
col_btn1, col_btn2 = st.sidebar.columns(2)
btn_pesquisar = col_btn1.button("Pesquisar", key="pesquisar")
btn_limpar = col_btn2.button("Limpar Filtros", key="limpar")

if btn_limpar:
    st.session_state.clear()
    st.experimental_rerun()

# ------------------- EXECUÇÃO -------------------
if btn_pesquisar:
    query = """
    SELECT 
        c.cidade,
        m.modelo,
        ct.quantidade,
        t.tecnologia,
        cv.classificacao
    FROM cidade_tipo_modelo ct
    JOIN cidade c ON ct.id_cidade = c.id_cidade
    JOIN modelo m ON ct.id_modelo = m.id_modelo
    JOIN tecnologia t ON ct.id_tecnologia = t.id_tecnologia
    JOIN classificacao_veiculo cv ON ct.id_classificacao = cv.id_classificacao
    WHERE 1=1
    """

    if regioes_sel and "Todos" not in regioes_sel:
        ids_reg = regioes_df[regioes_df['regiao'].isin(regioes_sel)]['id_regiao'].tolist()
        query += f" AND c.id_estado IN (SELECT id_estado FROM estado WHERE id_regiao IN {sql_in_list(ids_reg)})"
    if estados_sel and "Todos" not in estados_sel:
        ids_est = estados_df[estados_df['estado'].isin(estados_sel)]['id_estado'].tolist()
        query += f" AND c.id_estado IN {sql_in_list(ids_est)}"
    if cidades_sel and "Todos" not in cidades_sel:
        ids_cid = cidades_df[cidades_df['cidade'].isin(cidades_sel)]['id_cidade'].tolist()
        query += f" AND c.id_cidade IN {sql_in_list(ids_cid)}"
    if classif_sel and "Todos" not in classif_sel:
        ids_cl = classif_df[classif_df['classificacao'].isin(classif_sel)]['id_classificacao'].tolist()
        query += f" AND cv.id_classificacao IN {sql_in_list(ids_cl)}"
    if tec_sel and "Todos" not in tec_sel:
        ids_tec = tec_df[tec_df['tecnologia'].isin(tec_sel)]['id_tecnologia'].tolist()
        query += f" AND t.id_tecnologia IN {sql_in_list(ids_tec)}"

    df = pd.read_sql(query, conn)

    if df.empty:
        st.warning("⚠️ Nenhum resultado encontrado para os filtros aplicados.")
    else:
        total_veiculos = df['quantidade'].sum()
        modelos_unicos = df['modelo'].nunique()
        top_tecnologia = df.groupby('tecnologia')['quantidade'].sum().idxmax()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_veiculos}</div>'
                        '<div class="kpi-label">Total Veículos</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="kpi-card"><div class="kpi-value">{modelos_unicos}</div>'
                        '<div class="kpi-label">Modelos Únicos</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="kpi-card"><div class="kpi-value">{top_tecnologia}</div>'
                        '<div class="kpi-label">Top Tecnologia</div></div>', unsafe_allow_html=True)

else:
    st.info("Selecione os filtros e clique em Pesquisar para visualizar os gráficos.")
