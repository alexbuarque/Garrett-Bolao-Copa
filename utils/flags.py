FLAG_CODES: dict[str, str] = {
    # Grupo A
    "México":            "mx",
    "África do Sul":     "za",
    "Coreia do Sul":     "kr",
    "República Tcheca":  "cz",
    # Grupo B
    "Canadá":                "ca",
    "Bósnia e Herzegovina":  "ba",
    "Catar":                 "qa",
    "Suíça":                 "ch",
    # Grupo C
    "Brasil":    "br",
    "Marrocos":  "ma",
    "Haiti":     "ht",
    "Escócia":   "gb-sct",
    # Grupo D
    "Estados Unidos":  "us",
    "Paraguai":        "py",
    "Austrália":       "au",
    "Turquia":         "tr",
    # Grupo E
    "Alemanha":        "de",
    "Curaçau":         "cw",
    "Costa do Marfim": "ci",
    "Equador":         "ec",
    # Grupo F
    "Holanda":  "nl",
    "Japão":    "jp",
    "Suécia":   "se",
    "Tunísia":  "tn",
    # Grupo G
    "Bélgica":      "be",
    "Egito":        "eg",
    "Irã":          "ir",
    "Nova Zelândia":"nz",
    # Grupo H
    "Espanha":        "es",
    "Cabo Verde":     "cv",
    "Arábia Saudita": "sa",
    "Uruguai":        "uy",
    # Grupo I
    "França":   "fr",
    "Senegal":  "sn",
    "Iraque":   "iq",
    "Noruega":  "no",
    # Grupo J
    "Argentina": "ar",
    "Argélia":   "dz",
    "Áustria":   "at",
    "Jordânia":  "jo",
    # Grupo K
    "Portugal":       "pt",
    "R. D. do Congo": "cd",
    "Uzbequistão":    "uz",
    "Colômbia":       "co",
    # Grupo L
    "Inglaterra": "gb-eng",
    "Croácia":    "hr",
    "Gana":       "gh",
    "Panamá":     "pa",
}

_IMG = '<img src="https://flagcdn.com/w20/{code}.png" style="vertical-align:middle;margin-right:3px">'


def flag_html(team: str) -> str:
    """Return an <img> tag for the team's flag, or empty string if unknown."""
    code = FLAG_CODES.get(team)
    return _IMG.format(code=code) if code else ""


def with_flag_html(team: str) -> str:
    """Return flag <img> + team name as HTML string."""
    return f"{flag_html(team)}{team}"
