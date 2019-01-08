from ..models import *
from .Push import *
import time


class PushNotifier(QThread):

    logs = pyqtSignal('QString')

    def __init__(self, discord, parent):
        super(PushNotifier, self).__init__(parent)
        QThread.__init__(self, parent)
        self.send_to = ''
        self.search_keyword = ''
        self.logs.emit('[LOG] Push notification set up  ')
        self.discord = discord

    def init_notify(self, discord, user, search_keyword):
        self.logs.emit('[LOG] preparing Push Notifier : ' + self.send_to)
        self.send_to = user
        self.search_keyword = search_keyword
        self.discord = discord

    def run(self):
        self.logs.emit("[LOG] Push Notifier started succesfully : ")
        search_db = Search()
        initial_search = search_db.searchkeyword_tp(str(self.search_keyword))
        self.logs.emit('[LOG] Push Notifier prepared ')
        txt = "MONITORING Started"
        print(str(len(initial_search)) + " URLS in initial Search")
        if str(self.discord) == 'Discord':
            self.dm_discord(self.send_to, txt)
        else:
            self.dm_slack(self.send_to, txt)
        self.logs.emit("[LOG] Notification SENT " + txt)
        while True:
            print('0')
            time.sleep(10)
            print('1')
            try:
                current_search = search_db.searchkeyword_tp(str(self.search_keyword))
                print('2')
                found = current_search - initial_search
                print('3')
                if found:
                    self.logs.emit("[LOG] FOUND NEW PRODUCTS ")
                    play_music('media/ding.mp3')
                    p = Push(self.discord, self.send_to, list(found))
                    p.start()
                initial_search = current_search
            except Exception as e:
                print(str(e))

    @staticmethod
    def dm_slack(access_token, text):
        # https://hooks.slack.com/services/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
        print("SLACK data:" + str(access_token) + '   ' + str(text))
        requests.post(
            access_token, data=json.dumps({'text': text}),
            headers={'Content-Type': 'application/json'}
        )

    @staticmethod
    def dm_discord(access_token, text):
        msg = Webhook(access_token, msg=text)
        msg.post()
