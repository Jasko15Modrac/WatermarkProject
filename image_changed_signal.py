from PyQt5.QtCore import pyqtSignal, QObject


# Here we create ImageSignal class which will connect main_window with TextWidget and LogoWidget
class ImageSignal(QObject):
    signal = pyqtSignal(str)
