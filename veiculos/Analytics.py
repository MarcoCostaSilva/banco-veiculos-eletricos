import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------- CONFIGURAÇÃO -------------------
st.set_page_config(page_title="Analytics - Veículos Elétricos", layout="wide")
st.title("📈 Analytics - Veículos Elétricos")
st.sidebar.header("🔍 Filtros de Análise")

# ------------------- CONEXÃO DIRETA (SEM SEGREDOS!) -------------------
@st.cache_resource
def get_conn():
    import mysql.connector
    return mysql.connector.connect(
        host="mysql-118d8839-marco-50c4.g.aivencloud.com",
        user="avnadmin",
        password="AVNS_XrYI6baKiKmZXQRgGpg",
        database="veiculos_eletricos",
        port=11895,
        ssl_ca="ca.pem",
        ssl_verify_cert=True
    )

conn = get_conn()

# ------------------- FUNÇÕES -------------------
def adicionar_opcao_todos(lista):
    return ["Todos"] + lista

def sql_in_list(int_list):
    return "(" + ",".join(str(x) for x in int_list) + ")"

@st.cache_data
def carregar(sql):
    return pd.read_sql(sql, conn)

# ------------------- FILTROS -------------------
regioes_df = carregar("SELECT id_regiao, regiao FROM regiao ORDER BY regiao")
regioes_opts = adicionar_opcao_todos(regioes_df['regiao'].tolist())
regioes_sel = st.sidebar.multiselect("🌎 Região", regioes_opts)

if regioes_sel and "Todos" not in regioes_sel:
    ids_reg = regioes_df[regioes_df['regiao'].isin(regioes_sel)]['id_regiao'].tolist()
    estados_df = carregar(f"SELECT id_estado, estado, uf FROM estado WHERE id_regiao IN {sql_in_list(ids_reg)} ORDER BY uf")
else:
    estados_df = carregar("SELECT id_estado, estado, uf FROM estado ORDER BY uf")
estados_opts = adicionar_opcao_todos(estados_df['estado'].tolist())
estados_sel = st.sidebar.multiselect("🏛️ Estado", estados_opts)

if estados_sel and "Todos" not in estados_sel:
    ids_est = estados_df[estados_df['estado'].isin(estados_sel)]['id_estado'].tolist()
    cidades_df = carregar(f"SELECT id_cidade, cidade FROM cidade WHERE id_estado IN {sql_in_list(ids_est)} ORDER BY cidade")
else:
    cidades_df = carregar("SELECT id_cidade, cidade FROM cidade ORDER BY cidade")
cidades_opts = adicionar_opcao_todos(cidades_df['cidade'].tolist())
cidades_sel = st.sidebar.multiselect("🏙️ Cidade", cidades_opts)

classif_df = carregar("SELECT id_classificacao, classificacao FROM classificacao_veiculo ORDER BY classificacao")
classif_opts = adicionar_opcao_todos(classif_df['classificacao'].tolist())
classif_sel = st.sidebar.multiselect("🚗 Classificação", classif_opts)

tec_df = carregar("SELECT id_tecnologia, tecnologia FROM tecnologia ORDER BY tecnologia")
tec_opts = adicionar_opcao_todos(tec_df['tecnologia'].tolist())
tec_sel = st.sidebar.multiselect("⚡ Tecnologia", tec_opts)

# ------------------- BOTÕES -------------------
st.sidebar.markdown("---")
col1, col2 = st.sidebar.columns(2)
btn_pesquisar = col1.button("🔍 **PESQUISAR**", use_container_width=True)
btn_limpar = col2.button("🧹 **LIMPAR**", use_container_width=True)

if btn_limpar:
    st.rerun()

# ------------------- RESULTADOS -------------------
if btn_pesquisar:
    query = """
    SELECT c.cidade, m.modelo, ct.quantidade, t.tecnologia, cv.classificacao
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
        st.warning("⚠️ Nenhum resultado encontrado.")
    else:
        total_veiculos = df['quantidade'].sum()
        modelos_unicos = df['modelo'].nunique()
        top_tecnologia = df.groupby('tecnologia')['quantidade'].sum().idxmax()

        # KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("🚗 Total Veículos", f"{total_veiculos:,}")
        col2.metric("📋 Modelos Únicos", modelos_unicos)
        col3.metric("⚡ Top Tecnologia", top_tecnologia)

        # GRÁFICOS
        st.subheader("📊 **VISUALIZAÇÕES**")
        
        col_a, col_b = st.columns(2)
        with col_a:
            df_cidade = df.groupby('cidade', as_index=False)['quantidade'].sum()
            fig1 = px.bar(df_cidade, x='cidade', y='quantidade', title="Veículos por Cidade")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col_b:
            df_modelo = df.groupby('modelo', as_index=False)['quantidade'].sum()
            fig2 = px.bar(df_modelo, x='modelo', y='quantidade', title="Veículos por Modelo")
            st.plotly_chart(fig2, use_container_width=True)

        col_c, col_d = st.columns(2)
        with col_c:
            df_tec = df.groupby('tecnologia', as_index=False)['quantidade'].sum()
            fig3 = px.pie(df_tec, names='tecnologia', values='quantidade', title="Tecnologia")
            st.plotly_chart(fig3, use_container_width=True)
        
        with col_d:
            df_class = df.groupby('classificacao', as_index=False)['quantidade'].sum()
            fig4 = px.pie(df_class, names='classificacao', values='quantidade', title="Classificação")
            st.plotly_chart(fig4, use_container_width=True)

        # DOWNLOAD
        st.markdown("---")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 **DOWNLOAD CSV**", csv, "analytics.csv", "text/csv")

else:
    st.info("👆 Selecione os filtros e clique em **PESQUISAR**")