import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_processing import carregar_e_tratar  # se o seu for fora do src, ajuste

st.set_page_config(page_title="Brasil x Neymar (2010+)", layout="wide")

@st.cache_data
def load_data():
    df = carregar_e_tratar()
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.normalize()
    df = df.dropna(subset=["date"])
    df = df[df["date"] >= "2010-01-01"].copy()

    neymar = pd.read_csv("data/raw/neymar_games.csv")
    neymar["date"] = pd.to_datetime(neymar["date"], errors="coerce").dt.normalize()
    neymar = neymar.dropna(subset=["date"]).drop_duplicates(subset=["date"])

    neymar_dates = neymar["date"].tolist()
    neymar_match = (
        set(neymar_dates)
        | set(pd.Series(neymar_dates) + pd.Timedelta(days=1))
        | set(pd.Series(neymar_dates) - pd.Timedelta(days=1))
    )

    df["neymar_played"] = df["date"].isin(neymar_match)
    df["resultado"] = df.apply(
        lambda x: "V" if x["gols_brasil"] > x["gols_sofridos"] else ("E" if x["gols_brasil"] == x["gols_sofridos"] else "D"),
        axis=1
    )
    return df

def metricas(df_partidas: pd.DataFrame):
    jogos = len(df_partidas)
    v = (df_partidas["resultado"] == "V").sum()
    e = (df_partidas["resultado"] == "E").sum()
    d = (df_partidas["resultado"] == "D").sum()
    aproveitamento = (v / jogos) * 100 if jogos else 0
    return {
        "Jogos": jogos,
        "Vitórias": int(v),
        "Empates": int(e),
        "Derrotas": int(d),
        "Aproveitamento (%)": round(aproveitamento, 2),
        "Média gols": round(df_partidas["gols_brasil"].mean(), 2) if jogos else 0,
        "Média sofridos": round(df_partidas["gols_sofridos"].mean(), 2) if jogos else 0,
    }

df = load_data()

st.title("📊 Brasil (2010+) — Desempenho COM vs SEM Neymar")

# Filtros
colf1, colf2, colf3 = st.columns(3)
with colf1:
    grupo = st.radio("Filtrar jogos:", ["Todos", "Com Neymar", "Sem Neymar"], horizontal=True)
with colf2:
    torneios = sorted(df["tournament"].dropna().unique().tolist())
    selected_tournaments = st.multiselect("Torneios", torneios, default=torneios)
with colf3:
    anos = sorted(df["date"].dt.year.unique().tolist())
    ano_min, ano_max = st.slider("Período", min_value=min(anos), max_value=max(anos), value=(min(anos), max(anos)))

# Aplicar filtros
df_f = df[df["tournament"].isin(selected_tournaments)].copy()
df_f = df_f[(df_f["date"].dt.year >= ano_min) & (df_f["date"].dt.year <= ano_max)].copy()

if grupo == "Com Neymar":
    df_f = df_f[df_f["neymar_played"] == True]
elif grupo == "Sem Neymar":
    df_f = df_f[df_f["neymar_played"] == False]

# Separações fixas para comparação lado a lado
df_com = df_f[df_f["neymar_played"] == True].copy()
df_sem = df_f[df_f["neymar_played"] == False].copy()

m_com = metricas(df_com)
m_sem = metricas(df_sem)

# KPIs
k1, k2 = st.columns(2)
with k1:
    st.subheader("✅ Com Neymar")
    st.metric("Jogos", m_com["Jogos"])
    st.metric("Aproveitamento (%)", m_com["Aproveitamento (%)"])
    st.metric("Média gols", m_com["Média gols"])
    st.metric("Média sofridos", m_com["Média sofridos"])

with k2:
    st.subheader("❌ Sem Neymar")
    st.metric("Jogos", m_sem["Jogos"])
    st.metric("Aproveitamento (%)", m_sem["Aproveitamento (%)"])
    st.metric("Média gols", m_sem["Média gols"])
    st.metric("Média sofridos", m_sem["Média sofridos"])

st.divider()

# Gráfico por ano
df_year = df_f.copy()
df_year["ano"] = df_year["date"].dt.year
g = df_year.groupby(["ano", "neymar_played"]).agg(
    jogos=("resultado", "count"),
    vitorias=("resultado", lambda s: (s == "V").sum()),
    gols=("gols_brasil", "sum"),
    sofridos=("gols_sofridos", "sum"),
).reset_index()

g["aproveitamento_%"] = (g["vitorias"] / g["jogos"]) * 100
g["grupo"] = g["neymar_played"].map({True: "Com Neymar", False: "Sem Neymar"})

fig = px.line(
    g,
    x="ano",
    y="aproveitamento_%",
    color="grupo",
    markers=True,
    title="Aproveitamento por ano (filtros aplicados)"
)
st.plotly_chart(fig, use_container_width=True)

# Tabela para conferir jogos
st.subheader("📋 Partidas (filtros aplicados)")
cols_show = ["date", "home_team", "away_team", "home_score", "away_score", "tournament", "neymar_played", "resultado"]
st.dataframe(df_f.sort_values("date", ascending=False)[cols_show], use_container_width=True)