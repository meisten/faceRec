from PyQt5 import QtWidgets, QtGui

from src.views.LoaderView import LoaderScene
from src.views.MainView import MainScene

font_but = QtGui.QFont()
font_but.setFamily("Segoe UI Symbol")
font_but.setPointSize(10)
font_but.setWeight(95)


# Показ главного элемента
class QthreadApp(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # задание иконки приложения
        image = QtGui.QIcon('./styles/spbstu.png')
        self.setWindowIcon(image)
        # задание стилей
        self.setObjectName("index")
        self.setStyleSheet(
            """
                #index {
                    background-color: white
                }
                #loaderWidget {
                    background-color: black; margin: 7px
                    color: rgba(0, 190, 255, 255);
                }
            """)
        self.setWindowTitle("Обучение и распознавание")
        self.setFixedWidth(640)
        self.setFixedHeight(700)

        ###########################
        self.mainScene = None
        self.loaderScene = None

        # вызов активити лоадера, который подгружает необходимые библиотеки
        self.startLoader()

    # метод для вызова лоадера
    def startLoader(self):
        self.loaderScene = LoaderScene(self)
        # коллбек, вызываемый после того, как все модули будут загружены
        self.loaderScene.startProgram.connect(self.startMain)
        # Отрисовка графических элементов
        self.loaderScene.setupUI()
        self.show()

    def startMain(self, aligner, extract_feature, face_detect):
        self.mainScene = MainScene(self)
        # Отрисовка графических элементов и передача загруженных модулей
        self.mainScene.setupUI(aligner, extract_feature, face_detect)
        self.show()


# Точка входа программы
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
    myapp = QthreadApp(parent=None)
    myapp.activateWindow()
    myapp.setWindowOpacity(1)
    myapp.show()
    myapp.move(resolution.center() - myapp.rect().center())
    sys.exit(app.exec_())
else:
    desktop = QtWidgets.QApplication.desktop()
    resolution = desktop.availableGeometry()
