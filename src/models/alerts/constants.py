import os

URL = os.environ.get("MAILGUN_URL") #"https://api.mailgun.net/v3/sandbox2073d69f7bbb40a49bf744459ef1a2e4.mailgun.org/messages"
API_KEY = os.environ.get("MAILGUN_API_KEY") #"key-975c4f19083c573acec531e7d2c6a566"
FROM = os.environ.get("MAILGUN_FROM") #"Mailgun Sandbox <postmaster@sandbox2073d69f7bbb40a49bf744459ef1a2e4.mailgun.org>"
ALERT_TIMEOUT = (1/24)/60
COLLECTION = "alerts"
