from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QFrame
import datetime
import os
from os.path import dirname, abspath
import json

from src.services.Identification import Identification
from src.services.Recognition import Recognition

from src.styles.LineEdit import LineEdit
from src.styles.Button import Button

import regex
import cv2

font_but = QtGui.QFont()
font_but.setFamily("Segoe UI Symbol")
font_but.setPointSize(10)
font_but.setWeight(95)


# Главное окно
class MainScene(QtCore.QObject):
    signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.__location__ = dirname(dirname(abspath(__file__)))
        self.MainWindow = parent

        self.vs = cv2.VideoCapture(cv2.CAP_DSHOW)
        # Модуль для выявления лица
        self.face_detect = None
        # Модуль для выравнивания изображений
        self.aligner = None
        # Выявление особенностей лица
        self.extract_feature = None

        # Потоки
        self.identificationThread = None
        self.recognitionThread = None
        self.loaderThread = None

        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.textName = LineEdit(self.centralwidget)
        self.startIdentificationButton = Button(self.centralwidget)
        self.startRecognitionButton = Button(self.centralwidget)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.textf = QtWidgets.QTextEdit(self.centralwidget)
        self.menuLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.delete = Button(self.centralwidget)

        self.buttonStopIdentification = QtWidgets.QPushButton(self.centralwidget)
        self.processMessage = QtWidgets.QLabel(self.centralwidget)

        # Инициация стилей
        self.guiInitLabelBlock()
        self.guiInitNameText()
        self.guiInitStartIdentificationButton()
        self.guiInitStartRecognitionButton()
        self.guiInitStopIdentificationButton()
        self.guiInitLabelTextBlock()
        self.guiInitDeleteButton()
        self.guiInitHBox()
        self.guiInitLogTextLine()

    # Показ текущего окна
    def setupUI(self, aligner, extract_feature, face_detect):
        print("start ui")
        self.aligner = aligner
        self.extract_feature = extract_feature
        self.face_detect = face_detect
        self.MainWindow.setCentralWidget(self.centralwidget)

    # Инициация блока для вывода сообщения об обработке
    def guiInitLabelTextBlock(self):
        self.processMessage.hide()
        self.processMessage.setText("Обработка")
        self.processMessage.setObjectName("message")
        self.processMessage.setFixedWidth(640)
        self.processMessage.setStyleSheet(
            """
                #message {
                    color: white;
                    text-align: center;
                    font: Century Gothic;
                    font-size: 20px;
                }
            """
        )
        self.processMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.processMessage.setText("Обработка...")
        self.processMessage.move(0, 480)

    # Инициация блока для показа картинки
    def guiInitLabelBlock(self):
        self.label.setStyleSheet("""
                                                    background-color: rgba(0, 255, 0, 1); margin: 7px
                                                    color: rgba(0, 190, 255, 255);
                                                    """)
        self.label.setFixedWidth(640)
        self.label.setFixedHeight(480)
        self.label.setObjectName("Video")
        self.label.setStyleSheet(
            """#Video {
                    background-color: rgba(0,0,0,0)
                }
            """)
        self.label.move(0, 60)

    # Инициация текстового блока для ввода имени
    def guiInitNameText(self):
        self.textName.setPlaceholderText("Ваше имя")
        self.textName.setFont(font_but)
        self.textName.setFixedWidth(170)

    # Инициация блока логгирования
    def guiInitLogTextLine(self):
        self.textf.setFrameShape(QFrame.NoFrame)
        self.textf.setPlaceholderText("Логгирование туть")
        self.textf.setReadOnly(True)
        self.textf.setObjectName("loggerBlock")
        self.textf.setStyleSheet(
            """
                #loggerBlock:disabled {
                    background-color: white;
                    font-size:14px
                }
            """)
        effect = QGraphicsDropShadowEffect(self.centralwidget)
        effect.setOffset(0, 0)
        effect.setBlurRadius(5)
        effect.setColor(QColor(150, 150, 150))
        self.textf.setGraphicsEffect(effect)
        self.textf.setFixedWidth(640)
        self.textf.setFixedHeight(160)
        self.textf.move(0, 540)

    # Инициация кнопки старта обучения
    def guiInitStartIdentificationButton(self):
        self.startIdentificationButton.setText("Обучение")
        self.startIdentificationButton.setFixedWidth(120)
        self.startIdentificationButton.setFont(font_but)
        self.startIdentificationButton.clicked.connect(self.startIdentification)

    # Инициация кнопки успешного завершения идентификации
    def guiInitStopIdentificationButton(self):
        self.buttonStopIdentification.setText("Завершить идентификацию")
        self.buttonStopIdentification.setObjectName("stopIdentificationButton")
        effect = QGraphicsDropShadowEffect(self.centralwidget)
        effect.setOffset(0, 0)
        effect.setBlurRadius(45)
        effect.setColor(QColor(255, 255, 255))
        self.buttonStopIdentification.setFixedWidth(500)
        self.buttonStopIdentification.setFixedHeight(50)
        self.buttonStopIdentification.setFont(font_but)
        self.buttonStopIdentification.setStyleSheet(
            """
                #stopIdentificationButton {
                    background-color: rgba(0,0,0,0);
                    color: rgba(210,210,210,1);
                    border: 1px solid rgba(210,210,210,1);
                    border-radius: 6px;
                    text-shadow: 0px 0px 2px black;
                }
                #stopIdentificationButton:hover {
                    background-color: rgba(0,0,0,0);
                    color: white;
                    border: 1px solid white;
                    border-radius: 6px;
                    text-shadow: 0px 0px 2px black;
                }
            """
        )
        self.buttonStopIdentification.setGraphicsEffect(effect)
        self.buttonStopIdentification.hide()
        self.buttonStopIdentification.move(70, 480)
        self.buttonStopIdentification.clicked.connect(self.stopIdentification)

    # Инициация кнопки старта распознания
    def guiInitStartRecognitionButton(self):
        self.startRecognitionButton.setText("Распознавание")
        self.startRecognitionButton.setFixedWidth(180)
        self.startRecognitionButton.setFont(font_but)
        self.startRecognitionButton.clicked.connect(self.startRecognition)

    # Инициация кнопки удаления
    def guiInitDeleteButton(self):
        self.delete.setText("Удалить")
        self.delete.setFixedWidth(120)
        self.delete.setFont(font_but)
        self.delete.clicked.connect(self.deleteRow)

    # Инициация меню-бокса
    def guiInitHBox(self):
        self.menuLayout.addWidget(self.textName, alignment=QtCore.Qt.AlignTop)
        self.menuLayout.addWidget(self.startIdentificationButton, alignment=QtCore.Qt.AlignTop)
        self.menuLayout.addWidget(self.startRecognitionButton, alignment=QtCore.Qt.AlignTop)
        self.menuLayout.addWidget(self.delete, alignment=QtCore.Qt.AlignTop)
        self.menuLayout.setContentsMargins(7, 7, 7, 7)

    # Метод, вызываемый при клике на "Удалить". Происходит считывание имени, нахождение его в json и удаление его
    def deleteRow(self):
        try:
            name = self.textName.text()
            if name == "":
                self.log("Задано пустое имя")
                return

            if regex.search(r'\p{IsCyrillic}', name):
                self.log("Имя содержит недопустимые символы. Введите имя на английском")
                return

            f = open(os.path.join(self.__location__, 'services/storage.json'), 'r')
            data_set = json.loads(f.read())

            if name in data_set:
                data_set.pop(name)
                f = open(os.path.join(self.__location__, 'services/storage.json'), 'w')
                f.write(json.dumps(data_set))
                self.log("Пользователь " + name + " удален")
            else:
                self.log("Пользователь " + name + " не найден в базе")
            f.close()
        except Exception as e:
            print("3:" + str(e))

    # Метод, вызываемый при клике на "Обучение". Считывание имени. Прерывание процесса распознавания (если есть).
    # Запуск процесса обучения
    def startIdentification(self):
        try:
            name = self.textName.text()
            if name == "":
                self.log("Введите имя")
                return

            if regex.search(r'\p{IsCyrillic}', name):
                self.log("Имя содержит недопустимые символы. Введите имя на английском")
                return

            if self.recognitionThread is not None:
                self.recognitionThread.interrupt()
                self.recognitionThread = None

            if self.identificationThread is None:
                self.identificationThread = Identification(
                    face_detect=self.face_detect, aligner=self.aligner, extract_feature=self.extract_feature,
                    name=name, vs=self.vs
                )
                self.signal.connect(self.identificationThread.stop)
                self.identificationThread.start()
                self.identificationThread.log.connect(self.log)
                self.identificationThread.up.connect(self.update)
                self.identificationThread.process.connect(self.process)
                self.identificationThread.successfulSaveIdentificationResult.connect(
                    self.successfulSaveIdentificationResult
                )
                self.identificationThread.allowStopIdentification.connect(self.allowStopIdentification)
                self.identificationThread.disAllowStopIdentification.connect(self.disAllowStopIdentification)
                self.log("Необходимо получить особенности лица. Поворачивайте голову.")
            else:
                self.log("Уже запущено")

        except Exception as e:
            print("2:" + str(e))

    # Успешное завершение процесса обучения (кнопка "Завершить идентификацию")
    def stopIdentification(self):
        try:
            if self.identificationThread is not None:
                self.signal.emit()
        except Exception as e:
            print("4: " + str(e))

    # Коллбек, вызываемый процессом обучения (успешное сохранение данных)
    def successfulSaveIdentificationResult(self):
        self.identificationThread = None
        if self.recognitionThread is None:
            self.recognitionThread = Recognition(
                face_detect=self.face_detect, aligner=self.aligner, extract_feature=self.extract_feature,
                name=self.textName.text(), vs=self.vs
            )
            self.recognitionThread.start()
            self.recognitionThread.log.connect(self.log)
            self.recognitionThread.up.connect(self.update)
            self.log("Процесс распознавания начат.")
        else:
            self.label.setText("")

    # Метод, вызываемый при клике на "Распознание". Считывание имени. Прерывание процесса идентификации (если есть).
    # Запуск процесса распознания
    def startRecognition(self):
        try:
            name = self.textName.text()
            if name == "":
                self.log("Введите имя")
                return

            if regex.search(r'\p{IsCyrillic}', name):
                self.log("Имя содержит недопустимые символы. Введите имя на английском")
                return

            if self.identificationThread is not None:
                self.identificationThread.interrupt()
                self.identificationThread = None

            if self.recognitionThread is not None:
                self.recognitionThread.interrupt()

            self.buttonStopIdentification.hide()
            self.recognitionThread = Recognition(
                face_detect=self.face_detect, aligner=self.aligner, extract_feature=self.extract_feature,
                name=name, vs=self.vs
            )
            self.recognitionThread.start()
            self.recognitionThread.log.connect(self.log)
            self.recognitionThread.up.connect(self.update)
            self.log("Процесс распознавания начат.")
        except Exception as e:
            print("1: " + str(e))

    # Коллбек, вызываемый для добавления записи в текстовый блок (время + сообщение)
    def log(self, string):
        self.textf.append(str(datetime.datetime.now().time()) + ": " + string)

    # Коллбек, вызываемый для обновления картинки
    def update(self, qimage):
        self.label.setPixmap(QtGui.QPixmap(qimage))
        self.processMessage.hide()

    # Коллбек, вызываемый при обработке данных (серое размытое изображение + текст "Обработка")
    def process(self, qimage):
        self.label.setPixmap(QtGui.QPixmap(qimage))
        self.processMessage.show()

    # Коллбек, вызываемый в случае, если данных, полученных с камеры, хватает для обучения (все три стороны считаны)
    # Показывает кнопку "Завершить идентификацию")
    def allowStopIdentification(self):
        self.buttonStopIdentification.show()

    # Коллбек, вызываемый в случае, когда происходит сохранение данных (скрывает кнопку "Завершить идентификацию")
    def disAllowStopIdentification(self):
        self.buttonStopIdentification.hide()

