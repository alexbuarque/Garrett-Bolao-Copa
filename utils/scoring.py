def calculate_match_points(pred_a: int, pred_b: int, result_a: int, result_b: int) -> int:
    if pred_a == result_a and pred_b == result_b:
        return 5

    def winner(a, b):
        return "a" if a > b else ("b" if b > a else "draw")

    return 3 if winner(pred_a, pred_b) == winner(result_a, result_b) else 0
