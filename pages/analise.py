import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------
st.set_page_config(page_title="📊 Análise", layout="wide")

# ---------------------------------------------------------------
# Verifica se a planilha foi carregada
# ---------------------------------------------------------------
if "df_contratos" not in st.session_state:
    st.warning("⚠️ Nenhuma planilha foi enviada. Vá até a página 📁 Enviar Planilha.")
    st.stop()

df = st.session_state["df_contratos"]

# ---------------------------------------------------------------
# Renomeia colunas para facilitar os filtros
# ---------------------------------------------------------------

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

# ---------------------------------------------------------------
# Tratamentos
# ---------------------------------------------------------------

df['Data de Nascimento'] = pd.to_datetime(df['Data de Nascimento'], errors='coerce')
df['Idade'] = df['Data de Nascimento'].apply(lambda d: datetime.now().year - d.year if pd.notnull(d) else None)
df['Faixa Etária'] = pd.cut(df['Idade'], bins=[0, 17, 29, 39, 49, 59, 69, 79, 200],
                            labels=["0-17", "18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"])
# ---------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------

with st.sidebar:
    st.image("assets/logo.png", use_container_width=True)
    st.page_link("app.py", label="Enviar Planilha", icon="📂")
    st.page_link("pages/analise.py", label="Análise", icon="📊")
    st.page_link("pages/criacao.py", label="Referência", icon="✅")

    st.header("🔍 Filtros")

    with st.expander("Fatores do Contrato"):
        st.multiselect("ID Contratos", options=df["ID Contratos"].dropna().unique(), key="ID Contratos")
        st.multiselect("Status", options=df["STATUS"].dropna().unique(), key="Status")
        st.multiselect("Nº PEP", options=df["Nº PEP"].dropna().unique(), key="Nº PEP")
        st.multiselect("Departamento", options=df["DEPARTAMENTO"].dropna().unique(), key="Departamento")
        st.multiselect("Coordenação", options=df["COORDENAÇÃO"].dropna().unique(), key="Coordenação")
        st.date_input("Data de Criação", value=(df["Data de Criação"].min(), df["Data de Criação"].max()), key="Data de Criação")

    with st.expander("Fatores do Contratado"):
        st.multiselect("CPF", options=df["CPF"].dropna().unique(), key="CPF")
        st.multiselect("Sexo", options=df["Sexo"].dropna().unique(), key="Sexo")
        st.multiselect("Vínculo", options=df["VÍNCULO"].dropna().unique(), key="Vínculo")
        st.slider("Idade", int(df["Idade"].min()), int(df["Idade"].max()), value=(int(df["Idade"].min()), int(df["Idade"].max())), key="Idade")
        st.multiselect("Faixa Etária", options=df["Faixa Etária"].dropna().unique(), key="Faixa Etária")

    with st.expander("Fatores do Tempo"):
        st.selectbox("Com Data de Ingresso", options=["Sim", "Não"], key="com_dat_ingresso")
        st.date_input("Data de Ingresso", value=(df["Data de Ingresso"].min(), df["Data de Ingresso"].max()), key="Data de Ingresso")
        st.selectbox("Com Data de Início", options=["Sim", "Não"], key="com_dat_inicio")
        st.date_input("Data de Início", value=(df["Data de Início"].min(), df["Data de Início"].max()), key="Data de Início")
        st.selectbox("Com Data de Fim", options=["Sim", "Não"], key="com_dat_fim")
        st.date_input("Data de Fim", value=(df["DATA FIM"].min(), df["DATA FIM"].max()), key="Data de Fim")

    with st.expander("Fatores Financeiros"):
        st.slider("Valor Bruto", float(df["Valor Bruto"].min()), float(df["Valor Bruto"].max()), value=(float(df["Valor Bruto"].min()), float(df["Valor Bruto"].max())), key="Valor Bruto")
        st.slider("Valor Líquido", float(df["Valor Líquido"].min()), float(df["Valor Líquido"].max()), value=(float(df["Valor Líquido"].min()), float(df["Valor Líquido"].max())), key="Valor Líquido")
        st.slider("Custo Efetivo", float(df["Custo Efetivo"].min()), float(df["Custo Efetivo"].max()), value=(float(df["Custo Efetivo"].min()), float(df["Custo Efetivo"].max())), key="Custo Efetivo")
        st.slider("Custo Executado", float(df["Custo Executado"].min()), float(df["Custo Executado"].max()), value=(float(df["Custo Executado"].min()), float(df["Custo Executado"].max())), key="Custo Executado")
        st.slider("Custo Previsto", float(df["Custo Previsto"].min()), float(df["Custo Previsto"].max()), value=(float(df["Custo Previsto"].min()), float(df["Custo Previsto"].max())), key="Custo Previsto")

