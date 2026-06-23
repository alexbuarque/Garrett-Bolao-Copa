"""
2026 FIFA World Cup fixtures — official schedule.
All datetimes are UTC. Source: official FIFA bracket (BRT times + 3h).
"""
from datetime import datetime, timezone

TOURNAMENT_START = datetime(2026, 6, 11, 19, 0, 0, tzinfo=timezone.utc)

STAGE_LABELS = {
    "group":        "Fase de Grupos",
    "round_of_32":  "Fase de 16-avos",
    "round_of_16":  "Oitavas de Final",
    "quarterfinal": "Quartas de Final",
    "semifinal":    "Semifinais",
    "third_place":  "Disputa do 3º Lugar",
    "final":        "Final",
}

STAGE_ORDER = ["group", "round_of_32", "round_of_16", "quarterfinal", "semifinal", "third_place", "final"]

FIXTURES = [
    # ── GRUPO A ───────────────────────────────────────────────────────────────
    {"group_name": "A", "team_a": "México",            "team_b": "África do Sul",        "match_date": "2026-06-11T19:00:00+00:00", "stage": "group"},
    {"group_name": "A", "team_a": "Coreia do Sul",     "team_b": "República Tcheca",     "match_date": "2026-06-12T02:00:00+00:00", "stage": "group"},
    {"group_name": "A", "team_a": "República Tcheca",  "team_b": "África do Sul",        "match_date": "2026-06-18T16:00:00+00:00", "stage": "group"},
    {"group_name": "A", "team_a": "México",            "team_b": "Coreia do Sul",        "match_date": "2026-06-19T01:00:00+00:00", "stage": "group"},
    {"group_name": "A", "team_a": "República Tcheca",  "team_b": "México",               "match_date": "2026-06-25T01:00:00+00:00", "stage": "group"},
    {"group_name": "A", "team_a": "África do Sul",     "team_b": "Coreia do Sul",        "match_date": "2026-06-25T01:00:00+00:00", "stage": "group"},
    # ── GRUPO B ───────────────────────────────────────────────────────────────
    {"group_name": "B", "team_a": "Canadá",            "team_b": "Bósnia e Herzegovina", "match_date": "2026-06-12T19:00:00+00:00", "stage": "group"},
    {"group_name": "B", "team_a": "Catar",             "team_b": "Suíça",                "match_date": "2026-06-13T19:00:00+00:00", "stage": "group"},
    {"group_name": "B", "team_a": "Suíça",             "team_b": "Bósnia e Herzegovina", "match_date": "2026-06-18T19:00:00+00:00", "stage": "group"},
    {"group_name": "B", "team_a": "Canadá",            "team_b": "Catar",                "match_date": "2026-06-18T22:00:00+00:00", "stage": "group"},
    {"group_name": "B", "team_a": "Suíça",             "team_b": "Canadá",               "match_date": "2026-06-24T19:00:00+00:00", "stage": "group"},
    {"group_name": "B", "team_a": "Bósnia e Herzegovina", "team_b": "Catar",             "match_date": "2026-06-24T19:00:00+00:00", "stage": "group"},
    # ── GRUPO C ───────────────────────────────────────────────────────────────
    {"group_name": "C", "team_a": "Brasil",            "team_b": "Marrocos",             "match_date": "2026-06-13T22:00:00+00:00", "stage": "group"},
    {"group_name": "C", "team_a": "Haiti",             "team_b": "Escócia",              "match_date": "2026-06-14T01:00:00+00:00", "stage": "group"},
    {"group_name": "C", "team_a": "Escócia",           "team_b": "Marrocos",             "match_date": "2026-06-19T22:00:00+00:00", "stage": "group"},
    {"group_name": "C", "team_a": "Brasil",            "team_b": "Haiti",                "match_date": "2026-06-20T00:30:00+00:00", "stage": "group"},
    {"group_name": "C", "team_a": "Escócia",           "team_b": "Brasil",               "match_date": "2026-06-24T22:00:00+00:00", "stage": "group"},
    {"group_name": "C", "team_a": "Marrocos",          "team_b": "Haiti",                "match_date": "2026-06-24T22:00:00+00:00", "stage": "group"},
    # ── GRUPO D ───────────────────────────────────────────────────────────────
    {"group_name": "D", "team_a": "Estados Unidos",    "team_b": "Paraguai",             "match_date": "2026-06-13T01:00:00+00:00", "stage": "group"},
    {"group_name": "D", "team_a": "Austrália",         "team_b": "Turquia",              "match_date": "2026-06-14T04:00:00+00:00", "stage": "group"},
    {"group_name": "D", "team_a": "Estados Unidos",    "team_b": "Austrália",            "match_date": "2026-06-19T19:00:00+00:00", "stage": "group"},
    {"group_name": "D", "team_a": "Turquia",           "team_b": "Paraguai",             "match_date": "2026-06-20T11:00:00+00:00", "stage": "group"},
    {"group_name": "D", "team_a": "Turquia",           "team_b": "Estados Unidos",       "match_date": "2026-06-26T02:00:00+00:00", "stage": "group"},
    {"group_name": "D", "team_a": "Paraguai",          "team_b": "Austrália",            "match_date": "2026-06-26T02:00:00+00:00", "stage": "group"},
    # ── GRUPO E ───────────────────────────────────────────────────────────────
    {"group_name": "E", "team_a": "Alemanha",          "team_b": "Curaçau",              "match_date": "2026-06-14T17:00:00+00:00", "stage": "group"},
    {"group_name": "E", "team_a": "Costa do Marfim",   "team_b": "Equador",              "match_date": "2026-06-14T23:00:00+00:00", "stage": "group"},
    {"group_name": "E", "team_a": "Alemanha",          "team_b": "Costa do Marfim",      "match_date": "2026-06-20T20:00:00+00:00", "stage": "group"},
    {"group_name": "E", "team_a": "Equador",           "team_b": "Curaçau",              "match_date": "2026-06-21T00:00:00+00:00", "stage": "group"},
    {"group_name": "E", "team_a": "Equador",           "team_b": "Alemanha",             "match_date": "2026-06-25T20:00:00+00:00", "stage": "group"},
    {"group_name": "E", "team_a": "Curaçau",           "team_b": "Costa do Marfim",      "match_date": "2026-06-25T20:00:00+00:00", "stage": "group"},
    # ── GRUPO F ───────────────────────────────────────────────────────────────
    {"group_name": "F", "team_a": "Holanda",           "team_b": "Japão",                "match_date": "2026-06-14T20:00:00+00:00", "stage": "group"},
    {"group_name": "F", "team_a": "Suécia",            "team_b": "Tunísia",              "match_date": "2026-06-15T02:00:00+00:00", "stage": "group"},
    {"group_name": "F", "team_a": "Holanda",           "team_b": "Suécia",               "match_date": "2026-06-20T17:00:00+00:00", "stage": "group"},
    {"group_name": "F", "team_a": "Tunísia",           "team_b": "Japão",                "match_date": "2026-06-21T04:00:00+00:00", "stage": "group"},
    {"group_name": "F", "team_a": "Japão",             "team_b": "Suécia",               "match_date": "2026-06-25T23:00:00+00:00", "stage": "group"},
    {"group_name": "F", "team_a": "Tunísia",           "team_b": "Holanda",              "match_date": "2026-06-25T23:00:00+00:00", "stage": "group"},
    # ── GRUPO G ───────────────────────────────────────────────────────────────
    {"group_name": "G", "team_a": "Bélgica",           "team_b": "Egito",                "match_date": "2026-06-15T19:00:00+00:00", "stage": "group"},
    {"group_name": "G", "team_a": "Irã",               "team_b": "Nova Zelândia",        "match_date": "2026-06-16T01:00:00+00:00", "stage": "group"},
    {"group_name": "G", "team_a": "Bélgica",           "team_b": "Irã",                  "match_date": "2026-06-21T19:00:00+00:00", "stage": "group"},
    {"group_name": "G", "team_a": "Nova Zelândia",     "team_b": "Egito",                "match_date": "2026-06-22T01:00:00+00:00", "stage": "group"},
    {"group_name": "G", "team_a": "Egito",             "team_b": "Irã",                  "match_date": "2026-06-27T03:00:00+00:00", "stage": "group"},
    {"group_name": "G", "team_a": "Nova Zelândia",     "team_b": "Bélgica",              "match_date": "2026-06-27T03:00:00+00:00", "stage": "group"},
    # ── GRUPO H ───────────────────────────────────────────────────────────────
    {"group_name": "H", "team_a": "Espanha",           "team_b": "Cabo Verde",           "match_date": "2026-06-15T16:00:00+00:00", "stage": "group"},
    {"group_name": "H", "team_a": "Arábia Saudita",    "team_b": "Uruguai",              "match_date": "2026-06-15T22:00:00+00:00", "stage": "group"},
    {"group_name": "H", "team_a": "Espanha",           "team_b": "Arábia Saudita",       "match_date": "2026-06-21T16:00:00+00:00", "stage": "group"},
    {"group_name": "H", "team_a": "Uruguai",           "team_b": "Cabo Verde",           "match_date": "2026-06-21T22:00:00+00:00", "stage": "group"},
    {"group_name": "H", "team_a": "Cabo Verde",        "team_b": "Arábia Saudita",       "match_date": "2026-06-27T00:00:00+00:00", "stage": "group"},
    {"group_name": "H", "team_a": "Uruguai",           "team_b": "Espanha",              "match_date": "2026-06-27T00:00:00+00:00", "stage": "group"},
    # ── GRUPO I ───────────────────────────────────────────────────────────────
    {"group_name": "I", "team_a": "França",            "team_b": "Senegal",              "match_date": "2026-06-16T19:00:00+00:00", "stage": "group"},
    {"group_name": "I", "team_a": "Iraque",            "team_b": "Noruega",              "match_date": "2026-06-16T22:00:00+00:00", "stage": "group"},
    {"group_name": "I", "team_a": "França",            "team_b": "Iraque",               "match_date": "2026-06-22T21:00:00+00:00", "stage": "group"},
    {"group_name": "I", "team_a": "Noruega",           "team_b": "Senegal",              "match_date": "2026-06-23T00:00:00+00:00", "stage": "group"},
    {"group_name": "I", "team_a": "Noruega",           "team_b": "França",               "match_date": "2026-06-26T19:00:00+00:00", "stage": "group"},
    {"group_name": "I", "team_a": "Senegal",           "team_b": "Iraque",               "match_date": "2026-06-26T19:00:00+00:00", "stage": "group"},
    # ── GRUPO J ───────────────────────────────────────────────────────────────
    {"group_name": "J", "team_a": "Argentina",         "team_b": "Argélia",              "match_date": "2026-06-17T01:00:00+00:00", "stage": "group"},
    {"group_name": "J", "team_a": "Áustria",           "team_b": "Jordânia",             "match_date": "2026-06-17T04:00:00+00:00", "stage": "group"},
    {"group_name": "J", "team_a": "Argentina",         "team_b": "Áustria",              "match_date": "2026-06-22T17:00:00+00:00", "stage": "group"},
    {"group_name": "J", "team_a": "Jordânia",          "team_b": "Argélia",              "match_date": "2026-06-23T11:00:00+00:00", "stage": "group"},
    {"group_name": "J", "team_a": "Argélia",           "team_b": "Áustria",              "match_date": "2026-06-28T02:00:00+00:00", "stage": "group"},
    {"group_name": "J", "team_a": "Jordânia",          "team_b": "Argentina",            "match_date": "2026-06-28T02:00:00+00:00", "stage": "group"},
    # ── GRUPO K ───────────────────────────────────────────────────────────────
    {"group_name": "K", "team_a": "Portugal",          "team_b": "R. D. do Congo",       "match_date": "2026-06-17T17:00:00+00:00", "stage": "group"},
    {"group_name": "K", "team_a": "Uzbequistão",       "team_b": "Colômbia",             "match_date": "2026-06-18T02:00:00+00:00", "stage": "group"},
    {"group_name": "K", "team_a": "Portugal",          "team_b": "Uzbequistão",          "match_date": "2026-06-23T17:00:00+00:00", "stage": "group"},
    {"group_name": "K", "team_a": "Colômbia",          "team_b": "R. D. do Congo",       "match_date": "2026-06-24T02:00:00+00:00", "stage": "group"},
    {"group_name": "K", "team_a": "Colômbia",          "team_b": "Portugal",             "match_date": "2026-06-27T23:30:00+00:00", "stage": "group"},
    {"group_name": "K", "team_a": "R. D. do Congo",    "team_b": "Uzbequistão",          "match_date": "2026-06-27T23:30:00+00:00", "stage": "group"},
    # ── GRUPO L ───────────────────────────────────────────────────────────────
    {"group_name": "L", "team_a": "Inglaterra",        "team_b": "Croácia",              "match_date": "2026-06-17T20:00:00+00:00", "stage": "group"},
    {"group_name": "L", "team_a": "Gana",              "team_b": "Panamá",               "match_date": "2026-06-17T23:00:00+00:00", "stage": "group"},
    {"group_name": "L", "team_a": "Inglaterra",        "team_b": "Gana",                 "match_date": "2026-06-23T20:00:00+00:00", "stage": "group"},
    {"group_name": "L", "team_a": "Panamá",            "team_b": "Croácia",              "match_date": "2026-06-23T23:00:00+00:00", "stage": "group"},
    {"group_name": "L", "team_a": "Panamá",            "team_b": "Inglaterra",           "match_date": "2026-06-27T21:00:00+00:00", "stage": "group"},
    {"group_name": "L", "team_a": "Croácia",           "team_b": "Gana",                 "match_date": "2026-06-27T21:00:00+00:00", "stage": "group"},
]

