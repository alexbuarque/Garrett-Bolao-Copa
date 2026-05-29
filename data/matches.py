"""
2026 FIFA World Cup group stage fixtures.
12 groups (A-L), 4 teams each, 6 matches per group = 72 total.
Teams based on confirmed qualifiers. Dates/times are UTC.
"""
from datetime import datetime, timezone

GROUPS = {
    "A": ["USA", "El Salvador", "Polônia", "Austrália"],
    "B": ["México", "Jamaica", "Sérvia", "Argélia"],
    "C": ["Canadá", "Honduras", "Croácia", "Costa do Marfim"],
    "D": ["Argentina", "Panamá", "Turquia", "Japão"],
    "E": ["Brasil", "Trindade e Tobago", "Holanda", "Marrocos"],
    "F": ["Colômbia", "Costa Rica", "Bélgica", "Coreia do Sul"],
    "G": ["Uruguai", "Nova Zelândia", "Alemanha", "Nigéria"],
    "H": ["Equador", "Portugal", "Irã", "Senegal"],
    "I": ["Chile", "França", "Arábia Saudita", "Egito"],
    "J": ["Paraguai", "Inglaterra", "Catar", "Camarões"],
    "K": ["Venezuela", "Espanha", "Iraque", "Mali"],
    "L": ["Itália", "Suíça", "Uzbequistão", "África do Sul"],
}

# (group, round1_day, round2_day, round3_day)
GROUP_SCHEDULE = {
    "A": (datetime(2026, 6, 11, tzinfo=timezone.utc), datetime(2026, 6, 17, tzinfo=timezone.utc), datetime(2026, 6, 24, tzinfo=timezone.utc)),
    "B": (datetime(2026, 6, 11, tzinfo=timezone.utc), datetime(2026, 6, 17, tzinfo=timezone.utc), datetime(2026, 6, 24, tzinfo=timezone.utc)),
    "C": (datetime(2026, 6, 12, tzinfo=timezone.utc), datetime(2026, 6, 18, tzinfo=timezone.utc), datetime(2026, 6, 25, tzinfo=timezone.utc)),
    "D": (datetime(2026, 6, 12, tzinfo=timezone.utc), datetime(2026, 6, 18, tzinfo=timezone.utc), datetime(2026, 6, 25, tzinfo=timezone.utc)),
    "E": (datetime(2026, 6, 13, tzinfo=timezone.utc), datetime(2026, 6, 19, tzinfo=timezone.utc), datetime(2026, 6, 26, tzinfo=timezone.utc)),
    "F": (datetime(2026, 6, 13, tzinfo=timezone.utc), datetime(2026, 6, 19, tzinfo=timezone.utc), datetime(2026, 6, 26, tzinfo=timezone.utc)),
    "G": (datetime(2026, 6, 14, tzinfo=timezone.utc), datetime(2026, 6, 20, tzinfo=timezone.utc), datetime(2026, 6, 27, tzinfo=timezone.utc)),
    "H": (datetime(2026, 6, 14, tzinfo=timezone.utc), datetime(2026, 6, 20, tzinfo=timezone.utc), datetime(2026, 6, 27, tzinfo=timezone.utc)),
    "I": (datetime(2026, 6, 15, tzinfo=timezone.utc), datetime(2026, 6, 21, tzinfo=timezone.utc), datetime(2026, 6, 28, tzinfo=timezone.utc)),
    "J": (datetime(2026, 6, 15, tzinfo=timezone.utc), datetime(2026, 6, 21, tzinfo=timezone.utc), datetime(2026, 6, 28, tzinfo=timezone.utc)),
    "K": (datetime(2026, 6, 16, tzinfo=timezone.utc), datetime(2026, 6, 22, tzinfo=timezone.utc), datetime(2026, 6, 29, tzinfo=timezone.utc)),
    "L": (datetime(2026, 6, 16, tzinfo=timezone.utc), datetime(2026, 6, 22, tzinfo=timezone.utc), datetime(2026, 6, 29, tzinfo=timezone.utc)),
}

# Hours offset for first/second group sharing a day
# Odd-named groups (A,C,E,G,I,K) use earlier slots; even (B,D,F,H,J,L) use later slots
GROUP_HOURS = {
    "A": (13, 16, 18), "B": (19, 22, 21),
    "C": (13, 16, 18), "D": (19, 22, 21),
    "E": (13, 16, 18), "F": (19, 22, 21),
    "G": (13, 16, 18), "H": (19, 22, 21),
    "I": (13, 16, 18), "J": (19, 22, 21),
    "K": (13, 16, 18), "L": (19, 22, 21),
}


def _dt(base: datetime, hour: int) -> datetime:
    return base.replace(hour=hour, minute=0, second=0)


def get_all_fixtures() -> list[dict]:
    """Return all 72 group stage fixtures as a list of dicts."""
    fixtures = []
    match_id = 1
    for group in sorted(GROUPS.keys()):
        teams = GROUPS[group]
        r1, r2, r3 = GROUP_SCHEDULE[group]
        h1, h2, h3 = GROUP_HOURS[group]
        t0, t1, t2, t3 = teams
        rounds = [
            # Round 1
            (t0, t1, _dt(r1, h1)),
            (t2, t3, _dt(r1, h2)),
            # Round 2
            (t0, t2, _dt(r2, h1)),
            (t1, t3, _dt(r2, h2)),
            # Round 3 (simultaneous)
            (t0, t3, _dt(r3, h3)),
            (t1, t2, _dt(r3, h3)),
        ]
        for team_a, team_b, dt in rounds:
            fixtures.append({
                "id": match_id,
                "group_name": group,
                "team_a": team_a,
                "team_b": team_b,
                "match_date": dt.isoformat(),
                "stage": "group",
            })
            match_id += 1
    return fixtures


TOURNAMENT_START = datetime(2026, 6, 11, 13, 0, 0, tzinfo=timezone.utc)
