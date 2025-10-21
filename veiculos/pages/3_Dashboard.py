import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from conexao import conectar  # <-- conexão Aiven adicionada

# ------------------- CONFIGURAÇÃO GERAL -------------------
st.set_page_config(page_title="Dashboard - Veículos Elétricos", layout="wide")

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2em;
        font-weight: 700;
        color: #1a5130;
        text-align: center;
        margin-bottom: -10px;
    }
    .subtitle {
        font-size: 1.3em;
        color: #4a7856;
        text-align: center;
        margin-bottom: 10px;
    }
    .btn-green {
        background-color: #28a745;
        color: white;
        font-weight: bold;
        width: 100%;
        padding: 0.5rem;
        border: none;
        border-radius: 0.25rem;
        cursor: pointer;
    }
    .btn-red {
        background-color: #dc3545;
        color: white;
        font-weight: bold;
        width: 100%;
        padding: 0.5rem;
        border: none;
        border-radius: 0.25rem;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<p class="main-title">📍 Distribuição Espacial dos Veículos Elétricos no Brasil</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Mapa Interativo de Distribuição por Estado</p>', unsafe_allow_html=True)

# ------------------- CONEXÃO COM O BANCO -------------------
conn = conectar()  # <-- apenas trocada a conexão, sem alterar mais nada

@st.cache_data
def carregar(sql):
    return pd.read_sql(sql, conn)

# ------------------- DADOS BASE -------------------
regioes_df = carregar("SELECT id_regiao, regiao FROM regiao ORDER BY regiao;")
estados_df = carregar("SELECT id_estado, uf, estado, id_regiao FROM estado ORDER BY uf;")
tecnologias_df = carregar("SELECT id_tecnologia, tecnologia FROM tecnologia ORDER BY tecnologia;")
classificacoes_df = carregar("SELECT id_classificacao, classificacao FROM classificacao_veiculo ORDER BY classificacao;")
anos_df = carregar("SELECT DISTINCT ano_inicial FROM cidade_tipo_modelo ORDER BY ano_inicial;")
meses_df = pd.DataFrame({'mes': list(range(1, 13))})

# ------------------- SIDEBAR - FILTROS -------------------
st.sidebar.header("Filtros")

def adicionar_opcao_todos(lista):
    return ["Todos"] + lista

with st.sidebar.expander("📍 Filtros Geográficos"):
    regioes_opts = adicionar_opcao_todos(regioes_df['regiao'].tolist())
    regioes_sel = st.multiselect("Região", regioes_opts, default=["Todos"])

    if regioes_sel and "Todos" not in regioes_sel:
        ids_reg = regioes_df[regioes_df['regiao'].isin(regioes_sel)]['id_regiao'].tolist()
        estados_sel_df = estados_df[estados_df['id_regiao'].isin(ids_reg)]
    else:
        estados_sel_df = estados_df.copy()
    estados_opts = adicionar_opcao_todos(estados_sel_df['uf'].tolist())
    estados_sel = st.multiselect("Estado", estados_opts, default=["Todos"])

with st.sidebar.expander("⚙️ Filtros Técnicos"):
    tecnologias_opts = adicionar_opcao_todos(tecnologias_df['tecnologia'].tolist())
    tecnologias_sel = st.multiselect("Tecnologia", tecnologias_opts, default=["Todos"])

    classificacoes_opts = adicionar_opcao_todos(classificacoes_df['classificacao'].tolist())
    classificacoes_sel = st.multiselect("Classificação", classificacoes_opts, default=["Todos"])

    anos_opts = adicionar_opcao_todos(anos_df['ano_inicial'].astype(str).tolist())
    anos_sel = st.multiselect("Ano", anos_opts, default=["Todos"])

    meses_opts = adicionar_opcao_todos([str(m) for m in meses_df['mes']])
    meses_sel = st.multiselect("Mês", meses_opts, default=["Todos"])

# ------------------- BOTÕES -------------------
st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)

pesquisar = col1.button("Pesquisar", use_container_width=True)
limpar = col2.button("Limpar", use_container_width=True)

if limpar:
    st.session_state.clear()
    st.experimental_rerun()

# ------------------- CONSULTA PRINCIPAL -------------------
if pesquisar:
    query = """
    SELECT 
        e.uf,
        e.estado,
        r.regiao,
        SUM(ctm.quantidade) AS total_veiculos
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
    if anos_sel and "Todos" not in anos_sel:
        anos_n = [int(a) for a in anos_sel if a != "Todos"]
        query += f" AND ctm.ano_inicial IN {tuple(anos_n)}"
    if meses_sel and "Todos" not in meses_sel:
        meses_n = [int(m) for m in meses_sel if m != "Todos"]
        query += f" AND ctm.mes IN {tuple(meses_n)}"

    query += " GROUP BY e.uf, e.estado, r.regiao ORDER BY total_veiculos DESC;"

    df = carregar(query)

    if df.empty:
        st.warning("⚠️ Nenhum resultado encontrado para os filtros aplicados.")
    else:
        total_veiculos = int(df['total_veiculos'].sum())
        st.success(f"✅ {total_veiculos} veículos encontrados.")

        st.subheader("🗺️ Mapa de Distribuição de Veículos Elétricos por Estado")
        st.markdown(f"**Total de veículos:** {total_veiculos}", unsafe_allow_html=True)

        # ------------------- GEOJSON -------------------
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

        df['lat'] = df['uf'].map(lambda x: centros_estados.get(x)[0])
        df['lon'] = df['uf'].map(lambda x: centros_estados.get(x)[1])

        fig = px.choropleth(
            df,
            geojson=geojson,
            locations='uf',
            featureidkey='properties.sigla',
            color='total_veiculos',
            color_continuous_scale=['#dff0d8', '#7fc97f', '#1a5130'],
            scope='south america',
            hover_name='estado',
            hover_data={'total_veiculos': True, 'uf': False},
            labels={'total_veiculos': 'Total de Veículos'}
        )

        fig.update_traces(marker_line_width=0.4, marker_line_color='gray')
        fig.update_geos(fitbounds="locations", visible=False)

        fig.add_trace(go.Scattergeo(
            lon=df['lon'],
            lat=df['lat'],
            text=df['estado'] + ': ' + df['total_veiculos'].astype(int).astype(str),
            mode='text',
            textfont=dict(size=11, color='black', family='Arial')
        ))

        fig.update_layout(
            width=2000,
            height=1500,
            margin={"r":0,"t":30,"l":0,"b":0},
            coloraxis_showscale=False,
            paper_bgcolor="#ffffff"
        )

        st.plotly_chart(fig, use_container_width=True)
