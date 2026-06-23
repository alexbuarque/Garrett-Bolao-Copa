"""
2026 FIFA World Cup group stage fixtures — official schedule.
All datetimes are UTC. Source: official FIFA bracket (BRT times + 3h).
"""
from datetime import datetime, timezone

TOURNAMENT_START = datetime(2026, 6, 11, 19, 0, 0, tzinfo=timezone.utc)

FIXTURES = [
    # ── GRUPO A ───────────────────────────────────────────────────────────────
    {"group_name": "A", "team_a": "México",            "team_b": "África do Sul",     "match_date": "2026-06-11T19:00:00+00:00", "stage": "group"},
    {"group_name": "A", "team_a": "Coreia do Sul",     "team_b": "República Tcheca",  "match_date": "2026-06-12T02:00:00+00:00", "stage": "group"},
    {"group_name": "A", "team_a": "República Tcheca",  "team_b": "África do Sul",     "match_date": "2026-06-18T16:00:00+00:00", "stage": "group"},
    {"group_name": "A", "team_a": "México",            "team_b": "Coreia do Sul",     "match_date": "2026-06-19T01:00:00+00:00", "stage": "group"},
    {"group_name": "A", "team_a": "República Tcheca",  "team_b": "México",            "match_date": "2026-06-25T01:00:00+00:00", "stage": "group"},
    {"group_name": "A", "team_a": "África do Sul",     "team_b": "Coreia do Sul",     "match_date": "2026-06-25T01:00:00+00:00", "stage": "group"},
    # ── GRUPO B ───────────────────────────────────────────────────────────────
    {"group_name": "B", "team_a": "Canadá",            "team_b": "Bósnia e Herzegovina", "match_date": "2026-06-12T19:00:00+00:00", "stage": "group"},
    {"group_name": "B", "team_a": "Catar",             "team_b": "Suíça",             "match_date": "2026-06-13T19:00:00+00:00", "stage": "group"},
    {"group_name": "B", "team_a": "Suíça",             "team_b": "Bósnia e Herzegovina", "match_date": "2026-06-18T19:00:00+00:00", "stage": "group"},
    {"group_name": "B", "team_a": "Canadá",            "team_b": "Catar",             "match_date": "2026-06-18T22:00:00+00:00", "stage": "group"},
    {"group_name": "B", "team_a": "Suíça",             "team_b": "Canadá",            "match_date": "2026-06-24T19:00:00+00:00", "stage": "group"},
    {"group_name": "B", "team_a": "Bósnia e Herzegovina", "team_b": "Catar",          "match_date": "2026-06-24T19:00:00+00:00", "stage": "group"},
    # ── GRUPO C ───────────────────────────────────────────────────────────────
    {"group_name": "C", "team_a": "Brasil",            "team_b": "Marrocos",          "match_date": "2026-06-13T22:00:00+00:00", "stage": "group"},
    {"group_name": "C", "team_a": "Haiti",             "team_b": "Escócia",           "match_date": "2026-06-14T01:00:00+00:00", "stage": "group"},
    {"group_name": "C", "team_a": "Escócia",           "team_b": "Marrocos",          "match_date": "2026-06-19T22:00:00+00:00", "stage": "group"},
    {"group_name": "C", "team_a": "Brasil",            "team_b": "Haiti",             "match_date": "2026-06-20T00:30:00+00:00", "stage": "group"},
    {"group_name": "C", "team_a": "Escócia",           "team_b": "Brasil",            "match_date": "2026-06-24T22:00:00+00:00", "stage": "group"},
    {"group_name": "C", "team_a": "Marrocos",          "team_b": "Haiti",             "match_date": "2026-06-24T22:00:00+00:00", "stage": "group"},
    # ── GRUPO D ───────────────────────────────────────────────────────────────
    {"group_name": "D", "team_a": "Estados Unidos",    "team_b": "Paraguai",          "match_date": "2026-06-13T01:00:00+00:00", "stage": "group"},
    {"group_name": "D", "team_a": "Austrália",         "team_b": "Turquia",           "match_date": "2026-06-14T04:00:00+00:00", "stage": "group"},
    {"group_name": "D", "team_a": "Estados Unidos",    "team_b": "Austrália",         "match_date": "2026-06-19T19:00:00+00:00", "stage": "group"},
    {"group_name": "D", "team_a": "Turquia",           "team_b": "Paraguai",          "match_date": "2026-06-20T11:00:00+00:00", "stage": "group"},
    {"group_name": "D", "team_a": "Turquia",           "team_b": "Estados Unidos",    "match_date": "2026-06-26T02:00:00+00:00", "stage": "group"},
    {"group_name": "D", "team_a": "Paraguai",          "team_b": "Austrália",         "match_date": "2026-06-26T02:00:00+00:00", "stage": "group"},
    # ── GRUPO E ───────────────────────────────────────────────────────────────
    {"group_name": "E", "team_a": "Alemanha",          "team_b": "Curaçau",           "match_date": "2026-06-14T17:00:00+00:00", "stage": "group"},
    {"group_name": "E", "team_a": "Costa do Marfim",   "team_b": "Equador",           "match_date": "2026-06-14T23:00:00+00:00", "stage": "group"},
    {"group_name": "E", "team_a": "Alemanha",          "team_b": "Costa do Marfim",   "match_date": "2026-06-20T20:00:00+00:00", "stage": "group"},
    {"group_name": "E", "team_a": "Equador",           "team_b": "Curaçau",           "match_date": "2026-06-21T00:00:00+00:00", "stage": "group"},
    {"group_name": "E", "team_a": "Equador",           "team_b": "Alemanha",          "match_date": "2026-06-25T20:00:00+00:00", "stage": "group"},
    {"group_name": "E", "team_a": "Curaçau",           "team_b": "Costa do Marfim",   "match_date": "2026-06-25T20:00:00+00:00", "stage": "group"},
    # ── GRUPO F ───────────────────────────────────────────────────────────────
    {"group_name": "F", "team_a": "Holanda",           "team_b": "Japão",             "match_date": "2026-06-14T20:00:00+00:00", "stage": "group"},
    {"group_name": "F", "team_a": "Suécia",            "team_b": "Tunísia",           "match_date": "2026-06-15T02:00:00+00:00", "stage": "group"},
    {"group_name": "F", "team_a": "Holanda",           "team_b": "Suécia",            "match_date": "2026-06-20T17:00:00+00:00", "stage": "group"},
    {"group_name": "F", "team_a": "Tunísia",           "team_b": "Japão",             "match_date": "2026-06-21T04:00:00+00:00", "stage": "group"},
    {"group_name": "F", "team_a": "Japão",             "team_b": "Suécia",            "match_date": "2026-06-25T23:00:00+00:00", "stage": "group"},
    {"group_name": "F", "team_a": "Tunísia",           "team_b": "Holanda",           "match_date": "2026-06-25T23:00:00+00:00", "stage": "group"},
    # ── GRUPO G ───────────────────────────────────────────────────────────────
    {"group_name": "G", "team_a": "Bélgica",           "team_b": "Egito",             "match_date": "2026-06-15T19:00:00+00:00", "stage": "group"},
    {"group_name": "G", "team_a": "Irã",               "team_b": "Nova Zelândia",     "match_date": "2026-06-16T01:00:00+00:00", "stage": "group"},
    {"group_name": "G", "team_a": "Bélgica",           "team_b": "Irã",               "match_date": "2026-06-21T19:00:00+00:00", "stage": "group"},
    {"group_name": "G", "team_a": "Nova Zelândia",     "team_b": "Egito",             "match_date": "2026-06-22T01:00:00+00:00", "stage": "group"},
    {"group_name": "G", "team_a": "Egito",             "team_b": "Irã",               "match_date": "2026-06-27T03:00:00+00:00", "stage": "group"},
    {"group_name": "G", "team_a": "Nova Zelândia",     "team_b": "Bélgica",           "match_date": "2026-06-27T03:00:00+00:00", "stage": "group"},
    # ── GRUPO H ───────────────────────────────────────────────────────────────
    {"group_name": "H", "team_a": "Espanha",           "team_b": "Cabo Verde",        "match_date": "2026-06-15T16:00:00+00:00", "stage": "group"},
    {"group_name": "H", "team_a": "Arábia Saudita",    "team_b": "Uruguai",           "match_date": "2026-06-15T22:00:00+00:00", "stage": "group"},
    {"group_name": "H", "team_a": "Espanha",           "team_b": "Arábia Saudita",    "match_date": "2026-06-21T16:00:00+00:00", "stage": "group"},
    {"group_name": "H", "team_a": "Uruguai",           "team_b": "Cabo Verde",        "match_date": "2026-06-21T22:00:00+00:00", "stage": "group"},
    {"group_name": "H", "team_a": "Cabo Verde",        "team_b": "Arábia Saudita",    "match_date": "2026-06-27T00:00:00+00:00", "stage": "group"},
    {"group_name": "H", "team_a": "Uruguai",           "team_b": "Espanha",           "match_date": "2026-06-27T00:00:00+00:00", "stage": "group"},
    # ── GRUPO I ───────────────────────────────────────────────────────────────
    {"group_name": "I", "team_a": "França",            "team_b": "Senegal",           "match_date": "2026-06-16T19:00:00+00:00", "stage": "group"},
    {"group_name": "I", "team_a": "Iraque",            "team_b": "Noruega",           "match_date": "2026-06-16T22:00:00+00:00", "stage": "group"},
    {"group_name": "I", "team_a": "França",            "team_b": "Iraque",            "match_date": "2026-06-22T21:00:00+00:00", "stage": "group"},
    {"group_name": "I", "team_a": "Noruega",           "team_b": "Senegal",           "match_date": "2026-06-23T00:00:00+00:00", "stage": "group"},
    {"group_name": "I", "team_a": "Noruega",           "team_b": "França",            "match_date": "2026-06-26T19:00:00+00:00", "stage": "group"},
    {"group_name": "I", "team_a": "Senegal",           "team_b": "Iraque",            "match_date": "2026-06-26T19:00:00+00:00", "stage": "group"},
    # ── GRUPO J ───────────────────────────────────────────────────────────────
    {"group_name": "J", "team_a": "Argentina",         "team_b": "Argélia",           "match_date": "2026-06-17T01:00:00+00:00", "stage": "group"},
    {"group_name": "J", "team_a": "Áustria",           "team_b": "Jordânia",          "match_date": "2026-06-17T04:00:00+00:00", "stage": "group"},
    {"group_name": "J", "team_a": "Argentina",         "team_b": "Áustria",           "match_date": "2026-06-22T17:00:00+00:00", "stage": "group"},
    {"group_name": "J", "team_a": "Jordânia",          "team_b": "Argélia",           "match_date": "2026-06-23T11:00:00+00:00", "stage": "group"},
    {"group_name": "J", "team_a": "Argélia",           "team_b": "Áustria",           "match_date": "2026-06-28T02:00:00+00:00", "stage": "group"},
    {"group_name": "J", "team_a": "Jordânia",          "team_b": "Argentina",         "match_date": "2026-06-28T02:00:00+00:00", "stage": "group"},
    # ── GRUPO K ───────────────────────────────────────────────────────────────
    {"group_name": "K", "team_a": "Portugal",          "team_b": "R. D. do Congo",    "match_date": "2026-06-17T17:00:00+00:00", "stage": "group"},
    {"group_name": "K", "team_a": "Uzbequistão",       "team_b": "Colômbia",          "match_date": "2026-06-18T02:00:00+00:00", "stage": "group"},
    {"group_name": "K", "team_a": "Portugal",          "team_b": "Uzbequistão",       "match_date": "2026-06-23T17:00:00+00:00", "stage": "group"},
    {"group_name": "K", "team_a": "Colômbia",          "team_b": "R. D. do Congo",    "match_date": "2026-06-24T02:00:00+00:00", "stage": "group"},
    {"group_name": "K", "team_a": "Colômbia",          "team_b": "Portugal",          "match_date": "2026-06-27T23:30:00+00:00", "stage": "group"},
    {"group_name": "K", "team_a": "R. D. do Congo",    "team_b": "Uzbequistão",       "match_date": "2026-06-27T23:30:00+00:00", "stage": "group"},
    # ── GRUPO L ───────────────────────────────────────────────────────────────
    {"group_name": "L", "team_a": "Inglaterra",        "team_b": "Croácia",           "match_date": "2026-06-17T20:00:00+00:00", "stage": "group"},
    {"group_name": "L", "team_a": "Gana",              "team_b": "Panamá",            "match_date": "2026-06-17T23:00:00+00:00", "stage": "group"},
    {"group_name": "L", "team_a": "Inglaterra",        "team_b": "Gana",              "match_date": "2026-06-23T20:00:00+00:00", "stage": "group"},
    {"group_name": "L", "team_a": "Panamá",            "team_b": "Croácia",           "match_date": "2026-06-23T23:00:00+00:00", "stage": "group"},
    {"group_name": "L", "team_a": "Panamá",            "team_b": "Inglaterra",        "match_date": "2026-06-27T21:00:00+00:00", "stage": "group"},
    {"group_name": "L", "team_a": "Croácia",           "team_b": "Gana",              "match_date": "2026-06-27T21:00:00+00:00", "stage": "group"},
]


def get_all_fixtures() -> list[dict]:
    """Return all 72 group stage fixtures."""
    return FIXTURES
