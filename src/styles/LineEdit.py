from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class LineEdit(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setBlurRadius(5)
        effect.setColor(QColor(150, 150, 150))
        self.setGraphicsEffect(effect)
        self.setMouseTracking(True)
        self.setFixedHeight(40)
        self.setStyleSheet("""margin: 1px; padding: 7px;
                            background-color: rgba(255,255,255,1); 
                            color: rgba(0, 0, 0, 0.3);
                            border-style: none;
                            """)

    def leaveEvent(self, event):
        effect = QGraphicsDropShadowEffect(self)
        effect.setOffset(0, 0)
        effect.setBlurRadius(5)
        effect.setColor(QColor(150, 150, 150))
        self.setGraphicsEffect(effect)
        self.setStyleSheet("""margin: 1px; padding: 7px;
                            background-color: rgba(255,255,255,1); 
                            color: rgba(0, 0, 0, 0.3);
                            border-style: none;
                            """)