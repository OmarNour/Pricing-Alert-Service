from flask import Flask, render_template, session, redirect, url_for
from src.common.database import Database
from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint
from src.models.users.views import user_blueprint


app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    if session['email'] is None:
        return render_template('home.jinja2')
    else:
        return redirect(url_for('users.user_alerts'))



app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(user_blueprint, url_prefix="/users")


