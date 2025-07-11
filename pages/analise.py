import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="📊 Análise", layout="wide")

# Verifica se a planilha foi carregada
if "df_contratos" not in st.session_state:
    st.warning("⚠️ Nenhuma planilha foi enviada. Vá até a página 📁 Enviar Planilha.")
    st.stop()

df = st.session_state["df_contratos"]

# Renomeia colunas para facilitar os filtros
df = df.rename(columns={
    "VALOR BRUTO (R$)": "Valor Bruto",
    "VALOR LIQUIDO (R$)": "Valor Líquido",
    "CUSTO EFETIVO (R$)": "Custo Efetivo",
    "CUSTO EXECUTADO": "Custo Executado",
    "CUSTO PREVISTO": "Custo Previsto",
    "DATA INICIO": "Data de Início",
    "DT Criação": "Data de Criação",
    "Data de Ingresso no MS": "Data de Ingresso"
})

# Tratamentos
df['Data de Nascimento'] = pd.to_datetime(df['Data de Nascimento'], errors='coerce')
df['Idade'] = df['Data de Nascimento'].apply(lambda d: datetime.now().year - d.year if pd.notnull(d) else None)
df['Faixa Etária'] = pd.cut(df['Idade'], bins=[0, 17, 29, 39, 49, 59, 69, 79, 200],
                            labels=["0-17", "18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"])

# --- SIDEBAR ---
with st.sidebar:
    st.image("assets/logo.png", use_container_width=True)
    st.page_link("app.py", label="Enviar Planilha", icon="📂")
    st.page_link("pages/analise.py", label="Análise", icon="📊")

    st.header("🔍 Filtros")

    with st.expander("Fatores do Contrato"):
        st.multiselect("ID Contratos", options=df["ID Contratos"].dropna().unique())
        st.multiselect("Status", options=df["STATUS"].dropna().unique())
        st.multiselect("Nº PEP", options=df["Nº PEP"].dropna().unique())
        st.multiselect("Departamento", options=df["DEPARTAMENTO"].dropna().unique())
        st.multiselect("Coordenação", options=df["COORDENAÇÃO"].dropna().unique())
        st.date_input("Data de Criação", value=(df["Data de Criação"].min(), df["Data de Criação"].max()))

    with st.expander("Fatores do Contratado"):
        st.multiselect("CPF", options=df["CPF"].dropna().unique())
        st.multiselect("Sexo", options=df["Sexo"].dropna().unique())
        st.multiselect("Vínculo", options=df["VÍNCULO"].dropna().unique())
        st.slider("Idade", int(df["Idade"].min()), int(df["Idade"].max()))
        st.multiselect("Faixa Etária", options=df["Faixa Etária"].dropna().unique())

    with st.expander("Fatores do Tempo"):
        st.selectbox("Com Data de Ingresso", options=["Sim", "Não"])
        st.date_input("Data de Ingresso", value=(df["Data de Ingresso"].min(), df["Data de Ingresso"].max()))
        st.selectbox("Com Data de Início", options=["Sim", "Não"])
        st.date_input("Data de Início", value=(df["Data de Início"].min(), df["Data de Início"].max()))
        st.selectbox("Com Data de Fim", options=["Sim", "Não"])
        st.date_input("Data de Fim", value=(df["DATA FIM"].min(), df["DATA FIM"].max()))

    with st.expander("Fatores Financeiros"):
        st.slider("Valor Bruto", float(df["Valor Bruto"].min()), float(df["Valor Bruto"].max()))
        st.slider("Valor Líquido", float(df["Valor Líquido"].min()), float(df["Valor Líquido"].max()))
        st.slider("Custo Efetivo", float(df["Custo Efetivo"].min()), float(df["Custo Efetivo"].max()))
        st.slider("Custo Executado", float(df["Custo Executado"].min()), float(df["Custo Executado"].max()))
        st.slider("Custo Previsto", float(df["Custo Previsto"].min()), float(df["Custo Previsto"].max()))


# --- CABEÇALHO COM DEGRADÊ ---
st.markdown("""
    <div style='background: linear-gradient(to right, #004e92, #000428); padding: 40px; border-radius: 12px; margin-bottom:30px'>
        <h1 style='color: white;'>📊 Análise de Contratos SAES</h1>
        <p style='color: white;'>Explore custos, prazos e KPIs com filtros interativos.</p>
    </div>
""", unsafe_allow_html=True)

# --- SELEÇÃO DE TIPO DE ANÁLISE ---
aba = st.tabs([
    "🔢 Análise descritiva por número",
    "💰 Análise descritiva por valores",
    "📈 Análise preditiva temporal",
    "🤖 Análise preditiva de contratação"
])

with aba[0]:
    st.info("Conteúdo da Análise descritiva por número — (em construção)")

with aba[1]:
    st.info("Conteúdo da Análise descritiva por valores — (em construção)")

with aba[2]:
    st.info("Conteúdo da Análise preditiva temporal — (em construção)")

with aba[3]:
    st.info("Conteúdo da Análise preditiva de contratação — (em construção)")