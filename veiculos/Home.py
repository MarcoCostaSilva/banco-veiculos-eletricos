import streamlit as st

# ------------------- Configuração da Página -------------------
st.set_page_config(
    page_title="Home - Mobilidade Elétrica",
    layout="wide",
    page_icon="⚡"
)

# ------------------- Estilos Customizados -------------------
st.markdown("""
    <style>
        .title-main { font-size: 3em; font-weight: 700; color: #1a5130; text-align: center; margin-bottom: 10px; }
        .subtitle { font-size: 1.6em; color: #4a7856; text-align: center; margin-bottom: 30px; }
        .card { background-color: #EAF6EA; padding: 25px; border-radius: 10px; margin-bottom: 25px; }
        .card-title { font-size: 1.6em; font-weight: 700; color: #1a5130; margin-bottom: 10px; }
        .card-content { font-size: 1.2em; color: #333333; }
        .link-btn { color: white; background-color: #4a7856; border-radius: 6px; padding: 6px 14px; text-decoration: none; font-size: 1em; font-weight: 600; display: inline-block; margin: 8px 4px; }
        .link-btn:hover { background-color: #3a5a3f; }
    </style>
""", unsafe_allow_html=True)

# ------------------- Título e Subtítulo -------------------
st.markdown('<p class="title-main">⚡ Mobilidade Elétrica no Brasil</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Banco de Dados, Análises e Visualizações sobre Veículos Elétricos</p>', unsafe_allow_html=True)

# ------------------- Seção: Sobre o Projeto -------------------
st.markdown("""
    <div class="card">
        <p class="card-title">🌱 Sobre o Projeto</p>
        <p class="card-content">
            Este projeto consolida dados de veículos elétricos no Brasil para análise espacial, temporal e tecnológica,
            apoiando políticas públicas e ODS relacionados à energia limpa, inovação tecnológica e sustentabilidade urbana.
            <br><br><strong>Projeto de Iniciação Científica promovido pelo Centro Universitário das Faculdades Metropolitanas Unidas - FMU</strong>
        </p>
    </div>
""", unsafe_allow_html=True)

# ------------------- Seção: ODS e Políticas -------------------
st.markdown("""
    <div class="card">
        <p class="card-title">🌍 Alinhamento com Políticas Públicas e ODS</p>
        <p class="card-content">
            ODS 7: Energia Acessível e Limpa ⚡<br>
            ODS 9: Indústria, Inovação e Infraestrutura 🏭<br>
            ODS 11: Cidades e Comunidades Sustentáveis 🏙️<br>
            ODS 12: Consumo e Produção Responsáveis ♻️<br>
            ODS 13: Ação Contra a Mudança Global do Clima 🌎<br>
            Políticas nacionais: Rota 2030, PNME, PNE 2050
        </p>
    </div>
""", unsafe_allow_html=True)

# ------------------- Seção: Equipe e Contatos -------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="card" style="text-align:center;">
            <p class="card-title">👨💻 Marco Aurélio Costa da Silva</p>
            <p class="card-content">
                Pesquisador<br>Analista de Dados, Graduando em Estatística<br>
                E-mail: marco.dev.data@gmail.com<br>
                <a href="https://www.linkedin.com/in/marco-costadasilva/" class="link-btn">LinkedIn</a>
                <a href="https://github.com/MarcoCostaDaSilva" class="link-btn">GitHub</a>
                <a href="https://lattes.cnpq.br/8887305754672433" class="link-btn">Lattes</a>
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card" style="text-align:center;">
            <p class="card-title">👨🏫 Eugênio Akihiro Nassu</p>
            <p class="card-content">
                Orientador<br>Doutor em Ciência da Computação<br>
                E-mail: eugenio.nassu@fmu.br<br>
                <a href="https://www.linkedin.com/in/eugenioakihironassu" class="link-btn">LinkedIn</a>
                <a href="http://lattes.cnpq.br/9722612257818611" class="link-btn">Lattes</a>
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #4a7856;'><strong>🚀 Acesse as análises:</strong></p>", unsafe_allow_html=True)
st.info("👉 [Analytics](https://analytics.streamlit.app) | 👉 [Dashboard](https://dashboard.streamlit.app) | 👉 [Relatórios](https://relatorios.streamlit.app)")