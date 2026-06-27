def calculate_match_points(
    pred_a: int,
    pred_b: int,
    result_a: int,
    result_b: int,
    pred_penalties: bool = False,
    pred_pen_a: int | None = None,
    pred_pen_b: int | None = None,
    result_penalties: bool = False,
    result_pen_a: int | None = None,
    result_pen_b: int | None = None,
) -> int:
    def winner(a, b):
        return "a" if a > b else ("b" if b > a else "draw")

    # Base score (regulation / extra time)
    if pred_a == result_a and pred_b == result_b:
        base = 5
    elif winner(pred_a, pred_b) == winner(result_a, result_b):
        base = 3
    else:
        base = 0

    # Penalty bonus — only awarded when match actually went to penalties
    # and the user predicted penalties with a valid score
    pen_bonus = 0
    if (
        result_penalties
        and pred_penalties
        and pred_pen_a is not None
        and pred_pen_b is not None
        and result_pen_a is not None
        and result_pen_b is not None
    ):
        if pred_pen_a == result_pen_a and pred_pen_b == result_pen_b:
            pen_bonus = 3  # exact penalty score
        elif winner(pred_pen_a, pred_pen_b) == winner(result_pen_a, result_pen_b):
            pen_bonus = 1  # correct penalty winner

    return base + pen_bonus
