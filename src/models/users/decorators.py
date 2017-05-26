from functools import wraps
from flask import session, flash, redirect, url_for, request
import src.config as app_configurations


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            #flash(u'You need to be signed in for this page.')
            return redirect(url_for('users.login_user', next=request.path))
        return f(*args, **kwargs)

    return decorated_function


def requires_permission(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in app_configurations.ADMINS:
            return redirect(url_for('stores.index'))
        return f(*args, **kwargs)

    return decorated_function