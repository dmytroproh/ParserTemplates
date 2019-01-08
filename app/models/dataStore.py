import sqlite3
import time
from PyQt5.QtCore import QThread, pyqtSignal
from ..serviceManager import *


class DataStore(QThread):
    logs = pyqtSignal('QString')

    def __init__(self, parent=None, dbfile='mod/data.db'):
        super(DataStore, self).__init__(parent)
        QThread.__init__(self, parent)
        self.file = dbfile
        self.op = None
        self.lliisstt = None

    def set_op(self, op, datalist):
        self.lliisstt = datalist
        self.op = op

    def stor(self, tlist):
        try:
            with sqlite3.connect(self.file, isolation_level=None) as conn:
                c = conn.cursor()
                """
                conn.executemany("INSERT INTO headlines (heds, url, image_loc, time, source) VALUES (?,?,?,?,?)", listicle)
                """
                c.executemany("INSERT OR IGNORE  INTO datatable (loc,lastmod) VALUES (?,?)", tlist)
                conn.commit()
                time.sleep(1)
                print("ADDED " + str(len(tlist)))
                self.logs.emit("[LOG] DATA SAVED TO DISC FOR FUTURE USES ")
        except Exception:
            print_exception_info("ERROR OCCURRED WHEN trying to STore Data", Exception)

    def run(self):
        if self.op is None:
            pass
        else:
            try:
                print(["('" + each['loc'] + "' , '" + each['lastmod'] + "')" for each in self.lliisstt][0])
                print(["('" + each['loc'] + "' , '" + each['lastmod'] + "')" for each in self.lliisstt][0])
                self.stor([(each['loc'], each['lastmod']) for each in self.lliisstt])
            except Exception:
                print_exception_info("No urls or sitemap locked", Exception)
        print("FINISHED DATABASE OPERATION")