# ---------------------------------------------------------------
# Ler valores escolhidos nos filtros
# ---------------------------------------------------------------

f_contrato   = st.session_state.get("ID Contratos",      [])
f_status     = st.session_state.get("Status",            [])
f_pep        = st.session_state.get("Nº PEP",            [])
f_depto      = st.session_state.get("Departamento",      [])
f_coord      = st.session_state.get("Coordenação",       [])
f_data_cria  = st.session_state.get("Data de Criação",   [])

f_cpf        = st.session_state.get("CPF",               [])
f_sexo       = st.session_state.get("Sexo",              [])
f_vinculo    = st.session_state.get("Vínculo",           [])
f_idade      = st.session_state.get("Idade",             None)
f_faixa      = st.session_state.get("Faixa Etária",      [])

f_dat_ing    = st.session_state.get("Data de Ingresso",  [])
f_dat_ini    = st.session_state.get("Data de Início",    [])
f_dat_fim    = st.session_state.get("Data de Fim",       [])

f_vb         = st.session_state.get("Valor Bruto",       None)
f_vl         = st.session_state.get("Valor Líquido",     None)
f_cef        = st.session_state.get("Custo Efetivo",     None)
f_cex        = st.session_state.get("Custo Executado",   None)
f_cprev      = st.session_state.get("Custo Previsto",    None)

# ---------------------------------------------------------------
# Função auxiliar para conversão de datas
# ---------------------------------------------------------------

def to_timestamp_range(date_range):
    return pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])

# ---------------------------------------------------------------
# Aplicar filtros ao DataFrame original -> df_filt
# ---------------------------------------------------------------

df_filt = df.copy()

if f_contrato:  df_filt = df_filt[df_filt["ID Contratos"].isin(f_contrato)]
if f_status:    df_filt = df_filt[df_filt["STATUS"].isin(f_status)]
if f_pep:       df_filt = df_filt[df_filt["Nº PEP"].isin(f_pep)]
if f_depto:     df_filt = df_filt[df_filt["DEPARTAMENTO"].isin(f_depto)]
if f_coord:     df_filt = df_filt[df_filt["COORDENAÇÃO"].isin(f_coord)]
if f_data_cria: df_filt = df_filt[df_filt["Data de Criação"].between(*to_timestamp_range(f_data_cria))]

if f_cpf:       df_filt = df_filt[df_filt["CPF"].isin(f_cpf)]
if f_sexo:      df_filt = df_filt[df_filt["Sexo"].isin(f_sexo)]
if f_vinculo:   df_filt = df_filt[df_filt["VÍNCULO"].isin(f_vinculo)]
if f_idade:     df_filt = df_filt[df_filt["Idade"].between(*f_idade)]
if f_faixa:     df_filt = df_filt[df_filt["Faixa Etária"].isin(f_faixa)]

if f_dat_ing:   df_filt = df_filt[df_filt["Data de Ingresso"].between(*to_timestamp_range(f_dat_ing))]
if f_dat_ini:   df_filt = df_filt[df_filt["Data de Início"].between(*to_timestamp_range(f_dat_ini))]
if f_dat_fim:   df_filt = df_filt[df_filt["DATA FIM"].between(*to_timestamp_range(f_dat_fim))]

