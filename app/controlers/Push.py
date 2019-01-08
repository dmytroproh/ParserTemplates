from PyQt5.QtCore import QThread
from .Webhook import *
from ..serviceManager import *
from bs4 import BeautifulSoup


class Push(QThread):
    def __init__(self, discord, acc_token, urls, parent=None):
        super(Push, self).__init__(parent)
        QThread.__init__(self, parent)
        self.urls = urls
        self.auth = acc_token
        self.discord = discord

    def run(self):
        print("Sending Notification ......")
        for each_url in self.urls:
            txt = self.get_prod_name(each_url) + '  :  \n'
            txt += each_url
            try:
                if str(self.discord) == 'Discord':
                    self.dm_discord(self.auth, txt)
                else:
                    self.dm_slack(self.auth, txt)
                print("Notification Sent ,")
            except Exception:
                print_exception_info("ERROR OCCURRED WHEN dm", Exception)

    @staticmethod
    def dm_slack(access_token, text):
        # https://hooks.slack.com/services/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
        webhook_url = access_token
        slack_data = {'text': text}
        requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )

    @staticmethod
    def dm_discord(access_token, text):
        msg = Webhook(access_token, msg=text)
        msg.post()

    @staticmethod
    def get_prod_name(url):
        return BeautifulSoup(requests.get(url).text, "html.parser").title.text
