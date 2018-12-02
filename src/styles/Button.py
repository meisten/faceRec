from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class Button(QtWidgets.QPushButton):

    def __init__(self, parent=None, enabled=True):
        super(Button, self).__init__(parent)
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setBlurRadius(5)
        effect.setColor(QColor(150, 150, 150))
        self.setGraphicsEffect(effect)
        self.setFixedHeight(40)
        self.setMouseTracking(True)
        self.setEnabled(enabled)
        if self.isEnabled() is True:
            self.setStyleSheet("""margin: 1px; padding: 7px;
                                background-color: rgba(255,255,255,1); 
                                color: rgba(0, 0, 0, 0.3);
                                border-style: none;
                                """)
        else:
            self.setStyleSheet("""
                                margin: 1px; padding: 7px;
                                background-color: rgba(0, 0, 0, 0.1);
                                color: rgba(0, 0, 0, 0.3);
                                border-style: none;
                                """)

    def enterEvent(self, event):
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setBlurRadius(5)
        effect.setColor(QColor(150, 150, 150))
        self.setGraphicsEffect(effect)
        if self.isEnabled() is True:
            self.setStyleSheet("""margin: 1px; padding: 7px;
                            background-color: rgba(255,255,255,1); 
                            color: rgba(52, 180, 73, 255);
                            border-style: none;
                                    """)
        if self.isEnabled() is False:
            self.setStyleSheet("""
                                margin: 1px; padding: 7px;
                                background-color: rgba(0, 0, 0, 0.1);
                                color: rgba(0, 0, 0, 0.3);
                                border-style: none;
                                """)

    def leaveEvent(self, event):
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setBlurRadius(5)
        effect.setColor(QColor(150, 150, 150))
        self.setGraphicsEffect(effect)
        if self.isEnabled() is True:
            self.setStyleSheet("""margin: 1px; padding: 7px;
                                background-color: rgba(255,255,255,1); 
                                color: rgba(0, 0, 0, 0.3);
                                border-style: none;
                                """)
        else:
            self.setStyleSheet("""
                                margin: 1px; padding: 7px;
                                background-color: rgba(0, 0, 0, 0.1);
                                color: rgba(0, 0, 0, 0.3);
                                border-style: none;
                                """)