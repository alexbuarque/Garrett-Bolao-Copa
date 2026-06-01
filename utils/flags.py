FLAGS: dict[str, str] = {
    # Grupo A
    "México":            "🇲🇽",
    "África do Sul":     "🇿🇦",
    "Coreia do Sul":     "🇰🇷",
    "República Tcheca":  "🇨🇿",
    # Grupo B
    "Canadá":                "🇨🇦",
    "Bósnia e Herzegovina":  "🇧🇦",
    "Catar":                 "🇶🇦",
    "Suíça":                 "🇨🇭",
    # Grupo C
    "Brasil":    "🇧🇷",
    "Marrocos":  "🇲🇦",
    "Haiti":     "🇭🇹",
    "Escócia":   "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    # Grupo D
    "Estados Unidos":  "🇺🇸",
    "Paraguai":        "🇵🇾",
    "Austrália":       "🇦🇺",
    "Turquia":         "🇹🇷",
    # Grupo E
    "Alemanha":        "🇩🇪",
    "Curaçau":         "🇨🇼",
    "Costa do Marfim": "🇨🇮",
    "Equador":         "🇪🇨",
    # Grupo F
    "Holanda":  "🇳🇱",
    "Japão":    "🇯🇵",
    "Suécia":   "🇸🇪",
    "Tunísia":  "🇹🇳",
    # Grupo G
    "Bélgica":      "🇧🇪",
    "Egito":        "🇪🇬",
    "Irã":          "🇮🇷",
    "Nova Zelândia":"🇳🇿",
    # Grupo H
    "Espanha":       "🇪🇸",
    "Cabo Verde":    "🇨🇻",
    "Arábia Saudita":"🇸🇦",
    "Uruguai":       "🇺🇾",
    # Grupo I
    "França":   "🇫🇷",
    "Senegal":  "🇸🇳",
    "Iraque":   "🇮🇶",
    "Noruega":  "🇳🇴",
    # Grupo J
    "Argentina": "🇦🇷",
    "Argélia":   "🇩🇿",
    "Áustria":   "🇦🇹",
    "Jordânia":  "🇯🇴",
    # Grupo K
    "Portugal":       "🇵🇹",
    "R. D. do Congo": "🇨🇩",
    "Uzbequistão":    "🇺🇿",
    "Colômbia":       "🇨🇴",
    # Grupo L
    "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Croácia":    "🇭🇷",
    "Gana":       "🇬🇭",
    "Panamá":     "🇵🇦",
}


def flag(team: str) -> str:
    return FLAGS.get(team, "")


def with_flag(team: str) -> str:
    f = FLAGS.get(team, "")
    return f"{f} {team}" if f else team
