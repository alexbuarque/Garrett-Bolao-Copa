def calculate_match_points(pred_a: int, pred_b: int, result_a: int, result_b: int) -> int:
    """
    5 pts: exact score
    3 pts: correct winner/draw (but wrong score) + partial goal bonuses below
    +1 pt per team whose goal count was correctly predicted (only when score is NOT exact)
    """
    if pred_a == result_a and pred_b == result_b:
        return 5

    def winner(a, b):
        return "a" if a > b else ("b" if b > a else "draw")

    pts = 3 if winner(pred_a, pred_b) == winner(result_a, result_b) else 0
    if pred_a == result_a:
        pts += 1
    if pred_b == result_b:
        pts += 1
    return pts


def calculate_special_points(pred: dict, result: dict) -> int:
    """10 pts for each correct special prediction (case-insensitive, stripped)."""
    pts = 0
    for field in ("artilheiro", "mvp", "goleiro"):
        p = (pred.get(field) or "").strip().lower()
        r = (result.get(field) or "").strip().lower()
        if p and r and p == r:
            pts += 10
    return pts
