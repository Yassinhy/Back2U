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

def save_item(photo, Title, Sdesc, Ldesc, user_id):
    original_filename = secure_filename(photo.file_name)
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
    photos.save(photo, name = unique_filename)
    db.execute("INSERT INTO ITEMS (user_id, picture, title, short_description, description) VALUES (?, ?, ?, ?, ?)",
                                   user_id, unique_filename, Title, Sdesc, Ldesc)

