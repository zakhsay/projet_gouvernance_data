"""
Projet 3 — Gouvernance Plateforme Data
Génération des 4 tables simulées sur 6 mois (2024-07-01 → 2024-12-31)
Tables : pipeline_logs, table_metadata, usage_stats, qualite_scores
"""

import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("fr_FR")
random.seed(42)
np.random.seed(42)

# ─── Paramètres globaux ───────────────────────────────────────────────────────
START_DATE = datetime(2024, 7, 1)
END_DATE   = datetime(2024, 12, 31)
DOMAINES   = ["RH", "Finance", "Marketing", "Ventes"]
PIPELINES_PAR_DOMAINE = 10   # 40 pipelines au total
NB_TABLES  = 200
NB_USERS   = 80
NB_USAGE   = 5_000
NB_LOGS    = 10_000

CLASSIFICATIONS = ["Public", "Interne", "Confidentiel", "Strictement confidentiel"]
STATUTS = ["succès", "échec", "avertissement"]

def random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

# ─── 1. table_metadata (200 tables) ──────────────────────────────────────────
def generate_table_metadata() -> pd.DataFrame:
    rows = []
    table_id = 1
    for domaine in DOMAINES:
        for i in range(NB_TABLES // len(DOMAINES)):
            last_update = random_date(START_DATE, END_DATE)
            rows.append({
                "table_id":          f"TBL_{table_id:04d}",
                "nom":               f"{domaine.lower()}_{fake.word()}_{i+1}",
                "domaine":           domaine,
                "date_derniere_maj": last_update.strftime("%Y-%m-%d"),
                "taille_go":         round(random.uniform(0.1, 500.0), 2),
                "proprietaire":      fake.name(),
                "classif_sensibilite": random.choices(
                    CLASSIFICATIONS, weights=[30, 40, 20, 10]
                )[0],
            })
            table_id += 1
    df = pd.DataFrame(rows)
    return df

# ─── 2. pipeline_logs (10 000 entrées) ───────────────────────────────────────
def generate_pipeline_logs(table_meta: pd.DataFrame) -> pd.DataFrame:
    """
    Anomalie volontaire : semaine 3 (2024-07-15 → 2024-07-21)
    → taux d'échec Finance monté à ~40 %
    """
    pipeline_ids = {
        domaine: [f"PIPE_{domaine[:3].upper()}_{j+1:02d}" for j in range(PIPELINES_PAR_DOMAINE)]
        for domaine in DOMAINES
    }
    rows = []
    for _ in range(NB_LOGS):
        domaine = random.choices(DOMAINES, weights=[20, 30, 25, 25])[0]
        pipeline_id = random.choice(pipeline_ids[domaine])
        date_run = random_date(START_DATE, END_DATE)

        # Anomalie Finance semaine 3
        week3_start = datetime(2024, 7, 15)
        week3_end   = datetime(2024, 7, 21)
        if domaine == "Finance" and week3_start <= date_run <= week3_end:
            statut = random.choices(STATUTS, weights=[60, 40, 0])[0]
        else:
            statut = random.choices(STATUTS, weights=[82, 8, 10])[0]

        duree_sec = round(random.uniform(5, 3600), 1)
        if statut == "échec":
            duree_sec = round(random.uniform(5, 120), 1)   # les échecs sont rapides

        rows.append({
            "log_id":               f"LOG_{len(rows)+1:06d}",
            "pipeline_id":          pipeline_id,
            "domaine":              domaine,
            "date_run":             date_run.strftime("%Y-%m-%d %H:%M:%S"),
            "statut":               statut,
            "duree_sec":            duree_sec,
            "volume_lignes_traitees": random.randint(100, 2_000_000) if statut != "échec" else 0,
        })
    df = pd.DataFrame(rows).sort_values("date_run").reset_index(drop=True)
    return df

# ─── 3. usage_stats (5 000 entrées) ──────────────────────────────────────────
def generate_usage_stats(table_meta: pd.DataFrame) -> pd.DataFrame:
    equipes = ["Marketing", "Finance", "RH", "Ventes", "IT", "Direction", "Juridique"]
    user_ids = [f"USR_{i+1:04d}" for i in range(NB_USERS)]
    table_names = table_meta["nom"].tolist()
    table_domaines = dict(zip(table_meta["nom"], table_meta["domaine"]))

    rows = []
    for _ in range(NB_USAGE):
        table = random.choice(table_names)
        rows.append({
            "acces_id":       f"ACC_{len(rows)+1:06d}",
            "user_id":        random.choice(user_ids),
            "equipe":         random.choice(equipes),
            "domaine":        table_domaines[table],
            "table_consultee": table,
            "date_acces":     random_date(START_DATE, END_DATE).strftime("%Y-%m-%d %H:%M:%S"),
        })
    df = pd.DataFrame(rows).sort_values("date_acces").reset_index(drop=True)
    return df

# ─── 4. qualite_scores (score hebdo par table) ───────────────────────────────
def generate_qualite_scores(table_meta: pd.DataFrame) -> pd.DataFrame:
    """
    Scores de complétude, unicité, validité par table et par semaine.
    Format inspiré de Great Expectations.
    """
    # Générer les semaines sur la période
    semaines = []
    current = START_DATE
    while current <= END_DATE:
        semaines.append(current.strftime("%Y-%W"))
        current += timedelta(weeks=1)

    rows = []
    for _, t in table_meta.iterrows():
        # Profil de base par classification
        base = {
            "Public": (90, 95, 92),
            "Interne": (85, 90, 88),
            "Confidentiel": (80, 85, 83),
            "Strictement confidentiel": (75, 88, 80),
        }[t["classif_sensibilite"]]

        for semaine in semaines:
            # Légère variation semaine après semaine
            completude = round(min(100, max(0, base[0] + np.random.normal(0, 4))), 1)
            unicite    = round(min(100, max(0, base[1] + np.random.normal(0, 3))), 1)
            validite   = round(min(100, max(0, base[2] + np.random.normal(0, 5))), 1)
            score_global = round((completude + unicite + validite) / 3, 1)

            rows.append({
                "score_id":       f"SCR_{len(rows)+1:07d}",
                "table_id":       t["table_id"],
                "nom":            t["nom"],
                "domaine":        t["domaine"],
                "semaine":        semaine,
                "completude":     completude,
                "unicite":        unicite,
                "validite":       validite,
                "score_global":   score_global,
                "alerte":         score_global < 80,
            })
    df = pd.DataFrame(rows)
    return df

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    output_dir = "/mnt/user-data/outputs"
    os.makedirs(output_dir, exist_ok=True)

    print("⏳ Génération de table_metadata...")
    meta = generate_table_metadata()
    meta.to_csv(f"{output_dir}/table_metadata.csv", index=False)
    print(f"   ✅ {len(meta)} lignes → table_metadata.csv")

    print("⏳ Génération de pipeline_logs...")
    logs = generate_pipeline_logs(meta)
    logs.to_csv(f"{output_dir}/pipeline_logs.csv", index=False)
    print(f"   ✅ {len(logs)} lignes → pipeline_logs.csv")

    print("⏳ Génération de usage_stats...")
    usage = generate_usage_stats(meta)
    usage.to_csv(f"{output_dir}/usage_stats.csv", index=False)
    print(f"   ✅ {len(usage)} lignes → usage_stats.csv")

    print("⏳ Génération de qualite_scores...")
    qualite = generate_qualite_scores(meta)
    qualite.to_csv(f"{output_dir}/qualite_scores.csv", index=False)
    print(f"   ✅ {len(qualite)} lignes → qualite_scores.csv")

    # ── Aperçu rapide
    print("\n📊 Aperçu des tables générées :")
    for name, df in [("table_metadata", meta), ("pipeline_logs", logs),
                     ("usage_stats", usage), ("qualite_scores", qualite)]:
        print(f"\n{'─'*50}")
        print(f"  {name}  ({df.shape[0]} lignes × {df.shape[1]} colonnes)")
        print(df.head(3).to_string(index=False))

    print("\n✅ Toutes les données ont été générées avec succès !")