if f_vb:        df_filt = df_filt[df_filt["Valor Bruto"].between(*f_vb)]
if f_vl:        df_filt = df_filt[df_filt["Valor Líquido"].between(*f_vl)]
if f_cef:       df_filt = df_filt[df_filt["Custo Efetivo"].between(*f_cef)]
if f_cex:       df_filt = df_filt[df_filt["Custo Executado"].between(*f_cex)]
if f_cprev:     df_filt = df_filt[df_filt["Custo Previsto"].between(*f_cprev)]

# ---------------------------------------------------------------
# Cabeçalho com degradê
# ---------------------------------------------------------------

st.markdown("""
    <div style='background: linear-gradient(to right, #004e92, #000428); padding: 40px; border-radius: 12px; margin-bottom:30px'>
        <h1 style='color: white;'>📊 Análise de Contratos SAES</h1>
        <p style='color: white;'>Explore custos, prazos e KPIs com filtros interativos.</p>
    </div>
""", unsafe_allow_html=True)

st.header("🎲 Tipos de Análise")

# --- SELEÇÃO DE TIPO DE ANÁLISE ---
aba = st.tabs([
    "🧑 Descritiva por Colaboradores",
    "🗂️ Descritiva por Coordenação",
    "🏢 Descretiva por Departamento",
    "📁 Descritiva por Projeto",
    "🤖 Preditiva"
])


# ────────────────────────────────────────────────────────────────────────────────
#  ABA 0  –  Análise por Colaboradores
# ────────────────────────────────────────────────────────────────────────────────

