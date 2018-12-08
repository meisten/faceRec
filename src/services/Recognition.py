from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage

from src.FaceID import findPeople
from src.mask.CrownMask import CrownMask
import cv2

import imutils


class Recognition(QtCore.QThread):
    log = pyqtSignal(str)
    up = pyqtSignal(QImage)

    def __init__(self, parent=None, face_detect=None, aligner=None, extract_feature=None, name=None, vs=None,
                 rotation=None, jsonpath=None):
        self.face_detect = face_detect
        self.aligner = aligner
        self.extract_feature = extract_feature
        self.targetName = name
        self.running = False
        self.vs = vs
        self.jsonpath = jsonpath

        self.rotation = rotation
        self.crownMask = CrownMask()

        QtCore.QThread.__init__(self, parent)

    def run(self):
        try:
            width = self.vs.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = self.vs.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.running = True
            while self.running:
                _, frame = self.vs.read()
                frame = imutils.rotate_bound(frame, self.rotation)
                rects, landmarks = self.face_detect.detect_face(frame, 80)
                aligns = []
                positions = []
                image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
                                     QtGui.QImage.Format_RGB888).rgbSwapped()
                if len(rects) == 0:
                    self.up.emit(image)
                else:
                    for (i, rect) in enumerate(rects):
                        aligned_face, face_pos = self.aligner.align(160, frame, landmarks[i])
                        if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                            aligns.append(aligned_face)
                            positions.append(face_pos)
                        else:
                            print("Align face failed")
                    if len(aligns) > 0:
                        features_arr = self.extract_feature.get_features(aligns)
                        recog_data = findPeople(features_arr, self.jsonpath, positions)
                        for (i, rect) in enumerate(rects):
                            color = (0, 255, 0)
                            text_color = (255, 255, 255)
                            font = cv2.FONT_HERSHEY_COMPLEX
                            thinkness = 1
                            name = recog_data[i][0]
                            percent = str("%.2f" % recog_data[i][1]) + "%"
                            if name == self.targetName:
                                color = (0, 215, 255)
                                thinkness = 2
                                self.crownMask.addCrown(frame, rect, width, height)
                            if name == "":
                                thinkness = 1
                                color = (255, 255, 255)
                                percent = ""

                            cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), color,
                                          thickness=thinkness)

                            cv2.putText(frame, name, (rect[0] + 5, rect[1] + rect[3] - 5),
                                        font, 0.7, text_color, 1, cv2.LINE_AA)

                            if name != "":
                                cv2.putText(frame, percent, (rect[0] + rect[2], rect[1] + rect[3]),
                                            font, 1, text_color, 1, cv2.LINE_AA)

                            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
                                                 QtGui.QImage.Format_RGB888).rgbSwapped()
                            self.up.emit(image)
                        self.up.emit(image)
                    self.up.emit(image)

                if not self.running:
                    self.quit()

        except Exception as e:
            print(str(e))

    @pyqtSlot(name="interrupt")
    def interrupt(self):
        self.running = False
        self.log.emit("Распознавание прервано по просьбе пользователя")
        print("Recognized thread is killed")
        self.wait()
