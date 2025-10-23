# Banco de Dados Relacional e Plataforma de Visualização para Análise Estatística de Veículos Elétricos no Brasil

---

## Visão Geral

Este repositório implementa um sistema completo de integração e análise de dados sobre a frota de veículos elétricos e híbridos no Brasil, desenvolvido como projeto de Iniciação Científica no Bacharelado em Estatística pelo Centro Universitário das Faculdades Metropolitanas Unidas (FMU). O escopo abrange a coleta, padronização e modelagem de dados provenientes do Sistema Nacional de Trânsito (SENATRAN), disponibilizados via plataforma Fórum VE, resultando em um banco de dados relacional MySQL com 487.114 registros até maio de 2025.

A plataforma utiliza Python com Streamlit para interfaces web interativas, Pandas para processamento de dados, Plotly para visualizações dinâmicas e SQL parametrizado para consultas otimizadas. As análises focam em dimensões espaciais (distribuição por região/estado/cidade), tecnológicas (BEV, PHEV, HEV, FCEV, MHEV etc.), temporais (evolução desde 1973) e de mercado (fabricantes e modelos). Os resultados subsidiam políticas públicas alinhadas aos ODS 7, 9, 11, 12 e 13, e programas nacionais como Rota 2030, PNME e PNE 2050.

**Estatísticas Principais:**
- **Frota Total**: 487.114 veículos.
- **Fabricantes**: 123, com liderança da BYD (33,6%).
- **Modelos**: 560, destacando BYD Dolphin Mini GL EV e Toyota Corolla Hybrid.
- **Distribuição Espacial**: Concentração no Sudeste/Sul (ex.: São Paulo, DF, RJ); baixa penetração no Norte/Nordeste.
- **Evolução Temporal**: Fases de introdução (1973-2001), crescimento moderado (2002-2017) e expansão acelerada (2018-2025).

O repositório promove reprodutibilidade, com código-fonte, scripts de ETL, banco de dados modelado e deploy configurado para Streamlit Cloud. Contribuições são bem-vindas via pull requests, seguindo as diretrizes de código limpo e testes unitários.

---

## Objetivos

### Objetivo Geral
Implementar um banco de dados relacional em MySQL para consolidação, validação e análise estatística de dados de veículos elétricos, integrado a uma plataforma de visualização com dashboards interativos e relatórios automatizados, facilitando a exploração de tendências e suporte a decisões baseadas em evidências.

### Objetivos Específicos
- Coletar e padronizar dados do SENATRAN/Fórum VE, aplicando normalização e tratamento de inconsistências.
- Projetar esquema relacional com integridade referencial (chaves primárias/estrangeiras, índices compostos).
- Hospedar em ambiente MySQL remoto com SSL (Aiven Cloud) e consultas parametrizadas para eficiência.
- Desenvolver interfaces Streamlit com filtros multinível, agregações Pandas e renderização Plotly.
- Gerar relatórios exportáveis (CSV, Excel, DOCX, PDF) via bibliotecas como openpyxl e fpdf.
- Documentar pipeline de ETL e análises para reprodutibilidade acadêmica e industrial.

---

## Arquitetura do Sistema

O sistema segue uma arquitetura em camadas:

1. **Camada de Dados**: Banco MySQL com tabelas normalizadas (ex.: `regiao`, `estado`, `cidade`, `modelo`, `tecnologia`, `cidade_tipo_modelo` com agregações de quantidade).
2. **Camada de Processamento**: Scripts Python para ETL (Extração via API Fórum VE, Transformação com Pandas, Carga via mysql-connector-python).
3. **Camada de Apresentação**: Aplicações Streamlit com cache (@st.cache_data/resource) para queries e renderização dinâmica.
4. **Integração**: Conexão SSL segura; deploy em Streamlit Cloud com secrets.toml.

Diagrama conceitual do esquema de dados (insira imagem aqui, gerada via PlantUML ou Draw.io, e commite como `./docs/er_diagram.png`):

<img width="1088" height="653" alt="DER_ORIGINAL" src="https://github.com/user-attachments/assets/2e1749ca-8fd3-4771-936e-1902df313fb2" />


---
### requirements.txt
```plaintext
streamlit==1.50.0
pandas==2.2.3
plotly==5.24.1
mysql-connector-python==9.0.0
python-docx==1.1.2
fpdf==1.7.2
openpyxl==3.1.3
geopandas==0.14.0  # Para análise espacial no Dashboard
folium==0.15.2     # Para mapas interativos

