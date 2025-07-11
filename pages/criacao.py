import streamlit as st
from PIL import Image

with st.sidebar:
    st.image("assets/logo.png", use_container_width=True)
    st.page_link("app.py", label="Enviar Planilha", icon="📂")
    st.page_link("pages/analise.py", label="Análise", icon="📊")
    st.page_link("pages/criacao.py", label="Referência", icon="✅")

# ---------------------------------------------------------------
# Cabeçalho com degradê
# ---------------------------------------------------------------

st.markdown("""
    <div style='background: linear-gradient(to right, #004e92, #000428); padding: 40px; border-radius: 12px; margin-bottom:30px'>
        <h1 style='color: white;'>📊 Análise de Contratos SAES</h1>
        <p style='color: white;'>Explore custos, prazos e KPIs com filtros interativos.</p>
    </div>
""", unsafe_allow_html=True)

st.title("✅ Referência")

# Caminho da imagem
imagem = Image.open("assets/lia.png")

# Exibir imagem com ajuste de largura
st.image(imagem, width=300, caption="Lia – Referência Técnica")

# Texto formatado
st.markdown("""
**Engenheira Agrônoma** formada pela Universidade de Brasília (2008), mestre em **Gestão de Políticas Públicas** pela Universidade Federal do Tocantins (2022), especialista em **Gestão do Trabalho e da Educação na Saúde**, pela Universidade Federal do Rio Grande do Norte (2019), cursando especialização em **Saúde Coletiva com concentração em Monitoramento, Avaliação e Informações Estratégicas**, pelo ISC/UFBA (atual), possui aperfeiçoamento em **Gestão de Residências Médicas** no Hospital Sírio Libanês (2014) e **MBA em Gestão Empresarial com Ênfase em Estratégia** pela Fundação Getúlio Vargas (2012).

Tem experiência de 2 anos em **gestão empresarial** e trabalhou durante 10 anos no **Ministério da Saúde**, de 2013 a 2023, desenvolvendo ações de planejamento, monitoramento e avaliação das Políticas Públicas voltadas para a Atenção Primária à Saúde.

Atualmente está na **Agência Brasileira de Apoio à Gestão do Sistema Único de Saúde (AgSUS)**, onde atua na área de **monitoramento e avaliação de Políticas Públicas para o SUS**.
""")