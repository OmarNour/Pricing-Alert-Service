from src.common.database import Database
from src.models.alerts.alert import Alert


Database.initialize()
alerts_need_update = Alert.find_needs_update()

for alert in alerts_need_update:
    print(alert._id)
    alert.load_item_price()
    alert.send_email_if_price_reached()