PLAYOFF_FIXTURES = [
    # ── FASE DE 16-AVOS (jogos 73-88) ────────────────────────────────────────
    # Jun 28
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-06-28T23:00:00+00:00",
     "team_a": "2º Grupo A",     "team_b": "2º Grupo B"},       # Jogo 73 – Los Angeles
    # Jun 29
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-06-29T18:00:00+00:00",
     "team_a": "1º Grupo E",     "team_b": "3º A/B/C/D/F"},     # Jogo 74 – Boston
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-06-29T21:00:00+00:00",
     "team_a": "1º Grupo F",     "team_b": "2º Grupo C"},        # Jogo 75 – Monterrey
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-06-30T00:00:00+00:00",
     "team_a": "1º Grupo C",     "team_b": "2º Grupo F"},        # Jogo 76 – Houston
    # Jun 30
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-06-30T18:00:00+00:00",
     "team_a": "1º Grupo I",     "team_b": "3º C/D/F/G/H"},     # Jogo 77 – Nova York/NJ
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-06-30T21:00:00+00:00",
     "team_a": "2º Grupo E",     "team_b": "2º Grupo I"},        # Jogo 78 – Dallas
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-07-01T00:00:00+00:00",
     "team_a": "1º Grupo A",     "team_b": "3º C/E/F/H/I"},     # Jogo 79 – Cidade do México
    # Jul 1
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-07-01T18:00:00+00:00",
     "team_a": "1º Grupo L",     "team_b": "3º E/H/I/J/K"},     # Jogo 80 – Atlanta
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-07-01T21:00:00+00:00",
     "team_a": "1º Grupo D",     "team_b": "3º B/E/F/I/J"},     # Jogo 81 – Santa Clara
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-07-02T00:00:00+00:00",
     "team_a": "1º Grupo G",     "team_b": "3º A/E/H/I/J"},     # Jogo 82 – Seattle
    # Jul 2
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-07-02T18:00:00+00:00",
     "team_a": "2º Grupo K",     "team_b": "2º Grupo L"},        # Jogo 83 – Toronto
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-07-02T21:00:00+00:00",
     "team_a": "1º Grupo H",     "team_b": "2º Grupo J"},        # Jogo 84 – Los Angeles
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-07-03T00:00:00+00:00",
     "team_a": "1º Grupo B",     "team_b": "3º E/F/G/I/J"},     # Jogo 85 – Vancouver
    # Jul 3
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-07-03T18:00:00+00:00",
     "team_a": "1º Grupo J",     "team_b": "2º Grupo H"},        # Jogo 86 – Miami
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-07-03T21:00:00+00:00",
     "team_a": "1º Grupo K",     "team_b": "3º D/E/I/J/L"},     # Jogo 87 – Kansas City
    {"group_name": "16avos", "stage": "round_of_32", "match_date": "2026-07-04T00:00:00+00:00",
     "team_a": "2º Grupo D",     "team_b": "2º Grupo G"},        # Jogo 88 – Dallas

    # ── OITAVAS DE FINAL (jogos 89-96) ───────────────────────────────────────
    # Jul 4
    {"group_name": "Oitavas", "stage": "round_of_16", "match_date": "2026-07-04T18:00:00+00:00",
     "team_a": "Venc. Jogo 74",  "team_b": "Venc. Jogo 77"},    # Jogo 89 – Filadélfia
    {"group_name": "Oitavas", "stage": "round_of_16", "match_date": "2026-07-04T22:00:00+00:00",
     "team_a": "Venc. Jogo 73",  "team_b": "Venc. Jogo 75"},    # Jogo 90 – Houston
    # Jul 5
    {"group_name": "Oitavas", "stage": "round_of_16", "match_date": "2026-07-05T18:00:00+00:00",
     "team_a": "Venc. Jogo 76",  "team_b": "Venc. Jogo 78"},    # Jogo 91 – Nova York/NJ
    {"group_name": "Oitavas", "stage": "round_of_16", "match_date": "2026-07-05T22:00:00+00:00",
     "team_a": "Venc. Jogo 79",  "team_b": "Venc. Jogo 80"},    # Jogo 92 – Cidade do México
    # Jul 6
    {"group_name": "Oitavas", "stage": "round_of_16", "match_date": "2026-07-06T18:00:00+00:00",
     "team_a": "Venc. Jogo 83",  "team_b": "Venc. Jogo 84"},    # Jogo 93 – Dallas
    {"group_name": "Oitavas", "stage": "round_of_16", "match_date": "2026-07-06T22:00:00+00:00",
     "team_a": "Venc. Jogo 81",  "team_b": "Venc. Jogo 82"},    # Jogo 94 – Seattle
    # Jul 7
    {"group_name": "Oitavas", "stage": "round_of_16", "match_date": "2026-07-07T18:00:00+00:00",
     "team_a": "Venc. Jogo 86",  "team_b": "Venc. Jogo 88"},    # Jogo 95 – Atlanta
    {"group_name": "Oitavas", "stage": "round_of_16", "match_date": "2026-07-07T22:00:00+00:00",
     "team_a": "Venc. Jogo 85",  "team_b": "Venc. Jogo 87"},    # Jogo 96 – Vancouver

    # ── QUARTAS DE FINAL (jogos 97-100) ──────────────────────────────────────
    {"group_name": "Quartas", "stage": "quarterfinal", "match_date": "2026-07-09T22:00:00+00:00",
     "team_a": "Venc. Jogo 89",  "team_b": "Venc. Jogo 90"},    # Jogo 97 – Boston
    {"group_name": "Quartas", "stage": "quarterfinal", "match_date": "2026-07-10T22:00:00+00:00",
     "team_a": "Venc. Jogo 93",  "team_b": "Venc. Jogo 94"},    # Jogo 98 – Los Angeles
    {"group_name": "Quartas", "stage": "quarterfinal", "match_date": "2026-07-11T18:00:00+00:00",
     "team_a": "Venc. Jogo 91",  "team_b": "Venc. Jogo 92"},    # Jogo 99 – Miami
    {"group_name": "Quartas", "stage": "quarterfinal", "match_date": "2026-07-11T22:00:00+00:00",
     "team_a": "Venc. Jogo 95",  "team_b": "Venc. Jogo 96"},    # Jogo 100 – Kansas City

    # ── SEMIFINAIS (jogos 101-102) ────────────────────────────────────────────
    {"group_name": "Semifinal", "stage": "semifinal", "match_date": "2026-07-14T22:00:00+00:00",
     "team_a": "Venc. Jogo 97",  "team_b": "Venc. Jogo 98"},    # Jogo 101 – Dallas
    {"group_name": "Semifinal", "stage": "semifinal", "match_date": "2026-07-15T22:00:00+00:00",
     "team_a": "Venc. Jogo 99",  "team_b": "Venc. Jogo 100"},   # Jogo 102 – Atlanta

    # ── DISPUTA DO 3º LUGAR (jogo 103) ───────────────────────────────────────
    {"group_name": "3º Lugar", "stage": "third_place", "match_date": "2026-07-18T22:00:00+00:00",
     "team_a": "Perd. Jogo 101", "team_b": "Perd. Jogo 102"},   # Jogo 103 – Miami

    # ── FINAL (jogo 104) ─────────────────────────────────────────────────────
    {"group_name": "Final", "stage": "final", "match_date": "2026-07-19T22:00:00+00:00",
     "team_a": "Venc. Jogo 101", "team_b": "Venc. Jogo 102"},   # Jogo 104 – Nova York/NJ
]


def get_all_fixtures() -> list[dict]:
    """Return all 72 group stage fixtures."""
    return FIXTURES


def get_playoff_fixtures() -> list[dict]:
    """Return the 32 knockout stage fixtures (teams are placeholders until confirmed)."""
    return PLAYOFF_FIXTURES
