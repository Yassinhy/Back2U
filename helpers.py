from flask import redirect, session
from functools import wraps

##################################################################################################################################################
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

##################################################################################################################################################
def check_pass(string):
    """check if password is strong enough."""
    s1 = False
    s2 = False

    symbols = ['!', '@', '#', '$', '%', '*', '/', '<', '>', ';', ':', '~', '+', '_', '-', '(', ')']
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    for symbol in symbols:
        if (symbol in string):
            s1 = True
            break

    for num in nums:
        if (num in string):
            s2 = True
            break
    if (s1 == True and s2 == True):
        return True
    else:
        return False

##################################################################################################################################################
def gradient_color(score):
    score = max(0, min(100, score))
    if score <= 50:
        red = 255
        green = int(255 * (score / 50))  # 0 → 255
    else:
        red = int(255 * ((100 - score) / 50))  # 255 → 0
        green = 255
    return f"#{red:02X}{green:02X}00"