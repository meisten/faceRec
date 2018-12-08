from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal

from src.services.Loader import Loader


from src.lib.align_custom import AlignCustom
from src.lib.face_feature import FaceFeature
from src.lib.mtcnn_detect import MTCNNDetect


# Класс лоадера
class LoaderScene(QtCore.QObject):
    startProgram = pyqtSignal(AlignCustom, FaceFeature, MTCNNDetect)

    def __init__(self, parent):
        super().__init__()

        self.MainWindow = parent
        self.centralWidget = QtWidgets.QWidget(self.MainWindow)

        # Задание стилей
        self.setObjectName("loaderWidget")
        self.centralWidget.setFixedWidth(640)
        self.centralWidget.setFixedHeight(700)

        pixmap = QtGui.QPixmap('./styles/SpbPU.png')
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setPixmap(pixmap)
        self.label.setFixedWidth(640)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.labelText = QtWidgets.QLabel(self.centralWidget)
        self.labelText.setText("Загрузка модели...")
        self.labelText.setAlignment(QtCore.Qt.AlignCenter)
        self.labelText.setObjectName("loadingMessage")
        self.labelText.setStyleSheet(
            """
                #loadingMessage {
                    font-size: 15px;
                    font-family: Tahoma;
                }
            """)
        self.labelText.setFixedWidth(640)

        self.authors = QtWidgets.QLabel(self.centralWidget)
        self.authors.setText(
            """FaceRec library: <a href="https://github.com/vudung45/FaceRec">
                                    <font face=verdana size=3 color=black>David Vu</font></a><br>
               Qt design & shell: <a href="https://github.com/meose/faceRec">
                                    <font face=verdana size=3 color=black>Victor Snurnitsyn</font></a>"""
        )
        self.authors.setAlignment(QtCore.Qt.AlignLeft)
        self.authors.setObjectName("authors")
        self.authors.setOpenExternalLinks(True)
        self.authors.setStyleSheet(
            """
                #authors {
                    font-size: 13px;
                    font-family: Tahoma;
                }
            """)
        self.authors.move(400, 650)
        self.authors.setFixedHeight(50)
        self.authors.setFixedWidth(640)

        self.grid1 = QtWidgets.QGridLayout(self.centralWidget)
        self.grid1.setContentsMargins(0, 80, 0, 0)
        self.grid1.addWidget(self.label, 1, 0)
        self.grid1.addWidget(self.labelText, 2, 0)
        self.centralWidget.setLayout(self.grid1)

        # Поток загрузчика
        self.loaderThread = None

        # Модуль для выявления лица
        self.face_detect = None
        # Модуль для выравнивания изображений
        self.aligner = None
        # Выявление особенностей лица
        self.extract_feature = None

    # инициация графических элементов
    def setupUI(self):
        self.MainWindow.setCentralWidget(self.centralWidget)
        self.startLoading()

    # инициация загрузки модулей
    def startLoading(self):
        if self.loaderThread is None:
            self.loaderThread = Loader()
            self.loaderThread.finishLoad.connect(self.loadingFinish)
            self.loaderThread.start()

    # коллбек, вызываемый после загрузки модулей
    def loadingFinish(self, aligner, extract_feature, face_detect):
        self.aligner = aligner
        self.extract_feature = extract_feature
        self.face_detect = face_detect
        # запуск главного окна
        self.startProgram.emit(aligner, extract_feature, face_detect)

    def interruptLoading(self):
        if self.loaderThread is not None:
            self.loaderThread.interrupt()
