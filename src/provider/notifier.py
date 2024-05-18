
from notifypy import Notify
from src import __app_name__, __version__

class Notifier:
    notification = None

    def __init__(self):
        self.notification = Notify()
        self.notification.application_name = f"{__app_name__} v{__version__}"

    def send(self, title, message):
        self.notification.title = title
        self.notification.message = message
        self.notification.send()