with aba[0]:

    # --- Título e preparação ----------------------------------------------------------
    st.subheader("🧑‍💼 Indicadores por Colaboradores")
    df_colab = df_filt.drop_duplicates(subset="CPF").copy()

    # --- Métricas ---------------------------------------------------------------------
    num_colab  = df_colab["CPF"].nunique()
    idade_med  = round(df_colab["Idade"].mean(), 1)

    sexo_counts = df_colab["Sexo"].value_counts()
    razao_sexo  = round(sexo_counts.get("Feminino", 0) / max(sexo_counts.get("Masculino", 1), 1), 2)

    pct_dat_ini = round(df_colab["Data de Início"].notna().mean() * 100, 1)
    pct_dat_fim = round((df_colab["DATA FIM"] > pd.Timestamp.today()).mean() * 100, 1)

    valor_bruto_med = round(df_colab.groupby("CPF")["Valor Bruto"].sum().mean(), 2)
    valor_bruto_tot = round(df_filt["Valor Bruto"].sum(), 2)

    df_colab["Dias Contrato"] = (df_colab["DATA FIM"] - df_colab["Data de Início"]).dt.days
    tempo_med = round(df_colab["Dias Contrato"].mean(), 1)

    media_contratos = round(df_filt["CPF"].value_counts().mean(), 2)
    vinculos_distintos = df_colab["VÍNCULO"].nunique()
    faixa_comum = df_colab["Faixa Etária"].mode().iloc[0] if not df_colab["Faixa Etária"].mode().empty else "N/A"
    num_departamentos = df_colab["DEPARTAMENTO"].nunique()

    # --- Linha 1 de KPIs -------------------------------------------------------------
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Nº de Colaboradores", num_colab)
    c2.metric("🎂 Idade Média", idade_med)
    c3.metric("🚻 Razão F/M", razao_sexo)
    c4.metric("🏷️ Tipos de Vínculo", vinculos_distintos)

    # --- Linha 2 de KPIs -------------------------------------------------------------
    c5, c6, c7, c8 = st.columns(4)
    c5.metric("📄 % c/ Data Início", f"{pct_dat_ini}%")
    c6.metric("⏳ % c/ Data Fim futura", f"{pct_dat_fim}%")
    c7.metric("💰 Valor Bruto Médio (R$)", f"{valor_bruto_med:,.2f}")
    c8.metric("💸 Valor Bruto Total (R$)", f"{valor_bruto_tot:,.2f}")

    # --- Linha 3 de KPIs -------------------------------------------------------------
    c9, c10, c11, c12 = st.columns(4)
    c9.metric("⏱️ Tempo Médio Contrato (dias)", tempo_med)
    c10.metric("📑 Média Contratos/CPF", media_contratos)
    c11.metric("🎯 Faixa Etária Mais Comum", faixa_comum)
    c12.metric("🗂️ Departamentos", num_departamentos)

    st.markdown("---")

    # ---------- Primeira linha de gráficos ----------
    
    # --- Preparar dados da pirâmide etária ---
    df_piramide = df_colab.copy()

    # Recriar faixas etárias
    df_piramide["Faixa Etária"] = pd.cut(
        df_piramide["Idade"],
        bins=[0, 17, 29, 39, 49, 59, 69, 200],
        labels=["0-17", "18-29", "30-39", "40-49", "50-59", "60-69", "70+"]
    )

    # Agrupar por faixa e sexo
    df_pir = (
        df_piramide.groupby(["Faixa Etária", "Sexo"])
        .size()
        .reset_index(name="Total")
    )

    # Total para cálculo de percentual
    total_geral = df_pir["Total"].sum()

    # Aplicar valores negativos para homens (esquerda da pirâmide)
    df_pir["Total_signed"] = df_pir.apply(
        lambda row: -row["Total"] if row["Sexo"] == "Masculino" else row["Total"],
        axis=1
    )

    # Cores personalizadas
    cores = {
        "Masculino": "#6495ED",  # Azul claro
        "Feminino": "#FF69B4"    # Rosa
    }

    # Criar figura
    fig = go.Figure()

    for sexo in df_pir["Sexo"].unique():
        sub = df_pir[df_pir["Sexo"] == sexo]
        fig.add_trace(go.Bar(
            y=sub["Faixa Etária"],
            x=sub["Total_signed"],
            name=sexo,
            orientation="h",
            marker_color=cores[sexo],
            text=sub.apply(lambda row: f'{abs(row["Total"])} ({round(100*abs(row["Total"])/total_geral,1)}%)', axis=1),
            textposition="auto",
            hovertemplate="%{y}<br>%{x}<extra></extra>"
        ))

    fig.update_layout(
        title="Pirâmide Etária dos Colaboradores",
        barmode="relative",
        xaxis=dict(title="Número de Pessoas", tickvals=[-100, -50, 0, 50, 100], ticktext=[100, 50, 0, 50, 100]),
        yaxis=dict(title="Faixa Etária", categoryorder="category ascending"),
        legend_title="Sexo",
        margin=dict(t=40, b=40),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------- Segunda linha de gráficos ----------
     
    # Dados
    idades = df_colab["Idade"].dropna()
    media = round(np.mean(idades), 1)
    mediana = round(np.median(idades), 1)

    # Figura combinada
    fig = go.Figure()

    # Histograma
    fig.add_trace(go.Histogram(
        x=idades,
        nbinsx=20,
        name="Histograma",
        marker=dict(color='#243757'),  # Azul médio
        opacity=0.75,
        yaxis="y1"
    ))

    # Boxplot
    fig.add_trace(go.Box(
        x=idades,
        name="Boxplot",
        marker=dict(color='#243757'),  # Marrom acinzentado
        boxpoints='outliers',
        orientation='h',
        yaxis='y2'
    ))

    # Linha da média
    fig.add_trace(go.Scatter(
        x=[media, media],
        y=[0, idades.value_counts().max()],
        mode='lines',
        line=dict(color='#C2B79B', dash='dash'),
        name="Média",
        showlegend=True
    ))

    # Linha da mediana
    fig.add_trace(go.Scatter(
        x=[mediana, mediana],
        y=[0, idades.value_counts().max()],
        mode='lines',
        line=dict(color='#DAD5B7', dash='dash'),
        name="Mediana",
        showlegend=True
    ))

    # Anotações (rótulos) para média e mediana
    fig.update_layout(
        annotations=[
            dict(
                x=media,
                y=idades.value_counts().max(),
                xref='x',
                yref='y',
                text=f"Média: {media}",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-30,
                font=dict(color="#C2B79B", size=12),
                bgcolor="white"
            ),
            dict(
                x=mediana,
                y=idades.value_counts().max() * 0.9,
                xref='x',
                yref='y',
                text=f"Mediana: {mediana}",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-30,
                font=dict(color="#DAD5B7", size=12),
                bgcolor="white"
            )
        ]
    )

    # Layout final
    fig.update_layout(
        title="Distribuição da Idade",
        xaxis=dict(title="Idade", domain=[0, 1]),
        yaxis=dict(title="Frequência (Histograma)", domain=[0.3, 1], showgrid=False),
        yaxis2=dict(domain=[0, 0.2], showticklabels=False, showgrid=False),
        height=500,
        bargap=0.1,
        margin=dict(t=40, b=40, l=10, r=10),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Mostrar no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # ---------- Terceira linha de gráficos ----------

    # Agrupar por departamento e calcular a frequência
    frequencias = df_colab['DEPARTAMENTO'].value_counts().reset_index()
    frequencias.columns = ['DEPARTAMENTO', 'Frequência']

    # Calcular a porcentagem acumulada
    frequencias['Porcentagem Acumulada'] = frequencias['Frequência'].cumsum() / frequencias['Frequência'].sum() * 100

    # Criar a figura
    fig = go.Figure()

    # Barras da frequência com rótulos
    fig.add_trace(go.Bar(
        x=frequencias['DEPARTAMENTO'],
        y=frequencias['Frequência'],
        name='Frequência',
        marker=dict(color='#5b6981'),
        yaxis='y1',
        text=frequencias['Frequência'],
        textposition='outside'
    ))

    # Linha da porcentagem acumulada com rótulos
    fig.add_trace(go.Scatter(
        x=frequencias['DEPARTAMENTO'],
        y=frequencias['Porcentagem Acumulada'],
        name='Porcentagem Acumulada',
        yaxis='y2',
        mode='lines+markers+text',
        line=dict(color='red'),
        marker=dict(size=6),
        text=[f'{p:.1f}%' for p in frequencias['Porcentagem Acumulada']],
        textposition='top center'
    ))

    # Layout
    fig.update_layout(
        title='Pareto de Colaboradores por Departamento',
        xaxis=dict(title='Departamento', tickangle=-60, showgrid=False),
        yaxis=dict(title='Frequência', showgrid=False),
        yaxis2=dict(
            title='Porcentagem Acumulada (%)',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(x=0.5, y=1.2, orientation='h'),
        height=500,
        margin=dict(l=40, r=40, t=60, b=120),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # ---------- Quarta linha de gráficos ----------

    # Agrupar os dados por tipo de vínculo
    vinculos = df_colab['VÍNCULO'].value_counts().reset_index()
    vinculos.columns = ['Tipo de Vínculo', 'Quantidade']

    # Criar gráfico de rosca
    fig = go.Figure(go.Pie(
        labels=vinculos['Tipo de Vínculo'],
        values=vinculos['Quantidade'],
        hole=0.5,
        marker=dict(colors=px.colors.qualitative.Set3),
        textinfo='label+percent+value',
        insidetextorientation='radial'
    ))

    # Atualizar layout
    fig.update_layout(
        title='Distribuição por Tipos de Vínculo',
        showlegend=True,
        legend_title='Tipo de Vínculo',
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600
    )

    # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)

with aba[1]:
    st.info("Conteúdo da Análise descritiva por valores — (em construção)")

with aba[2]:
    st.info("Conteúdo da Análise preditiva temporal — (em construção)")

with aba[3]:
    st.info("Conteúdo da Análise preditiva de contratação — (em construção)")

with aba[4]:
    st.info("Conteúdo da Análise preditiva temporal — (em construção)")