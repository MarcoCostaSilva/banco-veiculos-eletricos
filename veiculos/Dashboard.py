import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
import requests
import os

# ------------------- CONFIGURAÇÃO -------------------
st.set_page_config(page_title="Dashboard - Veículos Elétricos", layout="wide")
st.title("🗺️ Dashboard - Distribuição Espacial")

# ------------------- CONEXÃO -------------------
@st.cache_resource
def get_conn():
    caminho_ca = os.path.join(os.path.dirname(__file__), st.secrets["SSL_CA_PATH"])
    return mysql.connector.connect(
        host=st.secrets["MYSQL_HOST"],
        user=st.secrets["MYSQL_USER"],
        password=st.secrets["MYSQL_PASSWORD"],
        database=st.secrets["MYSQL_DATABASE"],
        port=st.secrets["MYSQL_PORT"],
        ssl_ca=caminho_ca,
        ssl_verify_cert=True
    )

conn = get_conn()

@st.cache_data
def carregar(sql):
    return pd.read_sql(sql, conn)

# ------------------- DADOS BASE -------------------
regioes_df = carregar("SELECT id_regiao, regiao FROM regiao ORDER BY regiao")
estados_df = carregar("SELECT id_estado, uf, estado, id_regiao FROM estado ORDER BY uf")
tecnologias_df = carregar("SELECT id_tecnologia, tecnologia FROM tecnologia ORDER BY tecnologia")
classificacoes_df = carregar("SELECT id_classificacao, classificacao FROM classificacao_veiculo ORDER BY classificacao")
anos_df = carregar("SELECT DISTINCT ano_inicial FROM cidade_tipo_modelo ORDER BY ano_inicial")

# ------------------- SIDEBAR FILTROS -------------------
st.sidebar.header("🔍 Filtros")

def adicionar_opcao_todos(lista):
    return ["Todos"] + lista

with st.sidebar.expander("📍 Geográficos"):
    regioes_opts = adicionar_opcao_todos(regioes_df['regiao'].tolist())
    regioes_sel = st.multiselect("Região", regioes_opts, default=["Todos"])
    
    if regioes_sel and "Todos" not in regioes_sel:
        ids_reg = regioes_df[regioes_df['regiao'].isin(regioes_sel)]['id_regiao'].tolist()
        estados_opts = adicionar_opcao_todos(estados_df[estados_df['id_regiao'].isin(ids_reg)]['uf'].tolist())
    else:
        estados_opts = adicionar_opcao_todos(estados_df['uf'].tolist())
    estados_sel = st.multiselect("Estado", estados_opts, default=["Todos"])

with st.sidebar.expander("⚙️ Técnicos"):
    tecnologias_opts = adicionar_opcao_todos(tecnologias_df['tecnologia'].tolist())
    tecnologias_sel = st.multiselect("Tecnologia", tecnologias_opts, default=["Todos"])
    
    classificacoes_opts = adicionar_opcao_todos(classificacoes_df['classificacao'].tolist())
    classificacoes_sel = st.multiselect("Classificação", classificacoes_opts, default=["Todos"])

# ------------------- BOTÕES -------------------
st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)
pesquisar = col1.button("🔍 Pesquisar")
limpar = col2.button("🧹 Limpar")

if limpar:
    st.rerun()

# ------------------- CONSULTA -------------------
if pesquisar:
    query = """
    SELECT e.uf, e.estado, r.regiao, SUM(ctm.quantidade) AS total_veiculos
    FROM cidade_tipo_modelo ctm
    JOIN cidade c ON ctm.id_cidade = c.id_cidade
    JOIN estado e ON c.id_estado = e.id_estado
    JOIN regiao r ON e.id_regiao = r.id_regiao
    JOIN tecnologia t ON ctm.id_tecnologia = t.id_tecnologia
    JOIN classificacao_veiculo cv ON ctm.id_classificacao = cv.id_classificacao
    WHERE 1=1
    """

    def sql_in_list(values): 
        return "(" + ",".join(f"'{v}'" for v in values) + ")"

    if regioes_sel and "Todos" not in regioes_sel:
        query += f" AND r.regiao IN {sql_in_list(regioes_sel)}"
    if estados_sel and "Todos" not in estados_sel:
        query += f" AND e.uf IN {sql_in_list(estados_sel)}"
    if tecnologias_sel and "Todos" not in tecnologias_sel:
        query += f" AND t.tecnologia IN {sql_in_list(tecnologias_sel)}"
    if classificacoes_sel and "Todos" not in classificacoes_sel:
        query += f" AND cv.classificacao IN {sql_in_list(classificacoes_sel)}"

    query += " GROUP BY e.uf, e.estado, r.regiao ORDER BY total_veiculos DESC"

    df = carregar(query)

    if df.empty:
        st.warning("⚠️ Nenhum resultado encontrado.")
    else:
        total_veiculos = int(df['total_veiculos'].sum())
        st.success(f"✅ {total_veiculos} veículos encontrados")

        # MAPA
        url = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
        geojson = requests.get(url).json()

        centros_estados = {
            'AC': (-9.97499, -67.8243), 'AL': (-9.5713, -36.782), 'AP': (1.4142, -51.770),
            'AM': (-3.4653, -62.2159), 'BA': (-12.5797, -41.7007), 'CE': (-5.4984, -39.3206),
            'DF': (-15.7797, -47.9297), 'ES': (-19.1834, -40.3085), 'GO': (-16.6864, -49.2643),
            'MA': (-4.9609, -44.2913), 'MT': (-12.6819, -55.6728), 'MS': (-20.7722, -54.7851),
            'MG': (-18.5122, -44.5553), 'PA': (-5.5307, -52.2304), 'PB': (-7.1153, -35.2381),
            'PR': (-24.8925, -51.5565), 'PE': (-8.0476, -34.877), 'PI': (-7.7189, -42.7289),
            'RJ': (-22.9068, -43.1729), 'RN': (-5.7945, -35.211), 'RS': (-30.0346, -51.2177),
            'RO': (-11.5057, -63.5806), 'RR': (2.8196, -60.6738), 'SC': (-27.5954, -48.548),
            'SP': (-23.5505, -46.6333), 'SE': (-10.9472, -37.0731), 'TO': (-10.2462, -48.3243)
        }

        df['lat'] = df['uf'].map(lambda x: centros_estados.get(x, (-15, -50))[0])
        df['lon'] = df['uf'].map(lambda x: centros_estados.get(x, (-15, -50))[1])

        fig = px.choropleth(
            df, geojson=geojson, locations='uf', featureidkey='properties.sigla',
            color='total_veiculos', color_continuous_scale=['#dff0d8', '#7fc97f', '#1a5130'],
            scope='south america', hover_name='estado', hover_data={'total_veiculos': True}
        )

        fig.update_traces(marker_line_width=0.4, marker_line_color='gray')
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(height=600, coloraxis_showscale=False)

        st.plotly_chart(fig, use_container_width=True)