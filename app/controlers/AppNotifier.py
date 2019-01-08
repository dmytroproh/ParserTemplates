from ..models import *
from ..serviceManager import *


class AppNotifier(QThread):
    logs = pyqtSignal('QString')
    MDM = pyqtSignal(object)

    def __init__(self, parent):
        super(AppNotifier, self).__init__(parent)
        QThread.__init__(self, parent)
        self.setTerminationEnabled(True)
        self.logs.emit("[LOG] Monitor set up  ")
        self.search_keyword = ''
        self.initial_search = []

    def init_notify(self, search_keyword):
        self.logs.emit("[LOG] preparing Monitoring  : ")
        self.search_keyword = search_keyword

    def run(self):
        self.logs.emit("[LOG] Monitor started succesfully : ")
        search_db = Search()
        self.initial_search = search_db.searchkeyword_tp(str(self.search_keyword))
        self.logs.emit("[LOG] Monitor  prepared ")
        txt = "EVE ROBOTICS SCRAPPER MONITOR INITIATION  : GOT "
        txt += str(len(self.initial_search)) + " URLS in initial Search"

        self.MDM.emit([txt])
        self.logs.emit("[LOG] " + txt)
        while True:
            time.sleep(10)
            try:
                current_search = search_db.searchkeyword_tp(str(self.search_keyword))
                found = current_search - self.initial_search
                if found:
                    self.logs.emit("[LOG] FOUND NEW PRODUCTS ")
                    play_music('media/ding.mp3')
                    txt = ['< a href = "' + i + '" > ' + i + ' < / a >' for i in list(found)]
                    self.MDM.emit(txt)
                self.initial_search = current_search
            except Exception as e:
                time.sleep(1)
                print(str(e))
