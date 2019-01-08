from sys import exit, argv
from gc import disable
from app import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


def main():
    disable()
    application = QtWidgets.QApplication(argv)
    # Create and display the splash screen
    splash_pix = QPixmap('media/see.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    play_music('media/hear.mp3')
    # time.sleep(3)
    application.processEvents()
    form = MainApp()
    form.show()
    splash.finish(form)
    exit(application.exec_())
#lol

if __name__ == '__main__':
    try:
        main()
        print("program closed  AT " + str(datetime.now()))
    except Exception:
        print_exception_info("ERROR OCCURRED WHEN Starting APP", Exception)

