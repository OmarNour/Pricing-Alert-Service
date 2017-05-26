# views are the end point of the API that's related to the user
from flask import Blueprint, render_template, request, session, redirect, url_for

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as UserDecorators

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
def index():
    return "this is alerts' index"


@alert_blueprint.route('/new', methods=['GET','POST'])
@UserDecorators.requires_login
def create_alert():

    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        item = Item(name, url)
        item.save_to_mongo()

        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price()

        return redirect(url_for('users.user_alerts'))
    return render_template("alerts/new_alert.jinja2")


@alert_blueprint.route('/deactivate/<string:alert_id>')
@UserDecorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('.get_alert_page',alert_id=alert_id))


@alert_blueprint.route('/activate/<string:alert_id>')
@UserDecorators.requires_login
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('.get_alert_page',alert_id=alert_id))



@alert_blueprint.route('/<string:alert_id>')
@UserDecorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template("alerts/alert.jinja2", alert=alert)


@alert_blueprint.route('/alert/<string:user_id>')
def get_alerts_for_user(user_id):
    pass


@alert_blueprint.route('/edit/<string:alert_id>')
@UserDecorators.requires_login
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template("alerts/edit_alert.jinja2", alert=alert)


@alert_blueprint.route('/delete/<string:alert_id>')
@UserDecorators.requires_login
def delete_alert(alert_id):
    Alert.find_by_id(alert_id).delete()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
    Alert.find_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))
