import pandas as pd
from src.data_processing import carregar_e_tratar  # se o seu estiver fora do src, troque para: from data_processing import carregar_e_tratar

def calcular_metricas(df_partidas):
    jogos = len(df_partidas)

    vitorias = df_partidas[
        ((df_partidas["home_team"] == "Brazil") & (df_partidas["home_score"] > df_partidas["away_score"])) |
        ((df_partidas["away_team"] == "Brazil") & (df_partidas["away_score"] > df_partidas["home_score"]))
    ]
    empates = df_partidas[df_partidas["home_score"] == df_partidas["away_score"]]
    derrotas = df_partidas[
        ((df_partidas["home_team"] == "Brazil") & (df_partidas["home_score"] < df_partidas["away_score"])) |
        ((df_partidas["away_team"] == "Brazil") & (df_partidas["away_score"] < df_partidas["home_score"]))
    ]

    aproveitamento = (len(vitorias) / jogos) * 100 if jogos > 0 else 0
    media_gols = df_partidas["gols_brasil"].mean()
    media_sofridos = df_partidas["gols_sofridos"].mean()

    return {
        "jogos": jogos,
        "vitorias": len(vitorias),
        "empates": len(empates),
        "derrotas": len(derrotas),
        "aproveitamento_%": round(aproveitamento, 2),
        "media_gols": round(media_gols, 2),
        "media_sofridos": round(media_sofridos, 2),
    }

def main():
    # Carregar base do Brasil (já vem com gols_brasil e gols_sofridos do seu data_processing)
    df = carregar_e_tratar()

    # Normalizar datas
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.normalize()
    df = df.dropna(subset=["date"])

    # Filtrar 2010+
    df_2010 = df[df["date"] >= "2010-01-01"].copy()

    # Carregar datas do Neymar
    neymar = pd.read_csv("data/raw/neymar_games.csv")
    neymar["date"] = pd.to_datetime(neymar["date"], errors="coerce").dt.normalize()
    neymar = neymar.dropna(subset=["date"]).drop_duplicates(subset=["date"])

    neymar_dates = neymar["date"].tolist()

    # Match tolerante ±1 dia
    neymar_match = (
        set(neymar_dates)
        | set(pd.Series(neymar_dates) + pd.Timedelta(days=1))
        | set(pd.Series(neymar_dates) - pd.Timedelta(days=1))
    )

    # Marcar jogos com Neymar
    df_2010["neymar_played"] = df_2010["date"].isin(neymar_match)

    com_neymar = df_2010[df_2010["neymar_played"] == True].copy()
    sem_neymar = df_2010[df_2010["neymar_played"] == False].copy()

    print("Jogos COM Neymar:", len(com_neymar))
    print("Jogos SEM Neymar:", len(sem_neymar))

    # Calcular métricas
    metricas_com = calcular_metricas(com_neymar)
    metricas_sem = calcular_metricas(sem_neymar)

    print("\n=== COM NEYMAR ===")
    print(metricas_com)

    print("\n=== SEM NEYMAR ===")
    print(metricas_sem)

if __name__ == "__main__":
    main()