import sys

import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QComboBox, QLabel, QApplication, QFileDialog, QSlider
)
from PyQt6.QtCore import Qt


# TODO: implementation of video special effect
class SpecialEffect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Special Effect")
        self.setGeometry(200, 200, 800, 200)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.move(10, 90)
        self.slider.setRange(-100, 100)
        self.slider.setSingleStep(2)
        self.slider.valueChanged.connect(self.slider.setValue)

        picture_button = QPushButton("read image", self)
        picture_button.setGeometry(10, 10, 100, 30)
        picture_button.clicked.connect(self.open_picture)

        emboss_button = QPushButton("embossing", self)
        emboss_button.setGeometry(110, 10, 100, 30)
        emboss_button.clicked.connect(self.emboss)

        cartoon_button = QPushButton("cartoon", self)
        cartoon_button.setGeometry(210, 10, 100, 30)
        cartoon_button.clicked.connect(self.cartoon)

        sketch_button = QPushButton("pencil sketch", self)
        sketch_button.setGeometry(310, 10, 100, 30)
        sketch_button.clicked.connect(self.sketch)

        oil_button = QPushButton("oil", self)
        oil_button.setGeometry(410, 10, 100, 30)
        oil_button.clicked.connect(self.oil)

        save_button = QPushButton("save", self)
        save_button.setGeometry(510, 10, 100, 30)
        save_button.clicked.connect(self.save)

        self.pick_combo = QComboBox(self)
        self.pick_combo.addItems(
            ["embossing", "cartoon", "sketch(gray)", "sketch(coloer)", "oil"]
        )
        self.pick_combo.setGeometry(510, 40, 110, 30)

        quit_button = QPushButton("exit", self)
        quit_button.setGeometry(620, 10, 100, 30)
        quit_button.clicked.connect(self.quit_)

        self.label = QLabel("Welcome!", self)
        self.label.setGeometry(10, 90, 500, 170)

        video_button = QPushButton("video start", self)
        video_button.setGeometry(10, 50, 100, 30)
        video_button.clicked.connect(self.video_effect)

        video_quit_button = QPushButton("video exit", self)
        video_quit_button.setGeometry(110, 50, 100, 30)
        video_quit_button.clicked.connect(self.video_quit)

        bright_control = QPushButton("bright", self)
        bright_control.setGeometry(110, 90, 100, 30)
        bright_control.clicked.connect(self.bright_control_function)

        self.images = dict()

    def open_picture(self):
        fname = QFileDialog.getOpenFileName(self, "Read Image", "./")
        self.img = cv2.imread(fname[0])
        if self.img is None:
            sys.exit("FileError")
        cv2.imshow("Painting", self.img)

    def video_special_effect(self):
        pass

    def emboss(self):
        femboss = np.array([
            [-1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0]
        ])

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray16 = np.int16(gray)
        self.images["embossing"] = np.uint8(
            np.clip(cv2.filter2D(gray16, -1, femboss) + 128, 0, 255)
        )
        cv2.imshow("Emboss", self.images["embossing"])

    def cartoon(self):
        self.images["cartoon"] = cv2.stylization(
            self.img,
            sigma_s=60,
            sigma_r=0.45
        )
        cv2.imshow("Cartoon", self.images["cartoon"])

    def sketch(self):
        self.images["sketch_gray"], self.images["sketch_color"] = \
            cv2.pencilSketch(
                self.img,
                sigma_s=60,
                sigma_r=0.07,
                shade_factor=0.02
            )
        cv2.imshow("Pencil Sketch(gray)", self.images["sketch_gray"])
        cv2.imshow("Pencil sketch(color)", self.images["sketch_color"])

    def oil(self):
        self.images["oil"] = cv2.xphoto.oilPainting(
            self.img, 10, 1, cv2.COLOR_BGR2Lab
        )
        cv2.imshow("Oil Painting", self.images["oil"])

    def save(self):
        fname = QFileDialog.getSaveFileName(self, "File Save", "./")
        i = self.pick_combo.currentIndex()
        OPTIONS = [
            "embossing",
            "cartoon",
            "sketch_gray",
            "sketch_color",
            "oil"
        ]
        cv2.imwrite(fname[0], self.images[OPTIONS[i]])

    def quit_(self):
        cv2.destroyAllWindows()
        self.close()

    def video_effect(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            sys.exit("Camera Connection Fail!")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            pick_effect = self.pick_combo.currentIndex()
            match pick_effect:
                case 0:
                    femboss = np.array([
                        [-1.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0],
                        [0.0, 0.0, 1.0]
                    ])
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray16 = np.int16(gray)
                    special_img = np.uint8(
                        np.clip(
                            cv2.filter2D(gray16, -1, femboss) + 128,
                            0,
                            255
                        )
                    )
                case 1:
                    special_img = cv2.stylization(
                        frame,
                        sigma_s=60,
                        sigma_r=0.45
                    )
                case 2:
                    special_img, _ = cv2.pencilSketch(
                        frame,
                        sigma_s=60,
                        sigma_r=0.07,
                        shade_factor=0.02
                    )
                case 3:
                    _, special_img = cv2.pencilSketch(
                        frame,
                        sigma_s=60,
                        sigma_r=0.07,
                        shade_factor=0.02
                    )
                case 4:
                    special_img = cv2.xphoto.oilPainting(
                        frame,
                        10,
                        1,
                        cv2.COLOR_BGR2Lab
                    )

            cv2.imshow("Special Effect", special_img)
            cv2.waitKey(1)

    def bright_control_function(self):
        self.img = cv2.add(self.img, self.slider.value())
        cv2.imshow("Special Effect", self.img)

    def video_quit(self):
        self.cap.release()
        cv2.destroyWindow("Special Effect")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SpecialEffect()
    win.show()
    app.exec()
