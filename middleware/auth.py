import functools
from flask import session, redirect, url_for


def auth(view_func):
    @functools.wraps(view_func)
    def decorated(*args, **kwargs):
        if (
            "user_id" not in session
        ):  # Adjust the session key to match the one used in your login route
            return redirect("/login")
        return view_func(*args, **kwargs)

    return decorated
