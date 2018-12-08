from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

import os

from src.lib.align_custom import AlignCustom
from src.lib.face_feature import FaceFeature
from src.lib.mtcnn_detect import MTCNNDetect
from src.lib.tf_graph import FaceRecGraph


class Loader(QtCore.QThread):
    finishLoad = pyqtSignal(AlignCustom, FaceFeature, MTCNNDetect)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def run(self):
        FRGraph = FaceRecGraph()
        aligner = AlignCustom()
        extract_feature = FaceFeature(FRGraph)
        face_detect = MTCNNDetect(FRGraph, scale_factor=2)
        self.finishLoad.emit(aligner, extract_feature, face_detect)
        self.quit()

    def interrupt(self):
        self.quit()
