def calculate_match_points(pred_a: int, pred_b: int, result_a: int, result_b: int) -> int:
    if pred_a == result_a and pred_b == result_b:
        return 5

    def winner(a, b):
        return "a" if a > b else ("b" if b > a else "draw")

    return 3 if winner(pred_a, pred_b) == winner(result_a, result_b) else 0


def calculate_special_points(pred: dict, result: dict) -> int:
    """10 pts for each correct special prediction (case-insensitive, stripped)."""
    pts = 0
    for field in ("artilheiro", "mvp", "goleiro"):
        p = (pred.get(field) or "").strip().lower()
        r = (result.get(field) or "").strip().lower()
        if p and r and p == r:
            pts += 10
    return pts
