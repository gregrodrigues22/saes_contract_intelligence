import streamlit as st
import pandas as pd
import os
from utils.validar_planilha import validar_campos_obrigatorios

# Configuração da página
st.set_page_config(page_title="📁 Enviar Planilha", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.image("assets/logo.png", use_container_width=True)
    st.page_link("app.py", label="Enviar Planilha", icon="📂")
    st.page_link("pages/analise.py", label="Análise", icon="📊")

# --- CABEÇALHO COM DEGRADÊ ---
st.markdown("""
    <div style='background: linear-gradient(to right, #004e92, #000428); padding: 40px; border-radius: 12px; margin-bottom:30px'>
        <h1 style='color: white;'>📊 Análise de Contratos SAES</h1>
        <p style='color: white;'>Explore custos, prazos e KPIs com filtros interativos.</p>
    </div>
""", unsafe_allow_html=True)

# --- UPLOAD DE PLANILHA ---
st.markdown("### 📥 Envie a planilha de contratos")
uploaded_file = st.file_uploader("Drag and drop ou clique para selecionar", type=["xlsx", "xls", "csv"])

# Campos obrigatórios esperados
campos_obrigatorios = [
    "(Não Modificar) Cooperação Técnica", "(Não Modificar) Soma de Verificação da Linha",
    "(Não Modificar) Data de Modificação", "ID Contratos", "STATUS", "PROJETO", "Nº PEP",
    "DEPARTAMENTO", "COORDENAÇÃO", "NOME", "CPF", "Sexo", "VÍNCULO", "Data de Ingresso no MS",
    "DATA INICIO", "DATA FIM", "VALOR BRUTO (R$)", "VALOR LIQUIDO (R$)", "CUSTO EFETIVO (R$)",
    "CUSTO EXECUTADO", "CUSTO PREVISTO", "DT Criação", "Data de Nascimento"
]

# --- PROCESSAMENTO DO ARQUIVO ---
if uploaded_file is not None:
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "planilha_recebida.xlsx")

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    if validar_campos_obrigatorios(file_path, campos_obrigatorios):
        df = pd.read_excel(file_path)
        st.session_state["df_contratos"] = df
        st.success("✅ Arquivo carregado com sucesso e todos os campos obrigatórios foram encontrados!")

        if st.button("➡️ Ir para Análise"):
            st.switch_page("pages/analise.py")
    else:
        st.error("❌ A planilha não contém todos os campos obrigatórios.")
        with st.expander("📌 Ver lista de campos obrigatórios"):
            for campo in campos_obrigatorios:
                st.markdown(f"- `{campo}`")