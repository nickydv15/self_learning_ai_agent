# ==============================
# CALCULATOR TOOL
# ==============================

def calculator(expression):

    try:
        result = eval(
            expression,
            {"__builtins__": None},
            {}
        )

        return f"Calculator Result: {result}"

    except Exception:

        return "Calculator Error: Invalid expression."


# ==============================
# AUTOMATIC CALCULATION DETECTION
# ==============================

def is_calculation(text):

    text = text.lower().strip()

    allowed_chars = "0123456789+-*/().% "

    if text and all(
        char in allowed_chars
        for char in text
    ):

        has_number = any(
            char.isdigit()
            for char in text
        )

        has_operator = any(
            char in "+-*/%"
            for char in text
        )

        if has_number and has_operator:
            return True

    return False