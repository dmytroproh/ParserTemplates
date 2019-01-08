from shutil import copyfile
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QSplashScreen
from .controlers import *
from .models import *
from .regkey_manager import *
from .uix import *
from .serviceManager import *
from requests import get


class MainApp(QMainWindow, everossui.Ui_everossgui):
    def __init__(self, parent=None):
        self.version = int('021')
        # attributes
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        # initializations
        self.stdo.setEnabled(True)
        print("LOG FILE STARTED ")
        print("PROGRAM STARTED AT : " + str(datetime.now()))
        self.qFileDialog = QtWidgets.QFileDialog()
        self.safeConfigParser = SafeConfigParser()
        self.safeConfigParser.read('mod/cfg.ini')
        self.sitemapsParser = SitemapsParser(self, 'mod/cfg.ini')
        self.setup_object(self.sitemapsParser)
        self.sitemapsParser.load_proxies()
        print(" SG stack size is " + str(self.sitemapsParser.stackSize()))
        print("CONFIG FILE cfg.ini LOADED ")
        # Database objects
        print("DATABASE FILE data.db LOADED")
        # twitter Object :
        self.pushNotifier = PushNotifier(self.webhook_combo.currentText(), self)
        self.setup_object(self.pushNotifier)
        print("TT stack size is " + str(self.pushNotifier.stackSize()))
        self.appNotifier = AppNotifier(self)
        self.setup_object(self.appNotifier)
        self.appNotifier.MDM.connect(self.got_mdm)
        print(" M stack size is " + str(self.appNotifier.stackSize()))
        print("TWITTER NOTIFIER INITIATED")
        self.search = Search(self)
        self.setup_object(self.search)
        self.search.search_result.connect(self.search_result_ev)
        self.connect_buttons()
        try:
            self.check_for_license()
        except Exception:
            print_exception_info("ERROR OCCURRED WHEN Checking for Licence", Exception)
        try:
            self.twit_usr.setText(open('Push.token', 'r').read())
        except Exception:
            print_exception_info("ERROR OCCURRED : No Token file found", Exception)

    def connect_buttons(self):
        self.datequ.toggled.connect(self.datequ_clicked)
        self.updatedbbtn.clicked.connect(self.updatedb_click)
        self.exitbtn.clicked.connect(self.close)
        self.go.clicked.connect(self.go_clicked)
        self.keyword.returnPressed.connect(self.go_clicked)
        self.Noti_On.clicked.connect(self.notif_on_clicked)
        self.Noti_OFF.clicked.connect(self.notif_off_click)
        self.go_2.clicked.connect(self.app_notif_on_clicked)
        self.keyword_2.returnPressed.connect(self.app_notif_on_clicked)
        self.clearBtn_2.clicked.connect(self.app_notif_off_click)
        self.activate.clicked.connect(self.register)
        #self.resett.clicked.connect(self.reset_database)

    def setup_object(self, obj):
        obj.setTerminationEnabled(True)
        obj.logs.connect(self.sglog)

    def create_message_box(self, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("EVE Robotics Scraper Y")
        msg.show()

    def reset_database(self):
        copyfile('mod/rdata.db', 'mod/data.db')
        self.create_message_box("Database clean now")

    def check_update(self):
        if int(get('https://eve-robotics.com/version_controll/versiony.html').content) > self.version:
            self.create_message_box("This program is Outdated \n download lastest version\n join us on slack " +
                                    "#uptades to get the latest version for free", "EVE Robotics Scraper Y")

    def app_notif_off_click(self):
        self.go_2.setEnabled(False)
        self.clearBtn_2.setEnabled(False)
        QApplication.processEvents()
        self.appNotifier.terminate()
        QApplication.processEvents()
        self.go_2.setEnabled(True)
        self.clearBtn_2.setEnabled(False)
        self.sglog("Monitor  stopped successfully")

    def app_notif_on_clicked(self):
        if self.check_for_license():
            self.resultscreen_2.clear()
            try:
                self.appNotifier.init_notify(str(self.keyword_2.text()))
                QApplication.processEvents()
                self.appNotifier.start()
                QApplication.processEvents()
                self.clearBtn_2.setEnabled(True)
                self.go_2.setEnabled(False)
            except Exception:
                print_exception_info("ERROR OCCURRED WHEN trying to start Notifier", Exception)

    def got_mdm(self, txt):
        for i in txt:
            self.resultscreen_2.append(i)
            QApplication.processEvents()

    def register(self):
        print("HELLO")
        lic_key = str(self.keyEdit.text())
        print(lic_key)
        self.setUpdatesEnabled(False)
        chk = check_lic(lic_key)
        #chk = check_lic(key.split('|'))[0]
        #chk = {'status': 'pending', 'result': 'success'}
        #print(repr(chk))
        if chk is not None:
            try:
                if chk['status'] == 'pending' and chk['result'] == 'success':
                    chk2 = activate_lic(lic_key, "|ScraperY|" + str(machine_id()))
                    #chk2 = 'lol'
                    if chk2 is not None:
                        if chk['result'] == 'success':
                            ff = open('reg.lic', 'w')
                            d = encrypt(lic_key + "|ScraperY|" + str(machine_id()))
                            ff.write(str(d.decode("utf-8")))
                            ff.close()
                            self.create_message_box("Software Registered \n Thank you for purchrase")
                            self.keyEdit.setEnabled(False)
                            self.activate.setEnabled(False)
                        else:
                            self.create_message_box("Could Not register the software \n Please contact us to help you")
                    else:
                        self.create_message_box("No INTERNET Connection ")
            except Exception as e:
                print(str(e))
                self.create_message_box("Invalid Registration Key")
        else:
            self.create_message_box("No INTERNET Connection ")
        self.setUpdatesEnabled(True)

    def search_result_ev(self):
        self.resultscreen.clear()
        for line in open('searchresult.tmp', 'r'):
            x = eval(line)
            self.resultscreen.append('<a href="' + x['loc'] + '">' + x['loc'] + '</a>')
            QApplication.processEvents()
        QApplication.processEvents()
        self.go.setEnabled(True)
        self.keyword.setEnabled(True)
        QApplication.processEvents()
        self.keyword.returnPressed.connect(self.go_clicked)
        self.setEnabled(True)
        self.maintabs.setCurrentIndex(1)

    def notif_off_click(self):
        self.Noti_On.setEnabled(True)
        self.Noti_OFF.setEnabled(False)
        QApplication.processEvents()
        self.pushNotifier.terminate()
        QApplication.processEvents()
        self.sglog("Notifier stopped succesfully")

    def notif_on_clicked(self):
        do = open('Push.token', 'w')
        do.write(str(self.twit_usr.text()))
        do.close()
        if self.check_for_license():
            self.pushNotifier.init_notify(self.webhook_combo.currentText(),
                                          str(self.twit_usr.text()),
                                          str(self.Noti_kwrd.text()))
            self.Noti_OFF.setEnabled(True)
            self.Noti_On.setEnabled(False)
            QApplication.processEvents()
            self.pushNotifier.start()
            QApplication.processEvents()

    def updatedb_click(self):
        if self.check_for_license():
            self.sglog("LIVE MOD IS ON  AT " + str(datetime.now()))
            QApplication.processEvents()
            self.sitemapsParser.start()
            QApplication.processEvents()
            self.updatedbbtn.setEnabled(False)

    def sglog(self, message):
        print("MESSAGE : " + message)
        self.stdo.append(message)

    def datequ_clicked(self, enabled):
            self.fromdate.setEnabled(enabled)

    def go_clicked(self):
        if self.check_for_license():
            self.keyword.returnPressed.disconnect(self.go_clicked)
            self.go.setEnabled(False)
            self.keyword.setEnabled(False)
            self.resultscreen.append('Search initiated')
            self.stdo.append('[LOG]Search started')
            if self.datequ.isChecked():
                self.search.set(str(self.keyword.text()), str(self.fromdate.date().toPyDate()))
            else:
                self.search.set(str(self.keyword.text()))
            self.resultscreen.clear()
            self.resultscreen.setText('please wait')
            self.search.start()

    def check_for_license(self):
        try:
            ff = open('reg.lic', 'r')
            df = ff.read()
        except Exception as e:
            print(str(e))
            self.sglog("lic file not found")
            self.keyEdit.setEnabled(True)
            self.activate.setEnabled(True)
            self.create_message_box("This program is not registered")
            return False
        key = decrypt(df)

        print("KEY DECR " + key)
        #chk = {'status': 'active', 'result': 'success'}
        chk = check_lic(key.split('|')[0])
        #chk['registered_domains'] = [{'registered_domain': "|ScraperY|" + str(machine_id())}]
        if chk is not None:
            #print(str(chk))
            if chk['status'] == 'active' and chk['result'] == 'success':
                if chk['registered_domains'][0]['registered_domain'] == "|ScraperY|" + str(machine_id()):
                    self.keyEdit.setText("ACTIVATED")
                    self.keyEdit.setEnabled(False)
                    self.activate.setEnabled(False)
                    self.check_update()
                    return True
                else:
                    self.keyEdit.setEnabled(True)
                    self.activate.setEnabled(True)
                    self.create_message_box("This program is not registered\n pleas contact us \n if you think this is an error ")
                    return False
            elif chk['result'] == 'success':
                self.keyEdit.setEnabled(True)
                self.activate.setEnabled(True)
                self.create_message_box(
                    "This program is not registered\n pleas contact us \n if you think this is an error ")
                return False
        else:
            self.create_message_box("INTERNET Connection error")
            return False
