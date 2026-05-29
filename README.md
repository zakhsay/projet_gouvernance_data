\# Tableau de Bord de Gouvernance d'une Plateforme Data



\## Contexte

Projet 3 — Data Science Project Management (CRISP-DM)  

Simulation d'un tableau de bord de gouvernance pour une plateforme Data fictive (secteur distribution).



\## Architecture du projet



projet\_gouvernance\_data/

├── data/

│   ├── raw/                  # Données brutes simulées (4 tables CSV)

│   │   ├── pipeline\_logs.csv

│   │   ├── table\_metadata.csv

│   │   ├── usage\_stats.csv

│   │   └── qualite\_scores.csv

│   └── processed/            # Schéma en étoile (agrégations KPIs)

│       ├── kpis\_hebdo.csv

│       ├── dim\_domaine.csv

│       ├── dim\_pipeline.csv

│       └── dim\_table.csv

├── notebooks/

│   └── phase3\_kpis\_schema\_etoile.ipynb

├── scripts/

│   └── generate\_data.py

├── dashboard/                # Fichier Power BI (à venir)

├── .gitignore

└── README.md



\## Installation



```bash

pip install faker numpy pandas notebook

```



\## Utilisation



\### 1. Générer les données

```bash

python scripts/generate\_data.py

```



\### 2. Lancer Jupyter

```bash

jupyter notebook

```

Ouvrir `notebooks/phase3\_kpis\_schema\_etoile.ipynb`



\## Données simulées



| Table | Lignes | Description |

|---|---|---|

| pipeline\_logs | 10 000 | Logs d'exécution des pipelines (succès/échec/avertissement) |

| table\_metadata | 200 | Métadonnées des tables de la plateforme |

| usage\_stats | 5 000 | Statistiques d'accès par utilisateur |

| qualite\_scores | 5 400 | Scores qualité hebdomadaires par table |



\## KPIs calculés (Phase 3)



| KPI | Formule | Source |

|---|---|---|

| taux\_succes | nb\_succes / nb\_executions × 100 | pipeline\_logs |

| score\_global\_moy | moyenne(complétude + unicité + validité) | qualite\_scores |

| nb\_alertes | tables avec score < 80% | qualite\_scores |

| nb\_utilisateurs | utilisateurs distincts par semaine | usage\_stats |



\## Phases du projet (CRISP-DM)



\- \[x] Phase 1 — Business Understanding

\- \[x] Phase 2 — Data Understanding

\- \[x] Phase 3 — Data Preparation (schéma en étoile + KPIs)

\- \[ ] Phase 4 — Tableau de bord Power BI

\- \[ ] Phase 5 — Évaluation

\- \[ ] Phase 6 — Déploiement



\## Auteur

\*\*zakhsay\*\* — \[GitHub](https://github.com/zakhsay)

