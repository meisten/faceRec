import cv2
import os


class CrownMask:

    def __init__(self):
        self.x_offset = self.y_offset = 50
        self.__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        print(os.path.join(self.__location__, '3.png'))
        self.crown = cv2.imread(os.path.join(self.__location__, '3.png'), -1)
        self.alpha_s = self.crown[:, :, 3] / 255.0
        self.alpha_l = 1.0 - self.alpha_s

    def addCrown(self, frame, rect, width, height):
        middle_x = rect[0] + int(rect[2] / 2)
        middle_y = rect[1]
        y1, y2 = middle_y - self.crown.shape[0] + 65, middle_y + 65
        x1, x2 = middle_x - 60, middle_x + self.crown.shape[1] - 60

        if 0 < y1 < height and 0 < y2 < height and 0 < x1 < width and 0 < x2 < width:
            for c in range(0, 3):
                frame[y1:y2, x1:x2, c] = (self.alpha_s * self.crown[:, :, c] + self.alpha_l * frame[y1:y2, x1:x2, c])
        return frame
