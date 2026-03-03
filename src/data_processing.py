import pandas as pd

def carregar_e_tratar():
    # Carregar dataset
    df = pd.read_csv("data/raw/results.csv")

    # Converter coluna de data
    df["date"] = pd.to_datetime(df["date"])

    # Filtrar apenas jogos do Brasil
    brasil = df[
        (df["home_team"] == "Brazil") |
        (df["away_team"] == "Brazil")
    ].copy()

    # Criar coluna gols do Brasil
    brasil["gols_brasil"] = brasil.apply(
        lambda x: x["home_score"] if x["home_team"] == "Brazil" else x["away_score"],
        axis=1
    )

    # Criar coluna gols sofridos
    brasil["gols_sofridos"] = brasil.apply(
        lambda x: x["away_score"] if x["home_team"] == "Brazil" else x["home_score"],
        axis=1
    )

    return brasil

def filtrar_era_neymar(df):
    df["date"] = pd.to_datetime(df["date"])
    
    era_neymar = df[df["date"].dt.year >= 2010]
    
    return era_neymar

def estatisticas_brasil(df):
    vitorias = df[
        ((df["home_team"] == "Brazil") & (df["home_score"] > df["away_score"])) |
        ((df["away_team"] == "Brazil") & (df["away_score"] > df["home_score"]))
    ]

    empates = df[df["home_score"] == df["away_score"]]

    derrotas = df[
        ((df["home_team"] == "Brazil") & (df["home_score"] < df["away_score"])) |
        ((df["away_team"] == "Brazil") & (df["away_score"] < df["home_score"]))
    ]

    return len(vitorias), len(empates), len(derrotas)