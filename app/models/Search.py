import sqlite3
from PyQt5.QtCore import QThread, pyqtSignal


class Search(QThread):

    logs = pyqtSignal('QString')
    search_result = pyqtSignal()

    def __init__(self, parent=None):
        super(Search, self).__init__(parent)
        QThread.__init__(self, parent)
        self.query = ''
        self.date = None

    def set(self, query, date=None):
        self.query = query
        self.date = date

    def run(self):
        self.logs.emit("[LOG] Search started ")
        searchresult = self.searchkeyword(self.query, self.date)
        sfile = open('searchresult.tmp', 'w')
        sfile.write('\n'.join([str(i) for i in searchresult]))
        sfile.close()
        self.logs.emit("[LOG] Search Thread finished  found : " + str(len(searchresult)))
        self.search_result.emit()

    def searchkeyword(self, ser, lastmod=None):
        with sqlite3.connect('mod/data.db', isolation_level=None) as conn:
            result = []
            rows = conn.cursor().execute(self.build_querry(str(ser), lastmod))
            for row in rows:
                result.append({'loc': row[0], 'lastmod': row[1]})
            return result

    @staticmethod
    def par(string):
        return "(" + string + ")"

    def searchkeyword_tp(self, ser):
        with sqlite3.connect('mod/data.db', isolation_level=None) as conn:
            result = []
            rows = conn.cursor().execute(self.build_querry(str(ser)))
            for row in rows:
                result.append(row[0])
            return set(result)

    @staticmethod
    def cap(string):
        return "'%" + string + "%'"

    def build_querry(self, string, lastmod=None):
        print('BUILDING query')
        print(string)
        b = None
        try:
            b = string.split('#')[1]
        except IndexError:
            pass
        qq = "SELECT * FROM DATATABLE WHERE "
        l1 = string.split('#')[0].split(',')
        l2 = [j.split('&') for j in l1]
        qq += self.par("loc LIKE  " + ' OR loc LIKE '.join(' AND loc LIKE '.join([self.cap(h) for h in c]) for c in l2))
        if not (b is None):
            l1 = b.split(',')
            l2 = [j.split('&') for j in l1]
            qq += " AND NOT"
            qq += self.par("loc  LIKE  "
                           + ' OR loc  LIKE '.join(self.par(' AND '.join([self.cap(h) for h in c])) for c in l2))
        if lastmod is not None:
            qq += ' AND ' + self.par(" lastmod LIKE '" + lastmod + "'")

        qq += ";"
        print(qq)
        return qq

    def __del__(self):
        self.terminate()
        self.wait()
